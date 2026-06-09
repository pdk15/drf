from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    UserRegisterApi,
    UserProfileApi,
    UserChangePasswordApi,
    SendPasswordResetEmailApi,
    UserPasswordResetApi,
    UserLoginApi,   
    # profile_page,
    # get_product,
    # create_product,
    # product_detail,
    UserProfileApi,
    ProductViewSet,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('register/', UserRegisterApi.as_view(), name='register'),
    path('login/', UserLoginApi.as_view(), name='login'),
    path('profile/', UserProfileApi.as_view(), name='profile'),
    path('change-password/', UserChangePasswordApi.as_view(), name='change-password'),
    path('send-reset-password-email/', SendPasswordResetEmailApi.as_view(), name='send-reset-password-email'),
    path('reset/<uid>/<token>/', UserPasswordResetApi.as_view(), name='reset-password'),

    # Old function-based product APIs
    # path('get-product/', get_product, name='get_product'),
    # path('create-product/', create_product, name='create_product'),
    # path('product/<int:pk>/', product_detail, name='product-detail'),

    # ViewSet URLs
    path('', include(router.urls)),
]