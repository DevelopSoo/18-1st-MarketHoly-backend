import uuid
import json

from django.db        import transaction
from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse

from user.models     import User, Address
from product.models  import Product
from order.models    import Order, Cart, OrderStatus
from utils.decorator import login_required


DEFAULT_ORDER_STATUS = 1
class CartView(View):
    @transaction.atomic
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)

            id       = int(data['id'])
            quantity = int(data['quantity'])
                       
            product = Product.objects.get(id=id)

            if quantity > product.stock:
                return JsonResponse({'message': '구매가능수량초과'}, status=400)


            if not Order.objects.filter(user=request.user, order_status_id=DEFAULT_ORDER_STATUS).exists():
                created_order = Order(user         = request.user,
                                      price        = 0,
                                      order_number = str(uuid.uuid1()),
                                      order_status = DEFAULT_ORDER_STATUS)
                created_order.save()

            current_order = Order.objects.get(user=request.user, order_status_id=DEFAULT_ORDER_STATUS)
            cart, created = Cart.objects.get_or_create(order = current_order,
                                                       product = product)
            
            if created:
                cart.quantity = 0
            cart.quantity += quantity
            cart.save()
   
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except TypeError:
            return JsonResponse({'message': 'TypeError'}, status=400)

    @login_required
    def get(self, request):
        user = request.user
        
        default      = user.address_set.get(is_default=True)
        full_address = str(default.address) + (str(default.detail_address) if default.detail_address else "")
        
        
        if not Order.objects.filter(user=user, order_status_id=DEFAULT_ORDER_STATUS).exists():
            products = []

        products_in_cart = Order.objects.get(user=user, order_status_id=DEFAULT_ORDER_STATUS).cart_order.all()

        products = [{
                    'id': in_cart.id,
                    'product_id': in_cart.product.id,
                    'name': in_cart.product.name,
                    'img_url': in_cart.product.image_url,
                    'price': in_cart.product.price,
                    'quantity': in_cart.quantity
                } for in_cart in products_in_cart]

        return JsonResponse({'address': 'full_address', 'products': products}, status=200)


class OrderView(View):
    @login_required
    @transaction.atomic
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            carts = data['result']
            price = int(data['total_price'])

            new_order = Order.objects.create(
                                          user=user,
                                          order_status_id=2,
                                          price=price,
                                          order_number=str(uuid.uuid1())
                                          )

            for cart_id in carts:
                cart = Cart.objects.get(id=cart_id)
                cart.order = new_order
                cart.save()
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)
        
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)

