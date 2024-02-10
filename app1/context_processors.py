# context_processors.py

from .models import EmployerProfile, EmployerNotification, Notification

# def notification_count(request):
#     if request.user.is_authenticated and hasattr(request.user, 'employerprofile'):
#         employer_profile = EmployerProfile.objects.get(user=request.user)
#         notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
#         return {'notification_count': notifications.count()}
#     return {'notification_count': 0}





# def notification_count(request):
#     notification_count = 0

#     if request.user.is_authenticated:
#         if hasattr(request.user, 'employerprofile'):
#             employer_profile = EmployerProfile.objects.get(user=request.user)
#             notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
#             notification_count += notifications.count()
        
#         # Add count for job_posted_notifications
#         job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
#         notification_count += job_posted_notifications.count()

#     return {'notification_count': notification_count}




# def notification_count(request):
#     notification_count = 0

#     if request.user.is_authenticated:
#         if hasattr(request.user, 'employerprofile'):
#             employer_profile = EmployerProfile.objects.get(user=request.user)
#             employer_notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
#             notification_count += employer_notifications.count()

#         # Add count for job_posted_notifications
#         job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
#         notification_count += job_posted_notifications.count()

#     return {'notification_count': notification_count}




# def notification_count(request):
#     notification_count = 0

#     if request.user.is_authenticated:
#         if hasattr(request.user, 'employerprofile'):
#             employer_profile = EmployerProfile.objects.get(user=request.user)
#             # Check only unread employer notifications
#             notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
#             notification_count += notifications.count()

#         # Check only unread job_posted_notifications
#         job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
#         notification_count += job_posted_notifications.count()

#     return {'notification_count': notification_count}




# def notification_count(request):
#     notification_count = 0

#     if request.user.is_authenticated:
#         if hasattr(request.user, 'employerprofile'):
#             employer_profile = EmployerProfile.objects.get(user=request.user)
#             # Check only unread employer notifications
#             notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
#             notification_count += notifications.count()

#         # Check only unread job_posted_notifications for the admin in nav1
#         if request.resolver_match.url_name != 'employer_notifications':
#             job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
#             notification_count += job_posted_notifications.count()

#     return {'notification_count': notification_count}




# def notification_count(request):
#     notification_count = 0

#     if request.user.is_authenticated:
#         if hasattr(request.user, 'employerprofile'):
#             employer_profile = EmployerProfile.objects.get(user=request.user)
#             # Check only unread employer notifications
#             notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
#             notification_count += notifications.count()

#         # Check only unread job_posted_notifications for the admin in nav1
#         current_view_name = request.resolver_match.url_name
#         exclude_nav3_notifications = current_view_name != 'employer_notifications'

#         if exclude_nav3_notifications:
#             job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
#             notification_count += job_posted_notifications.count()

#     return {'notification_count': notification_count}






# def notification_count(request):
#     notification_count = 0

#     if request.user.is_authenticated:
#         if hasattr(request.user, 'employerprofile'):
#             employer_profile = EmployerProfile.objects.get(user=request.user)
#             # Check only unread employer notifications
#             notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
#             notification_count += notifications.count()

#         # Check only unread job_posted_notifications for the admin in nav1
#         exclude_nav3_notifications = '/employer_notifications/' not in request.path

#         if exclude_nav3_notifications:
#             job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
#             notification_count += job_posted_notifications.count()

#     return {'notification_count': notification_count}






# def notification_count(request):
#     notification_count = 0

#     if request.user.is_authenticated:
#         if hasattr(request.user, 'employerprofile'):
#             employer_profile = EmployerProfile.objects.get(user=request.user)
#             # Check only unread employer notifications
#             notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
#             notification_count += notifications.count()

#         # Check only unread job_posted_notifications for the admin in nav1
#         current_view_name = request.resolver_match.url_name
#         from_nav3 = request.GET.get('from_nav3', None)

#         exclude_nav3_notifications = current_view_name == 'employer_notifications' and from_nav3 is None

#         if exclude_nav3_notifications:
#             job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
#             notification_count += job_posted_notifications.count()

#     return {'notification_count': notification_count}







def notification_count(request):
    notification_count = 0

    if request.user.is_authenticated:
        if hasattr(request.user, 'employerprofile'):
            employer_profile = EmployerProfile.objects.get(user=request.user)
            # Check only unread employer notifications
            notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
            notification_count += notifications.count()

        current_view_name = request.resolver_match.url_name

        if current_view_name == 'notifications':
            # For nav1.html, include job_posted_notifications count
            job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
            notification_count += job_posted_notifications.count()

    return {'notification_count': notification_count}






# For nav1.html
def nav1_notification_count(request):
    notification_count = 0

    if request.user.is_authenticated:
        # Check only unread job_posted_notifications for nav1.html
        job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
        notification_count += job_posted_notifications.count()

    return {'nav1_notification_count': notification_count}

# For nav3.html
def nav3_notification_count(request):
    notification_count = 0

    if request.user.is_authenticated:
        if hasattr(request.user, 'employerprofile'):
            employer_profile = EmployerProfile.objects.get(user=request.user)
            # Check only unread employer notifications for nav3.html
            notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
            notification_count += notifications.count()

    return {'nav3_notification_count': notification_count}
