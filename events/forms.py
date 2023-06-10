from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=150, label='Nazwa użytkownika')
    password = forms.CharField(
        max_length=150,
        label='Hasło',
        widget=forms.PasswordInput()
    )

    def clean(self):
        data = super().clean()
        u = authenticate(username=data['user_name'], password=data['password'])
        if u is None:
            raise forms.ValidationError('Nieprawidłowa nazwa użytkownika lub hasło')
        else:
            data['user'] = u
        return data


class UserForm(forms.Form):
    user_name = forms.CharField(max_length=150, label='Nazwa użytkownika')
    password = forms.CharField(
        max_length=150,
        label='Hasło',
        widget=forms.PasswordInput()
    )
    password_rep = forms.CharField(
        max_length=150,
        label='Hasło ponownie',
        widget=forms.PasswordInput()
    )
    first_name = forms.CharField(max_length=150, label='Imię')
    last_name = forms.CharField(max_length=150, label='Nazwisko')
    email = forms.EmailField(label='E-mail')

    def clean(self):
        data = super().clean()
        if User.objects.filter(username=data['user_name']):
            raise forms.ValidationError('Użytkownik o takiej nazwie już istnieje')
        if data['password'] != data['password_rep']:
            raise forms.ValidationError('Wprowadzone hasła nie pasują do siebie')
        return data

class PasswordForm(forms.Form):
    password = forms.CharField(
        max_length=150,
        label='Wprowadź nowe hasło',
        widget=forms.PasswordInput()
    )
    password_rep = forms.CharField(
        max_length=150,
        label='Ponownie wprowadź nowe hasło',
        widget=forms.PasswordInput()
    )

    def clean(self):
        data = super().clean()
        if data['password'] != data['password_rep']:
            raise forms.ValidationError('Wprowadzone hasła nie pasują do siebie')
        return data

