from django import forms
from .models import Church, Activity, News, ContactMessage, Gallery, PrayerRequest, Donation, PaymentMethod

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

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'amount',
            'currency',
            'donor_name',
            'donor_email',
            'purpose',
            'is_anonymous',
            'payment_method'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Montant',
                'min': '0',
                'step': '0.01'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control'
            }),
            'donor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom'
            }),
            'donor_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre email'
            }),
            'purpose': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Le montant doit être supérieur à 0.")
        return amount

    def save(self, commit=True):
        donation = super().save(commit=False)
        if commit:
            donation.save()
        return donation