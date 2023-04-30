from django.urls import re_path, path
from .views import LoginView, RefreshTokenView

urlpatterns = [
    re_path('login/', LoginView.as_view()),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]