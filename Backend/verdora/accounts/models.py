# accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password, role='buyer', **extra):
        email = self.normalize_email(email)
        user  = self.model(email=email, phone=phone, role=role, **extra)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password, **extra):
        return self.create_user(email, phone, password, role='admin',
                                is_staff=True, is_superuser=True, **extra)

class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [('buyer','Buyer'), ('farmer','Farmer'), ('admin','Admin')]

    email       = models.EmailField(unique=True)
    phone       = models.CharField(max_length=15, unique=True)
    first_name  = models.CharField(max_length=80)
    last_name   = models.CharField(max_length=80)
    role        = models.CharField(max_length=10, choices=ROLES, default='buyer')
    avatar      = models.CharField(max_length=10, default='🧑‍🍳')
    is_active   = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name']
    objects = UserManager()

    class Meta:
        db_table = 'users'


class BuyerProfile(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE,
                                          related_name='buyer_profile')
    address        = models.CharField(max_length=255, blank=True)
    city           = models.CharField(max_length=100, blank=True)
    state          = models.CharField(max_length=100, blank=True)
    pincode        = models.CharField(max_length=6, blank=True)
    newsletter_opt = models.BooleanField(default=True)
    interests      = models.JSONField(default=list)
    loyalty_points = models.IntegerField(default=0)

    class Meta:
        db_table = 'buyer_profiles'


class FarmerProfile(models.Model):
    ORGANIC = [('certified','Certified'),('transition','In Transition'),
               ('conventional','Conventional')]
    VERIFY  = [('pending','Pending'),('active','Active'),('suspended','Suspended')]

    user               = models.OneToOneField(User, on_delete=models.CASCADE,
                                              related_name='farmer_profile')
    farm_name          = models.CharField(max_length=150)
    village            = models.CharField(max_length=100, blank=True)
    district           = models.CharField(max_length=100, blank=True)
    state              = models.CharField(max_length=100, blank=True)
    pincode            = models.CharField(max_length=6, blank=True)
    land_area_acres    = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    experience_yrs     = models.SmallIntegerField(null=True)
    aadhaar_number     = models.CharField(max_length=12, blank=True)   # hash in prod
    bank_account       = models.CharField(max_length=20, blank=True)
    ifsc_code          = models.CharField(max_length=11, blank=True)
    organic_status     = models.CharField(max_length=15, choices=ORGANIC,
                                          default='conventional')
    crop_categories    = models.JSONField(default=list)
    verification_status= models.CharField(max_length=15, choices=VERIFY,
                                          default='pending')
    total_earnings     = models.DecimalField(max_digits=12, decimal_places=2,
                                             default=0)

    class Meta:
        db_table = 'farmer_profiles'


class OTPToken(models.Model):
    PURPOSE = [('registration','Registration'),('login','Login'),
               ('password_reset','Password Reset')]

    email      = models.EmailField()
    otp_code   = models.CharField(max_length=6)
    purpose    = models.CharField(max_length=20, choices=PURPOSE)
    is_used    = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'otp_tokens'
        indexes  = [models.Index(fields=['email','purpose'])]