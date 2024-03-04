from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from App.models import Institution, Donation


class LandingPage(View):
    def get(self, request):
        bags_count = Donation.objects.count()
        organizations_count = Institution.objects.count()
        institutions = Institution.objects.filter(type=Institution.FUNDACJA)
        organizations = Institution.objects.filter(type=Institution.ORGANIZACJA_POZARZĄDOWA)
        locals = Donation.objects.all()

        paginator = Paginator(Institution.objects.filter(type=Institution.FUNDACJA), 5)
        page = request.GET.get('page')
        institution = paginator.get_page(page)

        return render(request, 'index.html', {'bags_count': bags_count, 'organizations_count': organizations_count
            , 'institutions': institutions, 'organizations': organizations, 'locals': locals, 'institution': institution})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterPage(View):
    def get(self, request):
        return render(request, 'register.html')
