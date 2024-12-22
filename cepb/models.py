from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

class Church(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom de l'église")
    description = models.TextField(verbose_name="Description")
    pastor_name = models.CharField(max_length=100, verbose_name="Nom du pasteur")
    address = models.CharField(max_length=255, verbose_name="Adresse")
    location = models.CharField(max_length=100, verbose_name="Localisation")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email", default='contact@cepb.org')
    service_time = models.TextField(verbose_name="Horaires des cultes")
    image = models.ImageField(upload_to='churches/', verbose_name="Image")
    capacity = models.IntegerField(verbose_name="Capacité", default=0)
    main_activities = models.TextField(verbose_name="Activités principales")
    special_ministries = models.TextField(verbose_name="Ministères spéciaux", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Église"
        verbose_name_plural = "Églises"

    def __str__(self):
        return self.name

class Activity(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de l'activité")
    description = models.TextField(verbose_name="Description")
    day = models.CharField(max_length=50, verbose_name="Jour")
    time = models.CharField(max_length=50, verbose_name="Heure")
    location = models.CharField(max_length=200, verbose_name="Lieu")
    leader = models.CharField(max_length=200, verbose_name="Responsable")
    image = models.ImageField(upload_to='activities/', verbose_name="Image", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['day', 'time']

    def __str__(self):
        return f"{self.title} ({self.day} à {self.time})"

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[
        ('draft', 'Brouillon'),
        ('published', 'Publié')
    ], default='draft')

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def __str__(self):
        return self.title

class ServiceSchedule(models.Model):
    DAYS = [
        ('Dimanche', 'Dimanche'),
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi')
    ]
    
    TYPE_CHOICES = [
        ('culte', 'Culte'),
        ('enseignement', 'Enseignement'),
        ('priere', 'Prière'),
        ('jeunesse', 'Jeunesse'),
        ('enfants', 'École du Dimanche')
    ]

    title = models.CharField(max_length=200, verbose_name='Titre du service')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='culte')
    day = models.CharField(max_length=20, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.title} - {self.day} {self.start_time}"

    @property
    def is_next_service(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        today = now.strftime('%A')
        
        # Convertir les jours en français
        days_fr_to_en = {
            'Dimanche': 'Sunday',
            'Lundi': 'Monday',
            'Mardi': 'Tuesday',
            'Mercredi': 'Wednesday',
            'Jeudi': 'Thursday',
            'Vendredi': 'Friday',
            'Samedi': 'Saturday'
        }
        
        service_day_en = days_fr_to_en[self.day]
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        today_index = days_of_week.index(today)
        service_index = days_of_week.index(service_day_en)
        
        # Calculer le nombre de jours jusqu'au prochain service
        days_until = (service_index - today_index) % 7
        
        # Si c'est le même jour, vérifier l'heure
        if days_until == 0:
            service_time = datetime.combine(now.date(), self.start_time)
            if now > service_time:
                days_until = 7
        
        next_service_date = now.date() + timedelta(days=days_until)
        return next_service_date

    @classmethod
    def get_next_service(cls):
        from datetime import datetime
        services = cls.objects.filter(is_active=True).order_by('day', 'start_time')
        if not services:
            return None
            
        next_service = None
        min_days_until = float('inf')
        
        for service in services:
            next_date = service.is_next_service
            days_until = (next_date - datetime.now().date()).days
            if days_until < min_days_until:
                min_days_until = days_until
                next_service = service
                
        return next_service

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Galerie"
        verbose_name_plural = "Galeries"

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.subject} - {self.name}"

class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=200)
    date = models.DateField()
    scripture_reference = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True)
    audio_file = models.FileField(upload_to='sermons/', blank=True, null=True)
    description = models.TextField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.preacher}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    author_name = models.CharField(max_length=200)
    author_role = models.CharField(max_length=200)
    content = models.TextField()
    author_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.author_name} - {self.author_role}"

class PrayerRequest(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    request = models.TextField()
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demande de prière"
        verbose_name_plural = "Demandes de prière"

    def __str__(self):
        return f"Prière pour {self.name}"

class Donation(models.Model):
    CURRENCY_CHOICES = [
        ('FC', 'Francs Congolais'),
        ('USD', 'Dollars US')
    ]

    PURPOSE_CHOICES = [
        ('general', 'Don général'),
        ('mission', 'Soutien aux missions'),
        ('building', 'Projet de construction'),
        ('youth', 'Ministère de la jeunesse'),
        ('other', 'Autre')
    ]
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='FC', verbose_name="Devise")
    donor_name = models.CharField(max_length=200, verbose_name="Nom du donateur")
    donor_email = models.EmailField(verbose_name="Email du donateur")
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES, default='general', verbose_name="Type de don")
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Moyen de paiement")
    is_anonymous = models.BooleanField(default=False, verbose_name="Don anonyme")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Don"
        verbose_name_plural = "Dons"
        ordering = ['-created_at']

    def __str__(self):
        amount_str = f"{self.amount} {self.currency}"
        return f"Don de {amount_str} par {self.donor_name if not self.is_anonymous else 'Anonyme'}"

class ContactInfo(models.Model):
    address = models.CharField(max_length=255, verbose_name="Adresse")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    sunday_service = models.CharField(max_length=100, verbose_name="Culte dominical", default="9h30 - 12h30")
    intercession_prayer = models.CharField(max_length=100, verbose_name="Prière d'intercession", default="9h00 - 18h00")
    teaching_service = models.CharField(max_length=100, verbose_name="Culte d'enseignement", default="16h30 - 18h30")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Information de contact"
        verbose_name_plural = "Informations de contact"

    def __str__(self):
        return f"Informations de contact {self.id}"

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name="Contenu")
    excerpt = models.TextField(verbose_name="Extrait", blank=True)
    image = models.ImageField(upload_to='blog/', verbose_name="Image", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('draft', 'Brouillon'),
            ('published', 'Publié')
        ],
        default='draft',
        verbose_name="Statut"
    )
    categories = models.CharField(
        max_length=100,
        choices=[
            ('actualites', 'Actualités'),
            ('enseignements', 'Enseignements'),
            ('temoignages', 'Témoignages'),
            ('evenements', 'Événements')
        ],
        default='actualites',
        verbose_name="Catégorie"
    )

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cepb:blog_detail', args=[self.slug])

class PaymentMethod(models.Model):
    PROVIDER_CHOICES = [
        ('mpesa', 'M-PESA'),
        ('airtel', 'Airtel Money'),
        ('orange', 'Orange Money'),
        ('bank', 'Banque'),
        ('rawbank', 'Rawbank'),
        ('tmb', 'Trust Merchant Bank'),
        ('equity', 'Equity Bank'),
        ('fbn', 'First Bank'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom du moyen de paiement")
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, verbose_name="Fournisseur")
    account_number = models.CharField(max_length=50, verbose_name="Numéro de compte")
    account_name = models.CharField(max_length=100, verbose_name="Nom du compte")
    instructions = models.TextField(verbose_name="Instructions de paiement")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Moyen de paiement"
        verbose_name_plural = "Moyens de paiement"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.provider})"
