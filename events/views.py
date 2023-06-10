from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from .models import Event, Client, Place, Category, Accessories, Subcontractor, Subcontractor_service, Oferta
from django.views.generic import CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import *

class IndexView(View):
    """
    Wyświetla podstawową stronę "base.html".
    """
    def get(self,request):
        return render(request, 'base.html')

class Dashboard(View):
    """
    Wyświetla panel nawigacyjny z nadchodzącymi wydarzeniami.
    """
    def get(self, request):
        upcoming_events = Event.objects.filter(term__gte=timezone.now()).order_by('term')[:5]
        ctx = {
            'upcoming_events': upcoming_events
        }
        return render(request, "dashboard.html", ctx)

class AddClient(View):
    """
    Obsługuje dodawanie nowego klienta.
    """
    def get(self, request):
        return render(request, "add-client.html")

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')

        new_client = Client(name=name, surname=surname, email=email, phone_number=phone_number, date_of_birth=date_of_birth, address=address)
        new_client.save()

        return redirect('client_list')

class AddEvent(View):
    """
    Obsługuje dodawanie nowego wydarzenia.
    """

    def get(self, request):
        clients = Client.objects.all()
        places = Place.objects.all()
        categories = Category.CATEGORIES
        accessories = Accessories.objects.all()
        ctx = {
            'clients': clients,
            'places' : places,
            'categories': categories,
            'accessories': accessories
        }
        return render(request, 'add-event.html', ctx)

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        term = request.POST.get('term')
        budget = request.POST.get('budget')
        number_of_people = request.POST.get('number_of_people')
        category_id = request.POST.get('category')
        client_id = request.POST.get('client')
        place_id = request.POST.get('place')
        accesories_ids = request.POST.getlist('accessories')

        client = Client.objects.get(pk=client_id)
        place = Place.objects.get(pk=place_id)
        category = Category.objects.get_or_create(category_name=category_id)[0]

        new_event = Event(name=name, description=description, term=term, budget=budget, number_of_people=number_of_people, client=client, place=place, category=category)
        new_event.save()

        new_event.accessories.set(accesories_ids)

        return redirect('event_list')

class ClientDetails(View):
    """
    Wyświetla szczegóły klienta i powiązane z nim wydarzenia.
    """
    def get(self, request, pk):
        client = Client.objects.get(pk=pk)
        events = client.event_set.all()
        ctx = {
            'client': client,
            'events': events
        }
        return render(request, 'client-details.html', ctx)

class EventDetails(View):
    """
    Wyświetla szczegóły wydarzenia.
    """
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        ctx = {
            'event': event
        }

        return render(request, 'event-details.html', ctx)

class ClientList(View):
    """
    Wyświetla listę wszystkich klientów.
    """
    def get(self, request):
        clients = Client.objects.all()
        ctx = {
            'clients': clients
        }
        return render(request, 'clients.html', ctx)

class EventList(View):
    """
    Wyświetla listę wszystkich wydarzeń.
    """
    def get(self, request):
        events = Event.objects.all()
        ctx = {
            'events': events
        }
        return render(request, 'events.html', ctx)

class AddSubcontractor(View):
    """
    Obsługuje dodawanie nowego podwykonawcy.
    """
    def get(self, request):
        return render(request, 'add-subcontractor.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        services = request.POST.getlist('service[]')
        prices_per_person = request.POST.getlist('price_per_person[]')
        prices_fixed = request.POST.getlist('price_fixed[]')

        subcontractor = Subcontractor.objects.create(name=name, description=description)

        for service, price_per_person, price_fixed in zip(services, prices_per_person, prices_fixed):
            if service and (price_per_person or price_fixed):
                Subcontractor_service.objects.create(
                    subcontractor=subcontractor,
                    service=service,
                    price_per_person=price_per_person if price_per_person else 0,
                    price_fixed=price_fixed if price_fixed else 0
                )

        return redirect('subcontractor_list')

class SubcontractorDetails(View):
    """
    Wyświetla szczegóły podwykonawcy i powiązane z nim usługi.
    """
    def get(self, request, pk):
        subcontractor = Subcontractor.objects.get(pk=pk)
        services = subcontractor.subcontractor_service_set.all()
        ctx = {
            'subcontractor': subcontractor,
            'services': services

        }
        return render(request, 'subcontractor-details.html', ctx)

class SubcontractorsList(View):
    """
    Wyświetla listę wszystkich podwykonawców.
    """
    def get(self, request):
        subcontractors = Subcontractor.objects.all()
        ctx = {
            'subcontractors': subcontractors
        }
        return render(request, 'subcontractors.html', ctx)

class SubcontractorModify(View):
    """
    Obsługuje modyfikację podwykonawcy.
    """
    def get(self, request, pk):
        try:
            subcontractor = Subcontractor.objects.get(pk=pk)
            services = Subcontractor_service.objects.filter(subcontractor=subcontractor)
        except Subcontractor.DoesNotExist:
            return HttpResponseNotFound('404 - Page not found')
        return render(request, 'subcontractor-modify.html', {'subcontractor': subcontractor, 'services': services})

    def post(self, request, pk):
        try:
            subcontractor = Subcontractor.objects.get(pk=pk)
        except Subcontractor.DoesNotExist:
            return HttpResponseNotFound('404 - Page not found')

        name = request.POST.get('name')
        description = request.POST.get('description')
        services = request.POST.getlist('service[]')
        prices_per_person = request.POST.getlist('price_per_person[]')
        prices_fixed = request.POST.getlist('price_fixed[]')

        subcontractor.name = name
        subcontractor.description = description
        subcontractor.save()

        # Usuwanie istniejących usług
        Subcontractor_service.objects.filter(subcontractor=subcontractor).delete()

        # Dodawanie nowych/usuniętych usług
        for service, price_per_person, price_fixed in zip(services, prices_per_person, prices_fixed):
            if service and (price_per_person or price_fixed):
                Subcontractor_service.objects.create(
                    subcontractor=subcontractor,
                    service=service,
                    price_per_person=price_per_person if price_per_person else 0,
                    price_fixed=price_fixed if price_fixed else 0
                )

        return redirect('subcontractor_details', pk=pk)

class ClientModify(View):
    """
    Obsługuje modyfikację klienta.
    """
    def get(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return HttpResponseNotFound('404 - Page not found')
        return render(request, 'client-modify.html', {'client': client})

    def post(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return HttpResponseNotFound('404 - Page not found')

        client.name = request.POST.get('name')
        client.surname = request.POST.get('surname')
        client.email = request.POST.get('email')
        client.phone_number = request.POST.get('phone_number')
        client.date_of_birth = request.POST.get('date_of_birth')
        client.address = request.POST.get('address')
        client.save()

        return redirect('client_details', pk=pk)

class EventModify(View):
    """
    Obsługuje modyfikację wydarzenia.
    """
    def get(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        places = Place.objects.all()
        clients = Client.objects.all()
        categories = Category.CATEGORIES
        accessories = Accessories.objects.all()

        return render(request, 'event-modify.html', {'event': event, 'places': places, 'clients': clients,
                                                     'categories': categories, 'accessories': accessories})

    def post(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        event.name = request.POST.get('name')
        event.description = request.POST.get('description')
        event.place_id = request.POST.get('place')
        event.term = request.POST.get('term')
        event.budget = request.POST.get('budget')
        event.client_id = request.POST.get('client')
        event.number_of_people = request.POST.get('number_of_people')

        category_id = request.POST.get('category')
        category = Category.objects.get_or_create(category_name=category_id)[0]
        event.category = category

        event.accessories.clear()

        accessories_ids = request.POST.getlist('accessories')

        for accessory_id in accessories_ids:
            accessory = Accessories.objects.get(pk=accessory_id)
            event.accessories.add(accessory)

        event.save()

        return redirect('event_details', pk=event_id)

class DeleteClient(View):
    """
    Obsługuje usuwanie klienta.
    """
    def post(self, request, client_id):
        client = Client.objects.get(pk=client_id)
        client.delete()
        return redirect('client_list')

class DeleteEvent(View):
    """
    Obsługuje usuwanie wydarzenia.
    """
    def post(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        event.delete()
        return redirect('event_list')

class DeleteSubcontractor(View):
    """
    Obsługuje usuwanie podwykonawcy.
    """
    def post(self, request, subcontractor_id):
        subcontractor = Subcontractor.objects.get(pk=subcontractor_id)
        subcontractor.delete()
        return redirect('subcontractor_list')

class AddOferta(View):
    """
    Obsługuje dodawanie nowej oferty dla wydarzenia.
    """
    def get(self, request):
        events = Event.objects.all()
        subcontractor_services = Subcontractor_service.objects.all()
        accessories = Accessories.objects.all()
        ctx = {
            'events': events,
            'subcontractor_services': subcontractor_services,
            'accessories': accessories
        }

        return render(request, 'add-oferta.html', ctx)

    def post(self, request):
        event_id = request.POST.get('event')
        subcontractor_services_ids = request.POST.getlist('subcontractor_services')
        accessories_ids = request.POST.getlist('accessories')
        discount = request.POST.get('discount')
        notes = request.POST.get('notes')
        status = request.POST.get('status')

        subcontractor_services = Subcontractor_service.objects.filter(pk__in=subcontractor_services_ids)
        accessories = Accessories.objects.filter(pk__in=accessories_ids)
        event = Event.objects.get(pk=event_id)

        new_oferta = Oferta(event=event, discount=discount, notes=notes, status=status)
        new_oferta.save()
        new_oferta.subcontractor_services.set(subcontractor_services)
        new_oferta.accessories.set(accessories)

        return redirect('event_list')


class OfertaDetails(View):
    """
    Wyświetla szczegóły oferty.
    """
    def get(self, request, oferta_id):
        oferta = get_object_or_404(Oferta, pk=oferta_id)
        total_price = oferta.calculate_total_price()

        ctx = {
            'oferta': oferta,
            'total_price': total_price
        }
        return render(request, 'oferta-details.html', ctx)

class OfferList(View):
    """
    Wyświetla listę wszystkich ofert.
    """
    def get(self, request):
        offers = Oferta.objects.all()
        ctx = {
            'offers': offers
        }
        return render(request, 'offers.html', ctx)



class UsersView(View):
    """
    Wyświetla listę użytkowników.
    """
    def get(self, request):
        users = User.objects.order_by('username')
        ctx = {
            'users': users
        }
        return render(request, 'users.html', ctx)


class LoginView(FormView):
    """
    Obsługuje proces logowania użytkownika.
    """
    form_class = LoginForm
    success_url = reverse_lazy('profile')
    template_name = 'login.html'

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super().form_valid(form)


class LogoutView(View):
    """
    Obsługuje wylogowanie użytkownika.
    """
    def get(self, request):
        logout(request)
        return redirect('index')


class CreateUserView(FormView):
    """
    Obsługuje tworzenie nowego użytkownika.
    """
    form_class = UserForm
    success_url = reverse_lazy('list_users')
    template_name = 'user_form.html'

    def form_valid(self, form):
        User.objects.create_user(
            username=form.cleaned_data['user_name'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email']
        )
        return super().form_valid(form)


def profile_view(request):
    """
    Wyświetla stronę profilu użytkownika.
    """
    user = request.user
    return render(request, 'profile.html', {'user': user})

