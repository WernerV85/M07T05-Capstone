"""Session-based cart helper.

Cart data is stored in the session and cleared when the session ends.
"""
from decimal import Decimal
from copy import deepcopy
from product.models import Product


class Cart:
    """Session-backed shopping cart.

    :param request: Django HttpRequest used to access the session.
    """

    def __init__(self, request):
        """Initialise the cart.

        :param request: Django HttpRequest object to access session.
        """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Save an empty cart in the session
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Add a product or update its quantity.

        :param product: Product instance to add.
        :param quantity: Quantity to add or set.
        :param update_quantity: When True, replace quantity instead of add.
        """
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
        """Mark the session as modified so it gets saved."""
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart.

        :param product: Product instance to remove.
        """
        product_id = str(product.prod_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterate over cart items with attached Product objects.

        :return: An iterator of cart item dictionaries.
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
        """Count all items in the cart.

        :return: Total quantity of items.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate the total price of all items in the cart.

        :return: Total price as a Decimal.
        """
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """Remove cart from session."""
        del self.session['cart']
        self.save()
