from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('landingpage')
        return render(request, 'register.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landingpage')


class RegisterPage(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.method == "POST":
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password != password2:
                messages.error('Hasła nie są takie same. ')
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Użytkownik o podanym adresie email już istnieje.')
                return redirect('register')

            user = User.objects.create_user(username=email, email=email, password=password, first_name=name,
                                            last_name=surname)
            user.save()
            messages.success(request, "Konto zostało pomyślnie utworzone. Zaloguj się.")
            return redirect('login')

        return render(request, 'register.html')
