# orders/models.py
from django.db import models
from accounts.models import User, FarmerProfile
from products.models import Product

class Cart(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='cart_items')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity   = models.SmallIntegerField(default=1)
    added_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table    = 'cart_items'
        unique_together = ('user', 'product')


class Order(models.Model):
    PAYMENT_METHOD = [('upi','UPI'),('card','Card'),
                      ('netbanking','Net Banking'),('cod','Cash on Delivery')]
    PAYMENT_STATUS = [('pending','Pending'),('paid','Paid'),
                      ('failed','Failed'),('refunded','Refunded')]
    STATUS         = [('processing','Processing'),('in_transit','In Transit'),
                      ('delivered','Delivered'),('cancelled','Cancelled'),
                      ('disputed','Disputed')]

    order_ref        = models.CharField(max_length=12, unique=True)
    buyer            = models.ForeignKey(User, on_delete=models.PROTECT,
                                         related_name='orders')
    delivery_address = models.TextField()
    subtotal         = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee     = models.DecimalField(max_digits=6, decimal_places=2, default=40)
    discount         = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_amount     = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method   = models.CharField(max_length=15, choices=PAYMENT_METHOD,
                                        default='upi')
    payment_status   = models.CharField(max_length=10, choices=PAYMENT_STATUS,
                                        default='pending')
    status           = models.CharField(max_length=15, choices=STATUS,
                                        default='processing')
    notes            = models.TextField(blank=True)
    ordered_at       = models.DateTimeField(auto_now_add=True)
    delivered_at     = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'orders'
        indexes  = [
            models.Index(fields=['buyer']),
            models.Index(fields=['status']),
            models.Index(fields=['ordered_at']),
        ]


class OrderItem(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE,
                                    related_name='items')
    product     = models.ForeignKey(Product, on_delete=models.PROTECT)
    farmer      = models.ForeignKey(FarmerProfile, on_delete=models.PROTECT)
    quantity    = models.SmallIntegerField()
    unit_price  = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'