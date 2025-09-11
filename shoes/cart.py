from decimal import Decimal
from django.conf import settings
from .models import Shoe

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, shoe, quantity=1, size=None, color=None):
        shoe_id = str(shoe.id)
        key = f"{shoe_id}_{size}_{color}"
        
        if key not in self.cart:
            self.cart[key] = {
                'quantity': 0,
                'price': str(shoe.price),
                'size': size,
                'color': color
            }
        
        self.cart[key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, shoe, size=None, color=None):
        shoe_id = str(shoe.id)
        key = f"{shoe_id}_{size}_{color}"
        
        if key in self.cart:
            del self.cart[key]
            self.save()

    def update(self, shoe, quantity, size=None, color=None):
        shoe_id = str(shoe.id)
        key = f"{shoe_id}_{size}_{color}"
        
        if key in self.cart:
            self.cart[key]['quantity'] = quantity
            self.save()

    def __iter__(self):
        shoe_ids = [key.split('_')[0] for key in self.cart.keys()]
        shoes = Shoe.objects.filter(id__in=shoe_ids)
        cart = self.cart.copy()
        
        for shoe in shoes:
            for key, item in cart.items():
                if key.startswith(str(shoe.id)):
                    item['shoe'] = shoe
                    item['total_price'] = Decimal(item['price']) * item['quantity']
                    yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()