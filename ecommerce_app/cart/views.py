'''Cart views
Includes:
- Add to cart (buyers only)
- View cart
- Update cart item quantity
- Remove from cart
- Checkout (send email with cart summary)
'''
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from product.models import Product
from .models import Order, OrderItem, OrderSerializer
from .cart import Cart
from django.http import JsonResponse
from rest_framework.decorators import (
    api_view, renderer_classes, authentication_classes, permission_classes
)
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


def _parse_quantity(raw_value):
    """Parse quantity input into an integer.

    :param raw_value: Raw value from request data.
    :return: Parsed integer quantity or None if invalid.
    """
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        return None


@login_required
def cart_add(request, product_id):
    """Add a product to the cart.

    :param request: Django HttpRequest.
    :param product_id: Product identifier to add.
    :return: Redirect response.
    """
    # Check if user is authenticated and is a buyer
    if request.user.user_type != 'buyer':
        messages.error(request, 'Only buyers can add items to cart')
        return redirect('product_list')

    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, prod_id=product_id)

        quantity = _parse_quantity(request.POST.get('quantity', 1))
        if quantity is None or quantity < 1:
            messages.error(request, 'Quantity must be a positive whole number.')
            return redirect('product_list')

        update = request.POST.get('update', False)
        update = str(update).lower() in ['1', 'true', 'on', 'yes']

        cart.add(product=product, quantity=quantity, update_quantity=update)
        messages.success(request, f'{product.name} added to cart')
        return redirect('cart_view')

    return redirect('product_list')


@login_required
def cart_view(request):
    """Render the shopping cart view.

    :param request: Django HttpRequest.
    :return: Rendered cart page.
    """
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
def cart_remove(request, product_id):
    """Remove a product from the cart.

    :param request: Django HttpRequest.
    :param product_id: Product identifier to remove.
    :return: Redirect response.
    """
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, prod_id=product_id)
        cart.remove(product)
        messages.success(request, f'{product.name} removed from cart')

    return redirect('cart_view')


@login_required
def cart_update(request, product_id):
    """Update the quantity of a product in the cart.

    :param request: Django HttpRequest.
    :param product_id: Product identifier to update.
    :return: Redirect response.
    """
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, prod_id=product_id)

        quantity = _parse_quantity(request.POST.get('quantity', 1))
        if quantity is None or quantity < 0:
            messages.error(request, 'Quantity must be zero or a positive whole number.')
            return redirect('cart_view')

        if quantity > 0:
            cart.add(product=product, quantity=quantity, update_quantity=True)
            messages.success(request, f'{product.name} quantity updated')
        else:
            cart.remove(product)
            messages.success(request, f'{product.name} removed from cart')

    return redirect('cart_view')


@login_required
def cart_checkout(request):
    """Checkout and place the order.

    :param request: Django HttpRequest.
    :return: Rendered response or redirect.
    """
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, 'Your cart is empty')
        return redirect('cart_view')

    if request.method == 'POST':
        # Build email content
        email_subject = f'Order Confirmation - {request.user.username}'

        email_body = f'''Hello {request.user.first_name} \
{request.user.last_name},

Thank you for your order! Here is your order summary:

ORDER DETAILS:
-------------
'''

        for item in cart:
            product = item['product']
            email_body += f'''
Product: {product.name}
Description: {product.description}
Price: ${item['price']:.2f}
Quantity: {item['quantity']}
Subtotal: ${item['total_price']:.2f}
-------------
'''

        total = cart.get_total_price()
        email_body += f'''

TOTAL: ${total:.2f}

Your order has been received and will be processed shortly.

Thank you for shopping with us!

Best regards,
eCommerce Team
'''

        # Create order record
        try:
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                status='completed'
            )

            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=Decimal(str(item['price']))
                )

            # Send email
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            # Clear the cart after successful checkout
            cart.clear()

            messages.success(
                request,
                'Order placed successfully! '
                'Check your email for confirmation.'
            )
            return render(
                request,
                'cart/checkout_success.html',
                {'order': order}
            )

        except Exception as e:
            messages.error(request, f'Failed to process order: {str(e)}')
            return redirect('cart_view')

    # GET request - show checkout confirmation page
    return render(request, 'cart/checkout_confirm.html', {'cart': cart})


@api_view(['GET'])
def view_orders(request):
    """Return all orders in JSON format.

    :param request: Django HttpRequest.
    :return: JsonResponse containing orders.
    """
    serializer = OrderSerializer(Order.objects.all(), many=True)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET'])
@renderer_classes([XMLRenderer])
def view_orders_xml(request):
    """Return all orders in XML format.

    :param request: Django HttpRequest.
    :return: DRF Response containing orders in XML.
    """
    serializer = OrderSerializer(Order.objects.all(), many=True)
    return Response(data=serializer.data)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_order(request):
    """Create a new order for the authenticated user.

    :param request: Django HttpRequest.
    :return: JsonResponse with order data or errors.
    """
    if request.user.id == request.data.get('user'):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                data=serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(
        {'ID mismatch': 'User Id and Order user ID not matching'},
        status=status.HTTP_403_FORBIDDEN)
