"""
URL configuration for verdora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Simple home view for root URL
def home(request):
    return HttpResponse("Welcome to Verdora API! Use /api/auth/ or /api/products/")

urlpatterns = [
    path('', home, name='home'),  # Root URL
    # path('admin/', admin.site.urls),  # Admin can be uncommented if needed

    path('api/auth/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    # Uncomment below APIs when ready
    # path('api/orders/', include('orders.urls')),
    # path('api/disputes/', include('disputes.urls')),
    # path('api/reviews/', include('reviews.urls')),
    # path('api/notifications/', include('notifications.urls')),
    # path('api/admin/', include('analytics.urls')),
]
