from django.urls import path
from django.contrib.auth.views import LogoutView,LoginView
from .views import RegisterView

app_name = 'user_management'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]