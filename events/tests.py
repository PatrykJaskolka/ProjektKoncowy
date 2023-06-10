from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from .models import Client, Event
from .views import ClientDetails

class AddClientTestCase(TestCase):
    def test_get(self):
        response = self.client.get(reverse('add_client'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'add-client.html')

    def test_post(self):
        data = {
            'name': 'John',
            'surname': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '123456789',
            'date_of_birth': '1990-01-01',
            'address': '123 Main St, City'
        }
        response = self.client.post(reverse('add_client'), data=data)

        self.assertRedirects(response, reverse('client_list'))

        self.assertTrue(Client.objects.filter(name='John', surname='Doe').exists())


class ClientDetailsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        client = Client.objects.create(name='John', surname='Doe', email='john.doe@example.com', date_of_birth='1990-01-01')
        url = reverse('client_details', args=[client.pk])
        request = self.factory.get(url)
        response = ClientDetails.as_view()(request, pk=client.pk)

        self.assertIn(b'client', response.content)
        self.assertIn(b'events', response.content)

        self.assertIn(bytes(client.name, 'utf-8'), response.content)