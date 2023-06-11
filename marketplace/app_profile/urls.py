from django.urls import path
from .views import SignUpView, UserLogoutView, AuthView, ProfileDetail, AvatarUpdateView, PasswordUpdateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/sign-up/', SignUpView.as_view(), name='sign-in'),
    path('api/sign-out/', UserLogoutView.as_view(), name='sign-out'),
    path('api/sign-in/', AuthView.as_view(), name='login'),
    path('api/profile/', ProfileDetail.as_view()),
    path('api/profile/avatar/', AvatarUpdateView.as_view(), name='avatar'),
    path('api/profile/password/', PasswordUpdateView.as_view(), name='change_password')
]