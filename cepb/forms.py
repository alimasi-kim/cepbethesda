from django import forms
from .models import Church, Activity, News, ContactMessage, Gallery, PrayerRequest, Donation

class ChurchForm(forms.ModelForm):
    class Meta:
        model = Church
        fields = [
            'name', 'location', 'description',
            'pastor_name', 'phone', 'email',
            'image', 'service_time', 'address',
            'capacity', 'main_activities', 'special_ministries',
            'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Description générale de l\'église...'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Adresse complète...'}),
            'main_activities': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ex: Culte de jeunesse, École du dimanche, Chorale...'
            }),
            'special_ministries': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ex: Ministère des femmes, Évangélisation...'
            }),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'day', 'time', 'location', 'leader', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'day': forms.Select(choices=[
                ('Lundi', 'Lundi'),
                ('Mardi', 'Mardi'),
                ('Mercredi', 'Mercredi'),
                ('Jeudi', 'Jeudi'),
                ('Vendredi', 'Vendredi'),
                ('Samedi', 'Samedi'),
                ('Dimanche', 'Dimanche'),
            ])
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title',
            'slug',
            'excerpt',
            'content',
            'image',
            'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, label='Nom')
    email = forms.EmailField(label='Email')
    subject = forms.CharField(max_length=200, label='Sujet')
    message = forms.CharField(widget=forms.Textarea, label='Message')

class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['name', 'email', 'request', 'is_private']
        labels = {
            'name': 'Votre nom',
            'email': 'Votre email',
            'request': 'Votre demande de prière',
            'is_private': 'Garder ma demande privée'
        }
        widgets = {
            'request': forms.Textarea(attrs={'rows': 4}),
        }

class DonationForm(forms.Form):
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

    amount = forms.DecimalField(
        label='Montant',
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le montant'})
    )
    currency = forms.ChoiceField(
        label='Devise',
        choices=CURRENCY_CHOICES,
        initial='FC',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    donor_name = forms.CharField(
        label='Votre nom',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom'})
    )
    donor_email = forms.EmailField(
        label='Votre email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre email'})
    )
    purpose = forms.ChoiceField(
        label='Type de don',
        choices=PURPOSE_CHOICES,
        initial='general',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_anonymous = forms.BooleanField(
        label='Je souhaite faire un don anonyme',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )