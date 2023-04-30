from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from datetime import datetime

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'refresh_token': str(refresh_token),
                'access_token': str(refresh_token.access_token)
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# class UserLogoutView(APIView):
#     authentication_classes = [JWTAuthentication]
    
#     def post(self, request):
#         user = request.user
#         token = AccessToken(request.headers.get('Authorization').split(' ')[1])
#         token.blacklist_token()
#         for refresh_token in RefreshToken.objects.filter(user=user):
#             refresh_token.blacklist()
#         return Response({"message":"로그아웃되었습니다."}, status=status.HTTP_200_OK)

#토큰방식 로그아웃// 제대로 안됬으니 다시 해보기

# class UserLogoutView(APIView):
#     authentication_classes = [JWTAuthentication]

#     def post(self, request):
#         user = request.user
#         refresh_token = user.refresh_token
#         print(refresh_token)
#         try:
#             # request에서 access_token을 추출합니다.
#             access_token = request.headers.get('Authorization').split(' ')[1]

#             # access_token을 파싱하여 토큰 객체를 생성합니다.
#             _, token = self.authentication_classes[0]().authenticate_credentials(access_token)

#             # access_token의 만료시간을 현재 시간으로 변경하여 저장합니다.
#             token['exp'] = datetime.utcnow()
#             token.set_jti()
#             refreshtoken = RefreshToken(refresh_token)
#             refreshtoken.blacklist
#             # access_token 시간 만료
#             return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)