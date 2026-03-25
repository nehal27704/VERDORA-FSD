from django.shortcuts import render

# orders/views.py  (checkout logic)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, Order, OrderItem
from products.models import Product
import uuid, random

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user  = request.user
        items = Cart.objects.filter(user=user).select_related('product__farmer')
        if not items.exists():
            return Response({'error': 'Cart is empty'}, status=400)

        subtotal = sum(i.product.price * i.quantity for i in items)
        delivery = 0 if subtotal >= 499 else 40
        total    = subtotal + delivery

        order = Order.objects.create(
            order_ref        = f'#{random.randint(80000,99999)}',
            buyer            = user,
            delivery_address = request.data.get('address', ''),
            subtotal         = subtotal,
            delivery_fee     = delivery,
            total_amount     = total,
            payment_method   = request.data.get('payment_method','upi'),
        )
        for item in items:
            OrderItem.objects.create(
                order=order, product=item.product,
                farmer=item.product.farmer,
                quantity=item.quantity,
                unit_price=item.product.price,
                total_price=item.product.price * item.quantity,
            )
            # Decrement stock
            Product.objects.filter(pk=item.product.pk).update(
                stock_quantity=item.product.stock_quantity - item.quantity,
                total_sales=item.product.total_sales + item.quantity,
            )
        items.delete()  # clear cart
        return Response({'order_id': order.id, 'order_ref': order.order_ref,
                         'total': str(total)}, status=201)