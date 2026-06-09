from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User , Product
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer , UserLoginSerializer , UserProfileSerializer  , UserChangePasswordSerializer , SendPasswordResetEmailSerializer , UserPasswordResetSerializer , ProductSerializer
from django.contrib.auth import authenticate
from api.renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework import viewsets

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegisterApi(APIView):
    renderer_classes = [ UserRenderer ]
    def post(self , request):
        serializer = UserRegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        token = get_tokens_for_user(user)            
        return Response({'msg':"User Registered successfully" , 'tokens': token} , status = status.HTTP_201_CREATED)

class UserLoginApi(APIView):
    renderer_classes = [ UserRenderer ]
    def post(self , request):
        serializer = UserLoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email , password=password)
        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({'message':"Login Successfull", 'tokens': tokens} , status = status.HTTP_200_OK) 
        return Response({'message':"Invalid Credentials"} , status = status.HTTP_401_UNAUTHORIZED)

class UserProfileApi(APIView):
    renderer_classes = [ UserRenderer ]
    permission_classes = [ IsAuthenticated ]
    def get(self , request):
        user = request.user
        serializer = UserProfileSerializer(instance=user)
        return Response(serializer.data , status = status.HTTP_200_OK)

class UserChangePasswordApi(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [ IsAuthenticated ]
    def post(self , request):
        serializer = UserChangePasswordSerializer(data = request.data , context={'user':request.user})
        serializer.is_valid(raise_exception = True)
        return Response({'msg':"Password Changed Successfully"} , status = status.HTTP_200_OK)
    
class SendPasswordResetEmailApi(APIView):
    renderer_classes = [UserRenderer]
    def post(self , request ):
        serializer = SendPasswordResetEmailSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response({'msg':"Password Reset Link Sent. Please Check Your Email"} , status = status.HTTP_200_OK)
    

class UserPasswordResetApi(APIView):
    renderer_classes = [UserRenderer]
    def post(self ,request, uid , token ):
        serializer = UserPasswordResetSerializer(data = request.data , context={'uid':uid , 'token':token})
        serializer.is_valid(raise_exception = True)
        return Response({'msg':"Password Reset Successfully"} , status = status.HTTP_200_OK)
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# @api_view(['POST'])
# def create_product(request):
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data , status = status.HTTP_201_CREATED)
#     return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_product(request):
#     prod = Product.objects.all()
#     serializer = ProductSerializer(prod, many=True)
#     return Response(serializer.data)

# @api_view(['GET' , 'PUT' , 'DELETE'])
# def product_detail(request , pk):
#     try:
#         product = Product.objects.get(id=pk)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product , data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)
    