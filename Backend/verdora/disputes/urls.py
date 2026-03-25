from django.urls import path
from . import views

urlpatterns = [
    path('',          views.DisputeListView.as_view()),
    path('<int:pk>/', views.DisputeDetailView.as_view()),
    path('<int:pk>/resolve/', views.ResolveDisputeView.as_view()),
]
