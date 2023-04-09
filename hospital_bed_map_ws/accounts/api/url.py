from django.urls import re_path
from .views import LoginView

urlpatterns = [
    re_path('login/', LoginView.as_view())
]