"""myplan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from events.views import IndexView, Dashboard, AddClient, AddEvent, ClientDetails, EventDetails, ClientList, EventList, AddSubcontractor, SubcontractorDetails, SubcontractorsList,  SubcontractorModify, ClientModify, EventModify, DeleteClient, DeleteEvent, DeleteSubcontractor, AddOferta, OfertaDetails, OfferList, CreateUserView, LoginView, LogoutView, UsersView, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('main/', Dashboard.as_view(), name="dashboard"),
    path('client/add/', AddClient.as_view(), name='add_client'),
    path('event/add/', AddEvent.as_view(), name='add_event'),
    path('client/<int:pk>/', ClientDetails.as_view(), name='client_details'),
    path('event/<int:pk>/', EventDetails.as_view(), name='event_details'),
    path('client/list/', ClientList.as_view(), name='client_list'),
    path('event/list/', EventList.as_view(), name='event_list'),
    path('subcontractor/add/', AddSubcontractor.as_view(), name='add_subcontractor'),
    path('subcontractor/<int:pk>/', SubcontractorDetails.as_view(), name='subcontractor_details'),
    path('subcontractor/list/', SubcontractorsList.as_view(), name='subcontractor_list'),
    path('subcontractor/modify/<int:pk>/', SubcontractorModify.as_view(), name='subcontractor_modify'),
    path('client/modify/<int:pk>/', ClientModify.as_view(), name='client_modify'),
    path('event/modify/<int:event_id>/', EventModify.as_view(), name='event_modify'),
    path('client/delete/<int:client_id>/', DeleteClient.as_view(), name='delete_client'),
    path('event/delete/<int:event_id>/', DeleteEvent.as_view(), name='delete_event'),
    path('subcontractor/delete/<int:subcontractor_id>/', DeleteSubcontractor.as_view(), name='delete_subcontractor'),
    path('add-offer/', AddOferta.as_view(), name='add_oferta'),
    path('oferta/<int:oferta_id>/', OfertaDetails.as_view(), name='oferta_details'),
    path('offer/list/', OfferList.as_view(), name='offers_list'),
    path('list_users/', UsersView.as_view(), name='list_users'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_user/', CreateUserView.as_view(), name='add_user'),
    path('profile/', profile_view, name='profile')
]