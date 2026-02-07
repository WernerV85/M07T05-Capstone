'''module for the product view
Includes:
- List all products
- Product detail view
- Create new product
- Update existing product
- Delete product
'''

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductSerializer
from .forms import ProductForm
from django.http import JsonResponse
from rest_framework.decorators import (
    api_view, renderer_classes, authentication_classes, permission_classes
)
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


def product_list(request):
    """List all products - accessible to all users"""
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})


def product_detail(request, prod_id):
    """Get a single product by ID"""
    product = get_object_or_404(Product, pk=prod_id)
    return render(request, 'product/product_detail.html', {'product': product})


@login_required
def product_create(request):
    """Create a new product - vendors only"""
    from django.contrib import messages
    from store.models import Store

    # Check if user is a vendor
    if request.user.user_type != 'vendor':
        messages.error(request, 'Only vendors can create products')
        return redirect('product_list')

    if request.method == 'POST':
        data = request.POST.copy()
        if 'store_id' in data and 'store' not in data:
            data['store'] = data['store_id']
        form = ProductForm(data, user=request.user)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, f'Product "{product.name}" created successfully!'
            )
            return redirect('product_detail', prod_id=product.prod_id)
    else:
        form = ProductForm(user=request.user)

    stores = Store.objects.filter(vendor=request.user)
    return render(request, 'product/product_form.html', {
        'stores': stores,
        'form': form
    })


@login_required
def product_update(request, prod_id):
    """Update an existing product - vendors only"""
    from django.contrib import messages
    from store.models import Store

    product = get_object_or_404(Product, pk=prod_id)

    # Check if user is a vendor
    if request.user.user_type != 'vendor':
        messages.error(request, 'Only vendors can update products')
        return redirect('product_detail', prod_id=prod_id)

    if product.store.vendor != request.user:
        messages.error(request, 'You can only update your own products')
        return redirect('product_detail', prod_id=product.prod_id)

    if request.method == 'POST':
        data = request.POST.copy()
        if 'store_id' in data and 'store' not in data:
            data['store'] = data['store_id']
        form = ProductForm(data, instance=product, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Product "{product.name}" updated successfully!'
            )
            return redirect('product_detail', prod_id=product.prod_id)
    else:
        form = ProductForm(instance=product, user=request.user)

    stores = Store.objects.filter(vendor=request.user)
    return render(request, 'product/product_form.html', {
        'product': product,
        'stores': stores,
        'form': form
    })


@login_required
def product_delete(request, prod_id):
    """Delete a product - vendors only"""
    from django.contrib import messages

    product = get_object_or_404(Product, pk=prod_id)

    # Check if user is a vendor
    if request.user.user_type != 'vendor':
        messages.error(request, 'Only vendors can delete products')
        return redirect('product_detail', prod_id=prod_id)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(
            request, f'Product "{product_name}" deleted successfully!'
        )
        return redirect('product_list')

    return render(
        request,
        'product/product_confirm_delete.html',
        {'product': product}
    )


@api_view(['GET'])
def view_products(request):
    """API endpoint to get all products in JSON format"""
    serializer = ProductSerializer(Product.objects.all(), many=True)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET'])
@renderer_classes([XMLRenderer])
def view_products_xml(request):
    serializer = ProductSerializer(Product.objects.all(), many=True)
    return Response(data=serializer.data)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_product(request):
    if request.user.user_type == 'vendor':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                data=serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(
        {'Permission denied': 'Only vendors can create products'},
        status=status.HTTP_403_FORBIDDEN)
