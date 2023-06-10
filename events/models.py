from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
class Client(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)

class Place(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

class Category(models.Model):
    CATEGORIES = (
        (1, 'Urodziny'),
        (2, 'Wieczor kawalerski'),
        (3, 'Wieczor panienski'),
        (4, 'Wesele'),
        (5, 'Chrzciny'),
        (6, 'Komunia'),
        (7, 'Stodniowka'),
        (8, 'Jubileusz'),
        (9, 'Sylwester'),
    )
    category_name = models.IntegerField(choices=CATEGORIES)

class Accessories(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_fixed = models.DecimalField(max_digits=10, decimal_places=2, default=0)



class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    place = models.ForeignKey(Place, default=None, on_delete=models.CASCADE)
    term = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, default=None, on_delete=models.CASCADE)
    number_of_people = models.PositiveIntegerField()
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
    accessories = models.ManyToManyField(Accessories)

class Subcontractor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Subcontractor_service(models.Model):
    subcontractor = models.ForeignKey(Subcontractor, default=None, on_delete=models.CASCADE)
    service = models.CharField(max_length=255)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_fixed = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Oferta(models.Model):
    STATUS_CHOICES = (
        ('Oczekujące', 'Oczekujące'),
        ('Zatwierdzone', 'Zatwierdzone'),
        ('Anulowane', 'Anulowane'),
    )

    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    subcontractor_services = models.ManyToManyField(Subcontractor_service)
    accessories = models.ManyToManyField(Accessories)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Oczekujące')
    creation_date = models.DateTimeField(default=datetime.now)

    def calculate_total_price(self):
        subtotal_services_per_person = sum(service.price_per_person * self.event.number_of_people for service in self.subcontractor_services.all())
        subtotal_services_fixed = sum(service.price_fixed for service in self.subcontractor_services.all())
        subtotal_accessories_per_person = sum(accessory.price_per_person * self.event.number_of_people for accessory in self.accessories.all())
        subtotal_accessories_fixed = sum(accessory.price_fixed for accessory in self.accessories.all())

        total_price = subtotal_services_per_person + subtotal_services_fixed + subtotal_accessories_per_person + subtotal_accessories_fixed
        if self.discount is not None:
            total_price -= self.discount
        return total_price

    def get_event_category(self):
        return self.event.category.get_category_name_display()

    def get_subcontractor_list(self):
        return self.subcontractor_services.values_list('subcontractor__name', flat=True)

    def get_short_description(self):
        return self.event.description[:100] + '...' if len(self.event.description) > 100 else self.event.description


