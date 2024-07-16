from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
class RegisterView(View):
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'login.html', {'error': 'Username already exists'})
        
        elif User.objects.filter(email=email).exists():
            return render(request, 'login.html', {'error': 'Email already exists'})        
        
        # Create user

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Log the user in after registration
        user = authenticate(username=username, password=password1)
        login(request, user)

        # Redirect to a success page or login page
        return redirect(reverse('user_management:login'))  # Redirect to login page after successful registration