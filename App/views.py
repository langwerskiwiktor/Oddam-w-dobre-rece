from django.shortcuts import render
from django.views import View

from App.models import Institution, Donation


class LandingPage(View):
    def get(self, request):
        bags_count = Donation.objects.count()
        organizations_count = Institution.objects.count()
        return render(request, 'index.html', {'bags_count': bags_count, 'organizations_count':organizations_count})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterPage(View):
    def get(self, request):
        return render(request, 'register.html')
