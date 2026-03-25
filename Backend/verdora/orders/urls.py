from django.urls import path
from . import views

urlpatterns = [
    path('cart/',             views.CartView.as_view()),           # GET, POST, DELETE
    path('cart/<int:pk>/',    views.CartItemView.as_view()),       # PATCH, DELETE
    path('checkout/',         views.CheckoutView.as_view()),       # POST → creates order
    path('',                  views.OrderListView.as_view()),      # buyer: own orders, admin: all
    path('<int:pk>/',         views.OrderDetailView.as_view()),
    path('<int:pk>/status/',  views.UpdateOrderStatusView.as_view()),
    path('payouts/',          views.PayoutListView.as_view()),     # admin
]