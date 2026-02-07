'''Session-based cart helper
Cart is stored in the session and automatically clears when the session ends.
'''
from decimal import Decimal
from copy import deepcopy
from product.models import Product


class Cart:
    """Session-based shopping cart"""

    def __init__(self, request):
        """Initialize the cart"""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Save an empty cart in the session
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Add a product to the cart or update its quantity"""
        product_id = str(product.prod_id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Mark the session as modified to make sure it gets saved"""
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart"""
        product_id = str(product.prod_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over items in cart and get products from database
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(prod_id__in=product_ids)
        # Use deepcopy to avoid modifying session data with Decimal objects
        cart = deepcopy(self.cart)

        for product in products:
            cart[str(product.prod_id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate the total price of all items in the cart"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """Remove cart from session"""
        del self.session['cart']
        self.save()
