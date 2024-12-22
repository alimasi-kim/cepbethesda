from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Church, Event, Sermon, Gallery, ContactMessage, 
    PrayerRequest, Donation, PaymentMethod, Post, 
    Activity, ServiceSchedule, Testimonial, ContactInfo
)

@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'pastor_name', 'phone', 'email', 'is_active')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'pastor_name', 'location')
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'description', 'pastor_name', 'image')
        }),
        ('Coordonnées', {
            'fields': ('address', 'location', 'phone', 'email')
        }),
        ('Services', {
            'fields': ('service_time', 'capacity')
        }),
        ('Activités', {
            'fields': ('main_activities', 'special_ministries')
        }),
        ('État', {
            'fields': ('is_active',)
        })
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'show_image', 'is_featured')
    list_filter = ('is_featured', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    readonly_fields = ('show_image',)
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'description', 'date', 'time')
        }),
        ('Lieu et image', {
            'fields': ('location', 'image', 'show_image')
        }),
        ('Options', {
            'fields': ('is_featured',)
        })
    )

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Pas d'image"
    show_image.short_description = 'Aperçu'

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date', 'scripture_reference', 'has_video', 'has_audio')
    list_filter = ('preacher', 'date')
    search_fields = ('title', 'preacher', 'scripture_reference', 'description')
    date_hierarchy = 'date'
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'preacher', 'date', 'scripture_reference')
        }),
        ('Contenu', {
            'fields': ('description', 'video_url', 'audio_file')
        })
    )

    def has_video(self, obj):
        return bool(obj.video_url)
    has_video.boolean = True
    has_video.short_description = 'Vidéo'

    def has_audio(self, obj):
        return bool(obj.audio_file)
    has_audio.boolean = True
    has_audio.short_description = 'Audio'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_image', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('show_image',)

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Pas d'image"
    show_image.short_description = 'Aperçu'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Expéditeur', {
            'fields': ('name', 'email')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('État', {
            'fields': ('is_read', 'created_at')
        })
    )

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'request_preview', 'created_at', 'is_private')
    list_filter = ('is_private', 'created_at')
    search_fields = ('name', 'email', 'request')
    readonly_fields = ('created_at',)

    def request_preview(self, obj):
        return obj.request[:100] + '...' if len(obj.request) > 100 else obj.request
    request_preview.short_description = 'Demande'

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount_display', 'currency', 'purpose', 'created_at', 'is_anonymous')
    list_filter = ('currency', 'purpose', 'is_anonymous', 'created_at')
    search_fields = ('donor_name', 'donor_email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Donateur', {
            'fields': ('donor_name', 'donor_email', 'is_anonymous')
        }),
        ('Don', {
            'fields': ('amount', 'currency', 'purpose')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        })
    )

    def amount_display(self, obj):
        return f"{obj.amount:,.2f} {obj.currency}"
    amount_display.short_description = 'Montant'

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'account_number', 'is_active', 'order')
    list_filter = ('provider', 'is_active')
    search_fields = ('name', 'account_number', 'account_name')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'provider', 'is_active')
        }),
        ('Détails du compte', {
            'fields': ('account_number', 'account_name')
        }),
        ('Instructions', {
            'fields': ('instructions', 'order')
        })
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'categories', 'status', 'created_at', 'show_image')
    list_filter = ('status', 'categories', 'created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('show_image',)
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Média', {
            'fields': ('image', 'show_image')
        }),
        ('Publication', {
            'fields': ('author', 'categories', 'status')
        })
    )

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Pas d'image"
    show_image.short_description = 'Aperçu'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'day', 'time', 'location', 'leader', 'show_image', 'is_active')
    list_filter = ('day', 'is_active')
    search_fields = ('title', 'description', 'leader')
    readonly_fields = ('show_image',)

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Pas d'image"
    show_image.short_description = 'Aperçu'

@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'day', 'time_display', 'is_next', 'is_active')
    list_filter = ('type', 'day', 'is_active')
    search_fields = ('title', 'description')
    fieldsets = (
        ('Informations du service', {
            'fields': ('title', 'type', 'description')
        }),
        ('Horaire', {
            'fields': ('day', 'start_time', 'end_time')
        }),
        ('État', {
            'fields': ('is_active',)
        })
    )

    def time_display(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"
    time_display.short_description = 'Horaire'

    def is_next(self, obj):
        next_service = ServiceSchedule.get_next_service()
        return obj == next_service
    is_next.boolean = True
    is_next.short_description = 'Prochain service'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_role', 'date', 'show_image')
    list_filter = ('date',)
    search_fields = ('author_name', 'content')
    readonly_fields = ('show_image',)

    def show_image(self, obj):
        if obj.author_image:
            return format_html('<img src="{}" width="100" />', obj.author_image.url)
        return "Pas d'image"
    show_image.short_description = 'Photo'

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('address', 'phone', 'email')
    fieldsets = (
        ('Coordonnées', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Horaires des services', {
            'fields': ('sunday_service', 'intercession_prayer', 'teaching_service')
        }),
        ('État', {
            'fields': ('is_active',)
        })
    )
