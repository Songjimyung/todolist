from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    #직렬화 될 때 포함되지 않도록!
    class Meta:
        model = User
        fields = "__all__"
# create_user 함수를 이용하면 password 따로 해시해줄 필요 없음 + user.save() 불필요       
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            age=validated_data['age'],
            introduction=validated_data.get('introduction', ''),
        )
        refresh_token = RefreshToken.for_user(user)
        user.refresh_token = str(refresh_token)
        user.save()
        return user
# 회원정보 수정 serializer required를 false로 줘서 개별로 수정가능하게
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'gender', 'age', 'introduction']
        read_only_fields = ['email']
        extra_kwargs = {
            'name': {'required': False},
            'gender': {'required': False},
            'age': {'required': False},
            'introduction': {'required': False},
        }
    def update(self, instance, validated_data):
        return instance.update(validated_data)
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['name'] = user.name
        token['gender'] = user.gender
        token['age'] = user.age  
        return token
    
