from django.urls import path
from . import views

urlpatterns = [
    path('overview/',    views.OverviewView.as_view()),     # KPIs
    path('revenue/',     views.RevenueView.as_view()),      # chart data
    path('top-farmers/', views.TopFarmersView.as_view()),
    path('top-products/',views.TopProductsView.as_view()),
    path('geo-sales/',   views.GeoSalesView.as_view()),
]