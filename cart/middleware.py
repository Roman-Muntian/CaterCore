# cart/middleware.py
from .models import Cart

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()
        
        session_key = request.session.session_key
        request.cart, created = Cart.objects.get_or_create(session_key=session_key)
        
        response = self.get_response(request)
        return response