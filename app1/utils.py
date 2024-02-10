# utils.py
from .models import Notification

def get_notification_count(user):
    if user.is_authenticated:
        # Assume EmployerProfile has a OneToOneField to User
        employer_profile = user.employerprofile
        notifications = Notification.objects.filter(employer_profile=employer_profile, is_read=False)
        return notifications.count()
    return 0
