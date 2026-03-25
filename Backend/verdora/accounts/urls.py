from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/buyer/',   views.BuyerRegisterView.as_view()),
    path('register/farmer/',  views.FarmerRegisterView.as_view()),
    path('otp/send/',         views.SendOTPView.as_view()),
    path('otp/verify/',       views.VerifyOTPView.as_view()),
    path('login/',            views.LoginView.as_view()),
    # path('logout/',           views.LogoutView.as_view()),
    # path('password/reset/',   views.PasswordResetView.as_view()),
    # # Profiles
    path('profile/buyer/',    views.BuyerProfileView.as_view()),
    path('profile/farmer/',   views.FarmerProfileView.as_view()),
    # # Admin — farmer management
    # path('farmers/',          views.FarmerListView.as_view()),
    # path('farmers/<int:pk>/', views.FarmerDetailView.as_view()),
    # path('farmers/<int:pk>/verify/', views.VerifyFarmerView.as_view()),
    # # Admin — customer management
    # path('customers/',        views.CustomerListView.as_view()),
    # path('customers/<int:pk>/toggle/', views.ToggleCustomerView.as_view()),
]