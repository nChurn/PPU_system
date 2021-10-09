from django.urls import path, re_path

from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('auth/login', CustomObtainTokenPairView.as_view(), name='login'),
    path('auth/login/refresh', TokenRefreshView.as_view(), name='login_refresh'),
    path('auth/register', CreateAccView.as_view(), name='register'),
    path('test', TestView.as_view(), name='test_auth'),
    path('ppu', CreatePPUView.as_view(), name='create_ppu'), # +
    
    path('ppu/add_file', AddFilePPUView.as_view(), name='add_file'), # +
    path('ppu/list_checking_ppus', ListCheckingPPUs.as_view(), name='list_checking_ppus'),
    re_path('moder/list_ppu', moder_list_ppus, name='moder_list_ppus'),
    path('moder/ppu_answer', moder_answer, name='moder_answer'),
#    path('moder/select_ispol', moder_select_vned, name='select_ispol')
]