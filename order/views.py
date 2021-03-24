import uuid
import json

from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse

from user.models     import User, Address
from product.models  import Product
from order.models    import Order, Cart, OrderStatus
from utils.decorator import login_required

# 장바구니에 담기 버튼 눌렀을 때 구현
class AddToCartView(View):
    @login_required
    def get(self, request):
        user     = request.user
        id       = request.GET.get('id')
        quantity = request.GET.get('quantity')

        exist_product = Product.objects.filter(id=id).exists()
        if not exist_product:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=400)
        
        product = Product.objects.get(id=id)

        if int(quantity) > product.stock:
            return JsonResponse({'message': '구매가능수량초과'}, status=400)

        order_status = OrderStatus.objects.get(name="장바구니")
        
        has_cart = Order.objects.filter(Q(user=user) & Q(order_status=order_status)).exists()
        if has_cart:
            order           = Order.objects.get(Q(user=user)&Q(order_status=order_status))
            already_in_cart = Cart.objects.filter(Q(order=order) & Q(product=product)).exists()
            if already_in_cart:
                return JsonResponse({'message': 'ALREADY_IN_CART'}, status=400)
            Cart.objects.create(product=product, order=order, quantity=quantity)
        else:
            create_order = Order.objects.create(user=user, price=0, order_number=str(uuid.uuid1()), order_status=order_status)
            create_cart  = Cart.objects.create(order=create_order, product=product, quantity=quantity)

        return JsonResponse({'message': 'SUCCESS'}, status=200)


# 장바구니를 눌렀을 때, 장바구니에 존재하는 상품 내역들 보여주기
class CartListView(View):
    @login_required
    def get(self, request):
        user = request.user
        
        default_address = user.address_set.get(is_default=True)
        full_address    = str(default_address.address) + str(default_address.detail_address)

        order_status = OrderStatus.objects.get(name="장바구니")
        exist_cart   = Order.objects.filter(Q(user=user) & Q(order_status=order_status)).exists()

        if not exist_cart:
            return JsonResponse({'message': 'EMPTY_CART'}, status=200)

        products_in_cart = Order.objects.get(Q(user=user) & Q(order_status=order_status)).cart_order.all()

        products = []
        products.append( {
                          'id': in_cart.product.id,
                          'name': in_cart.product.name,
                          'price': in_cart.product.price,
                          'discount_rate': in_cart.product.discountrate_set.get(id=in_cart.product.id).discount_rate if in_cart.product.discountrate_set.filter(id=in_cart.product.id).exists() else 0,
                          'storage_method': in_cart.product.storage_method,
                          'quantity': in_cart.quantity
                         } for in_cart in products_in_cart )


        return JsonResponse({'products':products, 'address': full_address}, status=200)

class OrderView(View):
    @login_required
    def post(self, request):
        user          = request.user
        data          = json.loads(request.body)
        purchase_list = data['data']

        # get cart
        cart    = OrderStatus.objects.get(name="장바구니")
        in_cart = Order.objects.get(Q(user=user) & Q(order_status=cart))

        # create new order
        price     = 0
        purchased = OrderStatus.objects.get(name="결제완료")
        new_order = Order.objects.create(user=user, price=price, order_status=purchased, order_number=str(uuid.uuid1()))

        for product_info in purchase_list:
            id       = product_info['id']
            quantity = product_info['quantity']
            product  = Product.objects.get(id=id)
            price   += product.price * quantity

            clear_cart = Cart.objects.get(order=in_cart, product=product).delete()
            make_purchase_list = Cart.objects.create(order=new_order, product=product, quantity=quantity)


        new_order.price = price

        # cart가 비어있는 경우 order에서 order_status=장바구니 인 로우 지우기
        products_in_cart = len(in_cart.cart_order.all())
        if not products_in_cart:
            in_cart.delete()

        return JsonResponse({'message':'SUCCESS'}, status=200)
