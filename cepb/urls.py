from django.urls import path
from . import views

app_name = 'cepb'

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Pages statiques
    path('about/', views.about, name='about'),
    path('mission/', views.mission, name='mission'),
    path('vision/', views.vision, name='vision'),
    path('contact/', views.contact, name='contact'),
    
    # Églises
    path('churches/', views.church_list, name='church_list'),
    path('churches/<int:pk>/', views.church_detail, name='church_detail'),
    
    # Sermons
    path('sermons/', views.sermon_list, name='sermon_list'),
    path('sermons/<int:pk>/', views.sermon_detail, name='sermon_detail'),
    
    # Événements
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Galerie
    path('gallery/', views.gallery, name='gallery'),
    
    # Prière
    path('prayer-request/', views.prayer_request, name='prayer_request'),
    
    # Dons
    path('donation/', views.donation, name='donation'),
    path('donation/success/', views.donation_success, name='donation_success'),
    path('donation/cancel/', views.donation_cancel, name='donation_cancel'),
]
