from django.core.management.base import BaseCommand
from cepb.models import ServiceSchedule
from datetime import time

class Command(BaseCommand):
    help = 'Configure les horaires des services de la CEPB'

    def handle(self, *args, **kwargs):
        cepb_services = [
            {
                'title': "Culte d'adoration",
                'day': 'Dimanche',
                'start_time': time(10, 0),  # 10:00
                'end_time': time(13, 0),    # 13:00
                'description': "Culte dominical d'adoration et de louange à la CEPB",
                'icon': 'fas fa-church',
                'order': 1,
            },
            {
                'title': 'Intercession',
                'day': 'Mardi',
                'start_time': time(17, 0),  # 17:00
                'end_time': time(19, 0),    # 19:00
                'description': 'Soirée de prière et d\'intercession',
                'icon': 'fas fa-pray',
                'order': 2,
            },
            {
                'title': 'Étude biblique',
                'day': 'Jeudi',
                'start_time': time(17, 0),  # 17:00
                'end_time': time(19, 0),    # 19:00
                'description': 'Étude approfondie de la Parole de Dieu',
                'icon': 'fas fa-bible',
                'order': 3,
            },
            {
                'title': 'Ministère des Jeunes',
                'day': 'Samedi',
                'start_time': time(14, 0),  # 14:00
                'end_time': time(16, 0),    # 16:00
                'description': 'Rencontre de la jeunesse CEPB',
                'icon': 'fas fa-users',
                'order': 4,
            },
            {
                'title': 'Chorale',
                'day': 'Samedi',
                'start_time': time(16, 0),  # 16:00
                'end_time': time(18, 0),    # 18:00
                'description': 'Répétition de la chorale',
                'icon': 'fas fa-music',
                'order': 5,
            },
            {
                'title': 'École du Dimanche',
                'day': 'Dimanche',
                'start_time': time(8, 30),  # 08:30
                'end_time': time(9, 30),    # 09:30
                'description': 'Formation spirituelle des enfants',
                'icon': 'fas fa-child',
                'order': 6,
            },
        ]

        # Créer les nouveaux services
        for service_data in cepb_services:
            service, created = ServiceSchedule.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            status = 'créé' if created else 'mis à jour'
            self.stdout.write(
                self.style.SUCCESS(f'Service {status} : {service_data["title"]}')
            ) 