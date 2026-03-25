from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.ReviewListView.as_view()),
    path('<int:pk>/',         views.ReviewDetailView.as_view()),
    path('product/<int:pid>/',views.ProductReviewsView.as_view()),
]