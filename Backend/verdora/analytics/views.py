from django.shortcuts import render

# analytics/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from orders.models import Order, OrderItem
from accounts.models import FarmerProfile, User
from disputes.models import Review

class OverviewView(APIView):
    def get(self, request):
        return Response({
            'total_revenue':  OrderItem.objects.aggregate(
                                  t=Sum('total_price'))['t'] or 0,
            'total_orders':   Order.objects.count(),
            'pending_orders': Order.objects.filter(status='processing').count(),
            'total_farmers':  FarmerProfile.objects.count(),
            'pending_farmers':FarmerProfile.objects.filter(
                                  verification_status='pending').count(),
            'total_customers':User.objects.filter(role='buyer').count(),
            'avg_rating':     Review.objects.aggregate(a=Avg('rating'))['a'] or 0,
            'open_disputes':  Dispute.objects.filter(status='open').count(),
        })