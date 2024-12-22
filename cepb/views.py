from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    Church, Sermon, Event, Testimonial, PrayerRequest, 
    Donation, Gallery, ContactMessage, ContactInfo, Post, PaymentMethod, ServiceSchedule
)
from .forms import ContactForm, PrayerRequestForm, DonationForm

def home(request):
    # Récupérer le prochain service
    next_service = ServiceSchedule.get_next_service()
    
    # Récupérer les événements à venir
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date', 'time')[:3]
    
    # Récupérer les dernières prédications
    latest_sermons = Sermon.objects.all().order_by('-date')[:3]
    
    # Récupérer les témoignages
    testimonials = Testimonial.objects.all().order_by('-date')[:3]
    
    # Récupérer les églises
    churches = Church.objects.filter(is_active=True)
    
    # Statistiques
    stats = {
        'churches_count': Church.objects.count(),
        'members_count': sum(church.capacity for church in Church.objects.all()),
        'sermons_count': Sermon.objects.count(),
        'activities_count': Event.objects.count(),
    }
    
    # Récupérer les moyens de paiement actifs
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    
    context = {
        'next_service': next_service,
        'upcoming_events': upcoming_events,
        'latest_sermons': latest_sermons,
        'testimonials': testimonials,
        'churches': churches,
        'stats': stats,
        'payment_methods': payment_methods,
    }
    return render(request, 'cepb/home.html', context)

def about(request):
    context = {
        'churches': Church.objects.filter(is_active=True),
        'stats': {
            'churches_count': Church.objects.count(),
            'members_count': sum(church.capacity for church in Church.objects.all()),
            'sermons_count': Sermon.objects.count(),
            'activities_count': Event.objects.count(),
        }
    }
    return render(request, 'cepb/about.html', context)

def mission(request):
    return render(request, 'cepb/mission.html')

def vision(request):
    return render(request, 'cepb/vision.html')

# Églises
def church_list(request):
    churches = Church.objects.all()
    return render(request, 'churches/list.html', {'churches': churches})

def church_detail(request, pk):
    church = get_object_or_404(Church, pk=pk)
    return render(request, 'churches/detail.html', {'church': church})

# Sermons
def sermon_list(request):
    sermons = Sermon.objects.all().order_by('-date')
    return render(request, 'sermons/list.html', {'sermons': sermons})

def sermon_detail(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)
    return render(request, 'sermons/detail.html', {'sermon': sermon})

# Événements
def event_list(request):
    events = Event.objects.all().order_by('date', 'time')
    featured_events = events.filter(is_featured=True)
    upcoming_events = events.filter(date__gte=timezone.now().date())
    
    context = {
        'events': events,
        'featured_events': featured_events,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'events/list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/detail.html', {'event': event})

# Blog
def blog_list(request):
    post_list = Post.objects.filter(status='published').order_by('-created_at')
    
    # Pagination : 9 articles par page
    paginator = Paginator(post_list, 9)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Récupérer l'article précédent et suivant
    previous_post = Post.objects.filter(
        status='published',
        created_at__lt=post.created_at
    ).order_by('-created_at').first()
    
    next_post = Post.objects.filter(
        status='published',
        created_at__gt=post.created_at
    ).order_by('created_at').first()
    
    return render(request, 'blog/detail.html', {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post
    })

# Galerie
def gallery(request):
    photos = Gallery.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'gallery/gallery.html', {'photos': photos})

# Contact
def contact(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Votre message a été envoyé avec succès.')
            return redirect('cepb:contact')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {
        'form': form,
        'contact_info': contact_info
    })

# Prière
def prayer_request(request):
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre demande de prière a été reçue.')
            return redirect('cepb:home')
    else:
        form = PrayerRequestForm()
    return render(request, 'prayer/request.html', {'form': form})

# Dons
def donation(request):
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    
    # Récupérer les paramètres de l'URL
    initial_amount = request.GET.get('amount')
    initial_currency = request.GET.get('currency')
    
    initial = {}
    if initial_amount:
        initial['amount'] = initial_amount
    if initial_currency:
        initial['currency'] = initial_currency
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            messages.success(request, 'Merci pour votre don! Nous vous contacterons bientôt pour finaliser la transaction.')
            return redirect('cepb:donation_success')
    else:
        form = DonationForm(initial=initial)
    
    context = {
        'form': form,
        'payment_methods': payment_methods,
        'title': 'Faire un don',
        'description': 'Soutenez notre mission en faisant un don'
    }
    return render(request, 'donation/donation.html', context)

def donation_success(request):
    return render(request, 'donation/success.html')

def donation_cancel(request):
    return render(request, 'donation/cancel.html')


