# products/models.py
from django.db import models
from accounts.models import FarmerProfile

class Category(models.Model):
    name  = models.CharField(max_length=50, unique=True)
    emoji = models.CharField(max_length=5, blank=True)
    slug  = models.SlugField(unique=True)

    class Meta:
        db_table      = 'categories'
        verbose_name_plural = 'categories'


class Product(models.Model):
    BADGE  = [('organic','Organic'),('seasonal','Seasonal'),
              ('heritage','Heritage'),('fresh','Fresh')]
    STATUS = [('active','Active'),('out_of_stock','Out of Stock'),
              ('flagged','Flagged')]

    farmer          = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE,
                                        related_name='products')
    category        = models.ForeignKey(Category, on_delete=models.PROTECT,
                                        related_name='products')
    name            = models.CharField(max_length=150)
    description     = models.TextField(blank=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    unit            = models.CharField(max_length=20)
    stock_quantity  = models.IntegerField(default=0)
    badge_type      = models.CharField(max_length=10, choices=BADGE, default='fresh')
    origin_location = models.CharField(max_length=150, blank=True)
    image_url       = models.URLField(max_length=500, blank=True)
    is_active       = models.BooleanField(default=True)
    status          = models.CharField(max_length=15, choices=STATUS, default='active')
    total_sales     = models.IntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        indexes  = [
            models.Index(fields=['category']),
            models.Index(fields=['farmer']),
            models.Index(fields=['status']),
        ]