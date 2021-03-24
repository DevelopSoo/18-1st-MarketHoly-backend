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

class AddToCartView(View):
    @transaction.atomic
    @login_required
    def get(self, request):
        try:
            user     = request.user
            id       = request.GET.get('id')
            quantity = int(request.GET.get('quantity'))

            exist_product = Product.objects.filter(id=id).exists()
            if not exist_product:
                return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=400)
            
            product = Product.objects.get(id=id)

            if quantity > product.stock:
                return JsonResponse({'message': '구매가능수량초과'}, status=400)

            order_status = OrderStatus.objects.get(name="장바구니")
            
            has_cart = Order.objects.filter(Q(user=user) & Q(order_status=order_status)).exists()
            if has_cart:
                order = Order.objects.get(Q(user=user) & Q(order_status=order_status))

                already_in_cart = Cart.objects.filter(Q(order=order) & Q(product=product)).exists()
                if already_in_cart:
                    return JsonResponse({'message': 'ALREADY_IN_CART'}, status=400)
                
                add_to_cart = Cart(order    = order, 
                                   product  = product, 
                                   quantity = quantity)

                add_to_cart.save()
            else:
                order = Order(user          = user,
                               price        = 0,
                               order_number = str(uuid.uuid1()),
                               order_status = order_status)

                cart = Cart(order    = order,
                            product  = product, 
                            quantity = quantity)

                order.save()
                cart.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except TypeError:
            return JsonResponse({'message': 'TypeError'}, status=400)


class CartListView(View):
    @login_required
    def get(self, request):
        user = request.user
        
        default      = user.address_set.get(is_default=True)
        full_address = str(default.address) + (str(default.detail_address) if default.detail_address else "")
        
        order_status = OrderStatus.objects.get(name="장바구니")
        exist_cart   = Order.objects.filter(Q(user=user) & Q(order_status=order_status)).exists()
        if not exist_cart:
            return JsonResponse({'message': 'EMPTY_CART'}, status=200)

        products_in_cart = Order.objects.get(Q(user=user) & Q(order_status=order_status)).cart_order.all()

        products = [{
                    'id': in_cart.product.id,
                    'name': in_cart.product.name,
                    'price': in_cart.product.price,
                    'discount_rate': in_cart.product.discountrate_set.get(id=in_cart.product.id).discount_rate if in_cart.product.discountrate_set.filter(id=in_cart.product.id).exists() else 0,
                    #'storage_method': in_cart.product.storage_method.name if in_cart.product.storage_method.name != None else "",
                    'quantity': in_cart.quantity
                } for in_cart in products_in_cart
                ]

        return JsonResponse({'address': full_address, 'product': products}, status=200)
        

class OrderView(View):
    @transaction.atomic
    @login_required
    def post(self, request):
        try:
            user          = request.user
            data          = json.loads(request.body)
            total_price   = data['total_price']
            products_list = data['products_list']

            # get cart
            cart    = OrderStatus.objects.get(name="장바구니")
            in_cart = Order.objects.get(Q(user=user) & Q(order_status=cart))

            # create new order
            purchased = OrderStatus.objects.get(name="결제완료")
            new_order = Order(user         = user, 
                              price        = total_price, 
                              order_status = purchased, 
                              order_number = str(uuid.uuid1()) )
            new_order.save()

            for product_info in products_list:
                id       = product_info['id']
                quantity = product_info['quantity']
                product  = Product.objects.get(id=id)
                
                if quantity > product.stock:
                    return JsonResponse({'message': '구매가능수량초과'}, status=400)

                product.stock -= quantity

                product_in_cart = Cart.objects.get(Q(order=in_cart) & Q(product=product))
                product_in_cart.delete()

                make_purchase_list = Cart(order    = new_order, 
                                          product  = product, 
                                          quantity = quantity)
                make_purchase_list.save()

            # 빈 장바구니는 지우기
            products_in_cart = len(in_cart.cart_order.all())
            if not products_in_cart:
                in_cart.delete()

            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)
        
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
