''' module to define store views
Includes:
- List all stores
- Store detail view
- Create new store
- Update existing store
- Delete store
'''

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store, StoreSerializer
from .forms import StoreForm
from django.http import JsonResponse
from rest_framework.decorators import (
    api_view, renderer_classes, authentication_classes, permission_classes
)
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


def store_list(request):
    """List all stores - accessible to all users"""
    stores = Store.objects.all()
    return render(request, 'store/store_list.html', {'stores': stores})


def store_detail(request, store_id):
    """Get a single store by ID"""
    store = get_object_or_404(Store, pk=store_id)
    return render(request, 'store/store_detail.html', {'store': store})


@login_required
def store_create(request):
    """Create a new store - vendors only"""
    # Check if user is a vendor
    if request.user.user_type != 'vendor':
        messages.error(request, 'Only vendors can create stores')
        return redirect('store_list')

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.save()
            messages.success(
                request, f'Store "{store.store_name}" created successfully!'
            )
            return redirect('store_detail', store_id=store.store_id)
    else:
        form = StoreForm()

    return render(request, 'store/store_form.html', {'form': form})


@login_required
def store_update(request, store_id):
    """Update an existing store - vendors only"""
    store = get_object_or_404(Store, pk=store_id)

    # Check if user is a vendor
    if request.user.user_type != 'vendor':
        messages.error(request, 'Only vendors can update stores')
        return redirect('store_detail', store_id=store_id)

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Store "{store.store_name}" updated successfully!'
            )
            return redirect('store_detail', store_id=store.store_id)
    else:
        form = StoreForm(instance=store)

    return render(request, 'store/store_form.html', {
        'store': store,
        'form': form
    })


@login_required
def store_delete(request, store_id):
    """Delete a store - vendors only"""
    store = get_object_or_404(Store, pk=store_id)

    # Check if user is a vendor
    if request.user.user_type != 'vendor':
        messages.error(request, 'Only vendors can delete stores')
        return redirect('store_detail', store_id=store_id)

    if request.method == 'POST':
        store_name = store.store_name
        store.delete()
        messages.success(
            request, f'Store "{store_name}" deleted successfully!'
        )
        return redirect('store_list')

    return render(request, 'store/store_confirm_delete.html', {'store': store})


@api_view(['GET'])
def view_stores(request):
    """API endpoint to get all stores in JSON format"""
    serializer = StoreSerializer(Store.objects.all(), many=True)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET'])
@renderer_classes([XMLRenderer])
def view_stores_xml(request):
    serializer = StoreSerializer(Store.objects.all(), many=True)
    return Response(data=serializer.data)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_store(request):
    if request.user.user_type == 'vendor':
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically assign the logged-in vendor to the store
            serializer.save(vendor=request.user)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(
        {'Permission denied': 'Only vendors can create stores'},
        status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def view_stores_by_vendor(request, vendor_id):
    """API endpoint to get all stores for a specific vendor"""
    stores = Store.objects.filter(vendor_id=vendor_id)
    serializer = StoreSerializer(stores, many=True)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET'])
def view_products_by_store(request, store_id):
    """API endpoint to get all products for a specific store"""
    from product.models import Product, ProductSerializer
    products = Product.objects.filter(store_id=store_id)
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(data=serializer.data, safe=False)
