# accounts/serializers.py
from rest_framework import serializers
from .models import User, BuyerProfile, FarmerProfile

class BuyerRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name  = serializers.CharField()
    email      = serializers.EmailField()
    phone      = serializers.CharField(max_length=10)
    password   = serializers.CharField(write_only=True, min_length=8)
    address    = serializers.CharField()
    city       = serializers.CharField()
    pincode    = serializers.CharField(max_length=6)
    state      = serializers.CharField()
    interests  = serializers.ListField(child=serializers.CharField(), required=False)
    newsletter_opt = serializers.BooleanField(default=True)

    # ✅ ADD THIS
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, data):
        user = User.objects.create_user(
            email=data['email'], phone=data['phone'],
            password=data['password'], role='buyer',
            first_name=data['first_name'], last_name=data['last_name'],
        )
        BuyerProfile.objects.create(
            user=user, address=data.get('address',''),
            city=data.get('city',''), pincode=data.get('pincode',''),
            state=data.get('state',''),
            interests=data.get('interests',[]),
            newsletter_opt=data.get('newsletter_opt', True),
        )
        return user

class FarmerRegisterSerializer(serializers.Serializer):
    # Step 1 fields
    first_name  = serializers.CharField()
    last_name   = serializers.CharField()
    email       = serializers.EmailField()
    phone       = serializers.CharField(max_length=10)
    aadhaar     = serializers.CharField(max_length=12)
    password    = serializers.CharField(write_only=True, min_length=8)

    # Step 2 fields
    farm_name        = serializers.CharField()
    village          = serializers.CharField()
    district         = serializers.CharField()
    state            = serializers.CharField()
    pincode          = serializers.CharField(max_length=6)
    land_area_acres  = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)
    experience_yrs   = serializers.IntegerField(required=False)
    crop_categories  = serializers.ListField(child=serializers.CharField())
    organic_status   = serializers.ChoiceField(
        choices=['certified','transition','conventional']
    )
    bank_account     = serializers.CharField()
    ifsc_code        = serializers.CharField(max_length=11)

    # ✅ ADD THIS (IMPORTANT)
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    # ✅ OPTIONAL (better validation)
    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Invalid phone number")
        return value

    def validate_aadhaar(self, value):
        if not value.isdigit() or len(value) != 12:
            raise serializers.ValidationError("Invalid Aadhaar number")
        return value

    def create(self, data):
        user = User.objects.create_user(
            email=data['email'],
            phone=data['phone'],
            password=data['password'],
            role='farmer',
            first_name=data['first_name'],
            last_name=data['last_name'],
        )

        FarmerProfile.objects.create(
            user=user,
            farm_name=data['farm_name'],
            village=data.get('village', ''),
            district=data.get('district', ''),
            state=data.get('state', ''),
            pincode=data.get('pincode', ''),
            land_area_acres=data.get('land_area_acres'),
            experience_yrs=data.get('experience_yrs'),
            aadhaar_number=data.get('aadhaar', ''),
            bank_account=data['bank_account'],
            ifsc_code=data['ifsc_code'],
            organic_status=data['organic_status'],
            crop_categories=data['crop_categories'],
        )

        return user