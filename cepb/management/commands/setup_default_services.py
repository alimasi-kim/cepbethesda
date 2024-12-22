from django.core.management.base import BaseCommand
from cepb.models import ServiceSchedule
from datetime import time

class Command(BaseCommand):
    help = 'Configure les horaires de services par défaut'

    def handle(self, *args, **kwargs):
        default_services = [
            {
                'title': "Culte d'adoration",
                'day': 'Dimanche',
                'start_time': time(10, 0),  # 10:00
                'end_time': time(12, 30),   # 12:30
                'description': "Culte dominical d'adoration et de louange",
                'icon': 'fas fa-church',
                'order': 1,
            },
            {
                'title': 'Soirée de prière',
                'day': 'Mardi',
                'start_time': time(18, 0),  # 18:00
                'end_time': time(20, 0),    # 20:00
                'description': 'Soirée de prière et d\'intercession',
                'icon': 'fas fa-pray',
                'order': 2,
            },
            {
                'title': 'Étude biblique',
                'day': 'Jeudi',
                'start_time': time(18, 0),  # 18:00
                'end_time': time(20, 0),    # 20:00
                'description': 'Étude approfondie de la Parole de Dieu',
                'icon': 'fas fa-bible',
                'order': 3,
            },
            {
                'title': 'Réunion des jeunes',
                'day': 'Samedi',
                'start_time': time(15, 0),  # 15:00
                'end_time': time(17, 0),    # 17:00
                'description': 'Rencontre de la jeunesse',
                'icon': 'fas fa-users',
                'order': 4,
            },
        ]

        for service_data in default_services:
            ServiceSchedule.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            self.stdout.write(
                self.style.SUCCESS(f'Service créé : {service_data["title"]}')
            ) 