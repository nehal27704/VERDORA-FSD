# disputes/models.py
from django.db import models
from accounts.models import User, FarmerProfile
from orders.models import Order

class Dispute(models.Model):
    RESOLUTION = [('refund','Refund to Customer'),('resend','Resend Product'),
                  ('dismissed','Dismissed'),('penalty','Penalty to Farmer')]
    STATUS     = [('open','Open'),('resolved','Resolved')]

    dispute_ref = models.CharField(max_length=8, unique=True)
    order       = models.ForeignKey(Order, on_delete=models.PROTECT,
                                    related_name='disputes')
    raised_by   = models.ForeignKey(User, on_delete=models.PROTECT,
                                    related_name='disputes_raised')
    farmer      = models.ForeignKey(FarmerProfile, on_delete=models.PROTECT,
                                    related_name='disputes')
    issue       = models.TextField()
    resolution  = models.CharField(max_length=15, choices=RESOLUTION,
                                   null=True, blank=True)
    notes       = models.TextField(blank=True)
    status      = models.CharField(max_length=10, choices=STATUS, default='open')
    raised_at   = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'disputes'


# reviews/models.py
from django.db import models
from accounts.models import User
from products.models import Product
from orders.models import Order

class Review(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='reviews')
    user       = models.ForeignKey(User, on_delete=models.PROTECT,
                                   related_name='reviews')
    order      = models.ForeignKey(Order, on_delete=models.PROTECT)
    rating     = models.SmallIntegerField()          # 1–5
    comment    = models.TextField(blank=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'reviews'
        unique_together = ('user', 'product', 'order')


# notifications/models.py
from django.db import models
from accounts.models import User

class Notification(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE,
                                   null=True, blank=True,
                                   related_name='notifications')
    message    = models.TextField()
    color      = models.CharField(max_length=7, default='#43a047')
    is_read    = models.BooleanField(default=False)
    link_type  = models.CharField(max_length=50, blank=True)
    link_id    = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        indexes  = [models.Index(fields=['user','is_read'])]


# orders/payout_model.py  (add to orders/models.py)
class Payout(models.Model):
    STATUS = [('pending','Pending'),('processing','Processing'),
              ('completed','Completed'),('failed','Failed')]

    txn_ref      = models.CharField(max_length=12, unique=True)
    farmer       = models.ForeignKey(FarmerProfile, on_delete=models.PROTECT,
                                     related_name='payouts')
    amount       = models.DecimalField(max_digits=12, decimal_places=2)
    status       = models.CharField(max_length=15, choices=STATUS, default='pending')
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payouts'