from django.shortcuts import render
from django.shortcuts import render

# imports
import random, string
from datetime import timedelta
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import OTPToken, User, FarmerProfile, BuyerProfile
from .serializers import BuyerRegisterSerializer, FarmerRegisterSerializer


# ================================
# OTP APIs
# ================================

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email   = request.data.get('email')
        purpose = request.data.get('purpose', 'registration')

        otp = ''.join(random.choices(string.digits, k=6))

        OTPToken.objects.create(
            email=email,
            otp_code=otp,
            purpose=purpose,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        return Response({
            'otp': otp,
            'message': 'OTP generated successfully'
        })


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp   = request.data.get('otp')

        token = OTPToken.objects.filter(
            email=email,
            otp_code=otp,
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()

        if not token:
            return Response({
                'error': 'Invalid or expired OTP'
            }, status=status.HTTP_400_BAD_REQUEST)

        token.is_used = True
        token.save()

        return Response({'verified': True})


# ================================
# REGISTER APIs
# ================================

class BuyerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BuyerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Buyer registered successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)


class FarmerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FarmerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            'message': 'Farmer registration submitted. Waiting for admin approval.'
        }, status=status.HTTP_201_CREATED)


# ================================
# LOGIN / LOGOUT
# ================================

from django.contrib.auth import authenticate

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({'message': 'Logged out successfully'})


# ================================
# PROFILE APIs
# ================================

class BuyerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = BuyerProfile.objects.get(user=request.user)

        data = {
            "name": request.user.first_name + " " + request.user.last_name,
            "email": request.user.email,
            "phone": request.user.phone,
            "city": profile.city,
            "state": profile.state
        }

        return Response(data)


class FarmerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = FarmerProfile.objects.get(user=request.user)

        data = {
            "farm_name": profile.farm_name,
            "owner": request.user.first_name,
            "district": profile.district,
            "state": profile.state,
            "status": profile.verification_status
        }

        return Response(data)


# ================================
# ADMIN APIs
# ================================

class VerifyFarmerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        profile = FarmerProfile.objects.get(pk=pk)

        profile.verification_status = 'active'
        profile.save()

        return Response({
            'message': f'{profile.farm_name} verified successfully'
        })