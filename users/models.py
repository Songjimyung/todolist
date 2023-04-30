from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일만 입력가능')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    age = models.IntegerField()
    introduction = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    refresh_token = models.TextField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'gender', 'age']

    def __str__(self):
        return self.email
    
    def update(self, validated_data):
        # 이메일, 이름, 성별, 나이, 자기소개 수정 가능
        self.email = validated_data.get('email', self.email)
        self.name = validated_data.get('name', self.name)
        self.gender = validated_data.get('gender', self.gender)
        self.age = validated_data.get('age', self.age)
        self.introduction = validated_data.get('introduction', self.introduction)

        # 비밀번호 수정시에만 set_password() 호출
        password = validated_data.get('password', None)
        if password is not None:
            self.set_password(password)

        # refresh_token 업데이트
        refresh_token = RefreshToken.for_user(self)
        self.refresh_token = str(refresh_token)
        self.save()

        return self