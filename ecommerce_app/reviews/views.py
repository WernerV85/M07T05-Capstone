''' module for review views
Includes:
- List all reviews
- Review detail view
- Create new review
'''
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, ReviewSerializer
from .forms import ReviewForm
from django.http import JsonResponse
from rest_framework.decorators import (
    api_view, renderer_classes, authentication_classes, permission_classes
)
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


def review_list(request):
    """List all reviews.

    :param request: Django HttpRequest.
    :return: Rendered review list page.
    """
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})


def review_detail(request, review_id):
    """Display details for a single review.

    :param request: Django HttpRequest.
    :param review_id: Review identifier.
    :return: Rendered review detail page.
    """
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


@login_required
def review_create(request):
    """Create a new review (authenticated users).

    :param request: Django HttpRequest.
    :return: Rendered form or redirect.
    """
    from product.models import Product
    from cart.models import OrderItem

    if request.method == 'POST':
        data = request.POST.copy()
        if 'product_id' in data and 'product' not in data:
            data['product'] = data['product_id']
        form = ReviewForm(data)
        if form.is_valid():
            product_id = form.cleaned_data['product'].prod_id

            # Check if user purchased this product
            is_verified = OrderItem.objects.filter(
                order__user=request.user,
                product_id=product_id,
                order__status='completed'
            ).exists()

            review = form.save(commit=False)
            review.user = request.user
            review.username = request.user.username
            review.is_verified_purchase = is_verified
            review.save()

            messages.success(
                request,
                f'Review for {review.product.name} submitted successfully!'
            )
            return redirect('product_detail', prod_id=product_id)
    else:
        form = ReviewForm()

    # GET request - show review form
    product_id = request.GET.get('product_id')
    product = None
    if product_id:
        product = get_object_or_404(Product, prod_id=product_id)

    return render(request, 'reviews/review_form.html', {
        'product': product,
        'form': form
    })


@api_view(['GET'])
def view_reviews(request):
    """Return all reviews in JSON format.

    :param request: Django HttpRequest.
    :return: JsonResponse with reviews.
    """
    serializer = ReviewSerializer(Review.objects.all(), many=True)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET'])
@renderer_classes([XMLRenderer])
def view_reviews_xml(request):
    """Return all reviews in XML format.

    :param request: Django HttpRequest.
    :return: DRF Response with reviews in XML.
    """
    serializer = ReviewSerializer(Review.objects.all(), many=True)
    return Response(data=serializer.data)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_review(request):
    """Create a new review via the API.

    :param request: Django HttpRequest.
    :return: JsonResponse with review data or errors.
    """
    if request.user.id == request.data.get('user'):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                data=serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(
        {'ID mismatch': 'User Id and Review user ID not matching'},
        status=status.HTTP_403_FORBIDDEN)
