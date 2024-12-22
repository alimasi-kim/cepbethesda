from .models import ServiceSchedule

def services_processor(request):
    services = ServiceSchedule.objects.filter(is_active=True).order_by('order', 'day', 'start_time')
    return {'services': services} 