from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View

from App.models import Institution, Donation, Category


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
            , 'institutions': institutions, 'organizations': organizations, 'locals': locals,
                                              'institution': institution})


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        category_choices = [(category.id, category.name) for category in categories]
        return render(request, 'form.html', {'categories': categories, 'category_choices': category_choices})

    def post(self, request):
        return render(request, 'form.html')



