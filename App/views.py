from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate

from django.core.paginator import Paginator
from django.db.models import Sum

from django.shortcuts import render, redirect

from django.views import View
from App.forms import UserForm, PasswordForm
from App.models import Institution, Donation, Category


class LandingPage(View):
    def get(self, request):
        total_bags = Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags']
        supported_organizations = Institution.objects.filter(donation__isnull=False).distinct().count()

        institutions = Institution.objects.filter(type=1).order_by('name')
        paginator = Paginator(institutions, 5)
        page = request.GET.get('page')
        fundations_page = paginator.get_page(page)

        organizations = Institution.objects.filter(type=2).order_by('name')
        paginator = Paginator(organizations, 5)
        page = request.GET.get('page')
        organizations_page = paginator.get_page(page)

        collections = Institution.objects.filter(type=3).order_by('name')
        paginator = Paginator(collections, 5)
        page = request.GET.get('page')
        collections_page = paginator.get_page(page)

        ctx = {'total_bags': total_bags, 'supported_organizations': supported_organizations,
               'institutions': institutions,
               'fundations_page': fundations_page, 'organizations_page': organizations_page,
               'collections_page': collections_page}

        return render(request, 'index.html', ctx)


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        # Pobieramy wszystkie kategorie
        categories = Category.objects.all()

        # Pobieramy wszystkie instytucje
        institutions = Institution.objects.all()

        # Iterujemy przez instytucje i tworzymy ciąg znaków kategorii
        for institution in institutions:
            categories_ids = [str(category.id) for category in institution.category.all()]
            institution.category_string = ', '.join(categories_ids)

        # Przekazujemy kategorie i instytucje do szablonu
        ctx = {'categories': categories, 'institutions': institutions}

        # Renderujemy szablon
        return render(request, 'form.html', ctx)


class Profil(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user)
        non_taken_donations = []
        taken_donations = []
        for donation in donations:
            if donation.is_taken:
                taken_donations.append(donation)
            else:
                non_taken_donations.append(donation)
        ctx = {'user': user, 'donations': donations, 'non_taken_donations': non_taken_donations,
               'taken_donations': taken_donations}
        return render(request, 'profil.html', ctx)

    def post(self, request):
        donation_id = request.POST.get('donation_id')
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = not donation.is_taken
        donation.save()
        return redirect('profile')


class UserEditView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_form = UserForm(instance=request.user)
        password_form = PasswordForm()
        return render(request, 'user_edit.html', {'user_form': user_form, 'password_form': password_form})

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        password_form = PasswordForm(request.POST)

        if password_form.is_valid():
            password = password_form.cleaned_data.get('new_password')
            if password:
                request.user.set_password(password)
                request.user.save()
                messages.success(request, 'Hasło zostało zmienione')
                user = authenticate(username=request.user.username, password=password)
                if user is not None:
                    login(request, user)
                return redirect('user-edit')
            else:
                messages.error(request, 'Nowe hasło nie może być puste')

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Dane zostały zmienione')
            return redirect('user-edit')
        else:
            messages.error(request, 'Wystąpił błąd podczas zmiany danych')

        return render(request, 'user_edit.html', {'user_form': user_form, 'password_form': password_form})
