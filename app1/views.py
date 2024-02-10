from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import JobSeekerProfile, EmployerProfile, Notification,Job, JobApplication,EmployerNotification,RejectedJob
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Notification
from django.http import HttpResponse
from django.conf import settings
import secrets,random,string
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from .models import JobSeekerNotification, SelectedJob
from django.views.decorators.cache import never_cache
from django.utils.dateparse import parse_date
from .models import VerifiedUser
from django.contrib.messages import get_messages
from django.views import View
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage




def home(request):
    return render(request, 'home.html')



def login(request):
    return render(request, 'login.html')

def jobseeker_signup(request):
    return render(request, 'jobseeker_signup.html')

def employer_signup(request):
    return render(request, 'employer_signup.html')

def admin(request):
    return render(request, 'admin.html')



# def jobseeker(request):
    jobseeker_profile = JobSeekerProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(is_approved=True)
    if not jobseeker_profile.profile_picture or not jobseeker_profile.educational_info or not jobseeker_profile.address:
        if not request.session.get('profile_popup_shown', False):
            request.session['profile_popup_shown'] = True
            show_popup = True
        else:
            show_popup = False
    else:
        show_popup = False
    
    return render(request, 'jobseeker.html', {'jobs': jobs,'show_popup': show_popup, 'jobseeker_profile': jobseeker_profile,})


def jobseeker(request):
    jobseeker_profile = JobSeekerProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(is_approved=True)

    # if not jobseeker_profile.profile_picture or not jobseeker_profile.educational_info or not jobseeker_profile.address:
    #     messages.warning(request, "Your profile is incomplete. Please complete it .")
    # else:
    #     messages.success(request, " ")

    show_popup = not jobseeker_profile.profile_picture or not jobseeker_profile.educational_info or not jobseeker_profile.address

    print(f'show_popup: {show_popup}')

    return render(request, 'jobseeker.html', {'jobs': jobs, 'jobseeker_profile': jobseeker_profile, 'jobseeker': request.user, 'show_popup': show_popup})





# def filtered_jobs(request):
#     location_filter = request.GET.get('location')
#     if location_filter:
#         jobs = Job.objects.filter(is_approved=True, location=location_filter)
#     else:
#         jobs = Job.objects.filter(is_approved=True)
#     all_locations = Job.objects.filter(location__isnull=False).values_list('location', flat=True).distinct()
#     return render(request, 'jobseeker.html', {'jobs': jobs, 'all_locations': all_locations})



# def filtered_jobs(request):
    query = request.GET.get('q')
    jobs = Job.objects.filter(is_approved=True)

    if query:
        parsed_date = parse_date(query)
        if parsed_date:
            jobs = jobs.filter(
                Q(location__icontains=query) |
                Q(designation__icontains=query) |
                Q(posting_date=parsed_date)
            )
        else:
            jobs = jobs.filter(
                Q(location__icontains=query) |
                Q(designation__icontains=query)
            )

    all_locations = Job.objects.filter(location__isnull=False).values_list('location', flat=True).distinct()
    return render(request, 'jobseeker.html', {'jobs': jobs, 'all_locations': all_locations})
from django.db.models import Q
from django.db import connection

def filter_jobs(request):
    # Get filter parameters from the request
    designation = request.GET.get('designation', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    last_date = request.GET.get('last_date', '')

    # Start with an empty queryset
    filtered_jobs = Job.objects.filter(is_approved=True)

    # Apply filters based on user input
    if designation:
        filtered_jobs = filtered_jobs.filter(Q(designation__icontains=designation))

    if location:
        filtered_jobs = filtered_jobs.filter(Q(location__icontains=location))

    if job_type:
        filtered_jobs = filtered_jobs.filter(Q(type=job_type))

    if last_date:
        try:
            # Extract the month from the last_date
            month = int(last_date.split('-')[1])
            # Add filtering based on the month
            filtered_jobs = filtered_jobs.filter(Q(last_date__month=month))
        except ValueError:
            # Handle the case where last_date is not in the expected format
            # You may want to log or handle this error in a way that makes sense for your application
            pass

    # Print filter parameters and SQL query for debugging
    print(f"Designation: {designation}")
    print(f"Location: {location}")
    print(f"Job Type: {job_type}")
    print(f"Last Date: {last_date}")

    if connection.queries:
        print(f"SQL Query: {connection.queries[-1]['sql']}")
    else:
        print("No SQL queries recorded.")

    return render(request, 'jobseeker.html', {'jobs': filtered_jobs})







def employer(request):
    employer_profile = EmployerProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(employer_profile=employer_profile, is_approved=True).exclude(employer_profile__isnull=True)
    jobs_with_applicants = jobs.annotate(num_applicants=Count('jobapplication'))
    return render(request, 'employer.html', {'employer_profile': employer_profile, 'jobs': jobs_with_applicants})





# def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
  
        
        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            if authenticated_user.is_staff:
                # Superuser (admin) login
                auth_login(request, authenticated_user)
                # messages.success(request, 'Admin login successful.')
                return redirect('admin_profile')

            try:
                jobseeker_profile = JobSeekerProfile.objects.get(user=authenticated_user)
                if not jobseeker_profile.blocked:
                    auth_login(request, authenticated_user)
                    # messages.success(request, 'Jobseeker login successful.')
                    return redirect('jobseeker')
                else:
                    messages.error(request, 'This account is blocked.')
            except JobSeekerProfile.DoesNotExist:
                pass

            try:
                employer_profile = EmployerProfile.objects.get(user=authenticated_user)
                if not employer_profile.blocked:
                    auth_login(request, authenticated_user)
                    # messages.success(request, 'Employer login successful.')
                    return redirect('employer')
                else:
                    messages.error(request, 'This account is blocked.')
            except EmployerProfile.DoesNotExist:
                pass

        messages.error(request, 'Invalid username or password.')
       
    error_messages = [message.message for message in get_messages(request) if message.tags == 'error']

       
    return render(request, 'login.html',{'error_messages': error_messages})


from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from .models import JobSeekerProfile, EmployerProfile

def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
  
        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            if authenticated_user.is_staff:
                # Superuser (admin) login
                auth_login(request, authenticated_user)
                return redirect('admin_profile')

            try:
                jobseeker_profile = JobSeekerProfile.objects.get(user=authenticated_user)
                if jobseeker_profile.is_approved and not jobseeker_profile.blocked:
                    auth_login(request, authenticated_user)
                    return redirect('jobseeker')
                elif not jobseeker_profile.is_approved:
                    messages.error(request, 'Your job seeker account is not yet approved.')
                else:
                    messages.error(request, 'This job seeker account is blocked.')
            except JobSeekerProfile.DoesNotExist:
                pass

            try:
                employer_profile = EmployerProfile.objects.get(user=authenticated_user)
                if employer_profile.is_approved and not employer_profile.blocked:
                    auth_login(request, authenticated_user)
                    return redirect('employer')
                elif not employer_profile.is_approved:
                    messages.error(request, 'Your employer account is not yet approved.')
                else:
                    messages.error(request, 'This employer account is blocked.')
            except EmployerProfile.DoesNotExist:
                pass

        messages.error(request, 'Invalid username or password.')
       
    error_messages = [message.message for message in get_messages(request) if message.tags == 'error']

    return render(request, 'login.html', {'error_messages': error_messages})




def notifications(request):
    
    job_posted_notifications = Notification.objects.filter(notification_type='job_posted').select_related('employer_profile', 'jobs')
    job_application_notifications = Notification.objects.filter(notification_type='job_applied')
    notification_count = job_posted_notifications.filter(is_read=False).count()

    
    new_jobseeker_notifications = Notification.objects.filter(notification_type='job_seeker_signup', action='signup')
    new_employer_notifications = Notification.objects.filter(notification_type='employer_signup', action='signup')

    
    # from_nav1 = request.GET.get('from_nav1', None)
    # if from_nav1 is not None:
    #     # Perform any additional handling if needed
    #     pass
    
    # for notification in new_jobseeker_notifications:
    #     print(f"Job Seeker {notification.name} Verification Status: {notification.profile.is_verified}")
   
    # for notification in new_employer_notifications:
    #     print(f"Employer {notification.company_name} Verification Status: {notification.employer_profile.is_verified}")


    return render(
        request,
        'notifications.html',
        {
            'job_posted_notifications': job_posted_notifications,
            'new_jobseeker_notifications': new_jobseeker_notifications,
            'new_employer_notifications': new_employer_notifications,
            'job_application_notifications': job_application_notifications,
            'notification_count': notification_count
        }
    )







# def jobseeker_signup(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if email is unique
        if JobSeekerProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('jobseeker_signup')

        # Check if username is unique
        if JobSeekerProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('jobseeker_signup')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('jobseeker_signup')

        # Create the User object and set the password
        user = User.objects.create_user(username=username, email=email, password=password)

        # Process job seeker signup
        jobseeker = JobSeekerProfile.objects.create(
            user=user,
            name=name,
            email=email,
            mobile=mobile,
            dob=dob,
            username=username,
            password=password
            # You may need to adjust the fields based on your JobSeekerProfile model
        )

        # Create notification
        Notification.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            dob=dob,
            action='signup',
            notification_type='job_seeker_signup'
        )

        messages.success(request, 'Job seeker registration successful. Please log in.')
        return redirect('login')

    return render(request, 'jobseeker_signup.html')







# def employer_signup(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        logo = request.FILES['logo']
        website = request.POST['website']
        address = request.POST['address']
        password = request.POST['password']

        # Check if email is unique
        if EmployerProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('employer_signup')

        # Process employer signup
        employer = EmployerProfile.objects.create(
            company_name=company_name,
            email=email,
            mobile=mobile,
            logo=logo,
            website=website,
            address=address,
            password=password
        )

        # Create notification
        Notification.objects.create(user_type='employer', username=company_name, action='signup')

        messages.success(request, 'Employer registration successful. Please log in.')
        return redirect('login')

    return render(request, 'employer_signup.html')

# def jobseeker_signup(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if email is unique
        if JobSeekerProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('jobseeker_signup')

        # Check if username is unique
        if JobSeekerProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('jobseeker_signup')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('jobseeker_signup')

        # Create the User object and set the password
        user = User.objects.create_user(username=username, email=email, password=password)

        # Process job seeker signup
        jobseeker = JobSeekerProfile.objects.create(
            user=user,
            name=name,
            email=email,
            mobile=mobile,
            dob=dob,
            username=username,
            password=password
            # You may need to adjust the fields based on your JobSeekerProfile model
        )

        # Create notification
        Notification.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            dob=dob,
            action='signup',
            notification_type='job_seeker_signup'
        )

        # Send an email to the user with autogenerated password and username
        subject = 'Welcome to YourSite - Job Seeker Signup'
        message = f'Thank you for signing up as a job seeker!\n\nUsername: {username}\nPassword: {password}'
        from_email = 'vishalvenugopal89@gmail.com'  # Update with your email
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        
        messages.success(request, 'Job seeker registration successful. Please log in.')
        return redirect('login')

    return render(request, 'jobseeker_signup.html')


def jobseeker_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if JobSeekerProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'jobseeker_signup.html')

        if JobSeekerProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'jobseeker_signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'jobseeker_signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)

        jobseeker = JobSeekerProfile.objects.create(
            user=user,
            name=name,
            email=email,
            mobile=mobile,
            dob=dob,
            username=username,
            password=password
            
        )

        
        Notification.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            dob=dob,
            action='signup',
            notification_type='job_seeker_signup'
        )

        
        subject = 'Welcome to YourSite - Job Seeker Signup'
        message = f'Thank you for signing up as a job seeker!\n\nUsername: {username}\nPassword: {password}'
        from_email = 'vishalvenugopal89@gmail.com'  
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        
        messages.success(request, 'Job seeker registration successful. Please log in.')
        return redirect('login')
    
    storage = messages.get_messages(request)
    storage.used = True
    
    return render(request, 'jobseeker_signup.html')




def employer_signup(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        logo = request.FILES['logo']
        website = request.POST['website']
        address = request.POST['address']
        password = request.POST['password']

        # Check if email is unique
        if EmployerProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('employer_signup')

        # Check if username is unique
        if EmployerProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('employer_signup')

        # Create the User object and set the password
        user = User.objects.create_user(username=username, email=email, password=password)

        # Process employer signup
        employer = EmployerProfile.objects.create(
            user=user,
            company_name=company_name,
            email=email,
            mobile=mobile,
            logo=logo,
            website=website,
            address=address,
            username=username,
            password=password
            
        )

        Notification.objects.create(
            company_name=company_name,
            email=email,
            mobile=mobile,
            logo=logo,
            website=website,
            address=address,
            action='signup',
            notification_type='employer_signup'
        )

        subject = 'Welcome to YourSite - Employer Signup'
        message = f'Thank you for signing up as a Employer !\n\nUsername: {username}\nPassword: {password}'
        from_email = 'vishalvenugopal89@gmail.com'  
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        

        messages.success(request, 'Employer registration successful. Please log in.')
        return redirect('login')

    return render(request, 'employer_signup.html')







def logoutview(request):
    logout(request)
    return redirect('login')  



def approve_action(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)

    
    username = secrets.token_urlsafe(8)
    password = secrets.token_urlsafe(12)

    
    jobseeker = JobSeekerProfile.objects.get(email=notification.email)
    jobseeker.auto_generated_username = username
    jobseeker.auto_generated_password = password
    jobseeker.save()

    
    subject = 'Your Account Details'
    message = f'Your username: {username}\nYour password: {password}'
    from_email = 'vishalvenugopal89@gmail.com'  
    recipient_list = [notification.email]

    send_mail(subject, message, from_email, recipient_list)

    

    return redirect('notifications')







# def post_job(request):
    if request.method == 'POST':
        employer_profile = EmployerProfile.objects.get(user=request.user)
        designation = request.POST.get('designation')
        description = request.POST.get('description')
        last_date = request.POST.get('last_date')
        image = request.FILES.get('image')

        job = Job.objects.create(
            employer_profile=employer_profile,
            designation=designation,
            description=description,
            last_date=last_date,
            posting_date=timezone.now(),
            image=image,
            is_approved=False  # Job is not approved initially
        )

        Notification.objects.create(
            employer_profile=employer_profile,
            notification_type='job_posted',
            jobs=job
        )

        messages.success(request, 'Job posted successfully. Waiting for admin approval.')
        return redirect('employer')

    return render(request, 'jobsposted.html')


def post_job(request):
    if request.method == 'POST':
        employer_profile = EmployerProfile.objects.get(user=request.user)
        designation = request.POST.get('designation')
        description = request.POST.get('description')
        last_date = request.POST.get('last_date')
        image = request.FILES.get('image')
        location = request.POST.get('location') 
        type = request.POST.get('type')


        job = Job.objects.create(
            employer_profile=employer_profile,
            designation=designation,
            description=description,
            last_date=last_date,
            posting_date=timezone.now(),
            image=image,
            is_approved=False,
            location=location,
            type=type

        )

        Notification.objects.create(
            employer_profile=employer_profile,
            notification_type='job_posted',
            jobs=job
        )

        messages.success(request,'Job posted successfully. Please wait for admin approval.')
        return redirect('jobposted')

    return render(request, 'jobsposted.html')









def jobposted(request):
    return render(request, 'jobsposted.html')



def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        job.designation = request.POST.get('designation')
        job.description = request.POST.get('description')
        job.location = request.POST.get('location') 
        job.last_date = request.POST.get('last_date')
        image = request.FILES.get('image')
        job.type = request.POST.get('type')

        if image:
            job.image = image

        job.save()
        return redirect('employer')  

    return render(request, 'edit_job.html', {'job': job})



def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        job.delete()
        return redirect('employer')  

    return render(request, 'delete_job.html', {'job': job})





# def apply_job(request, job_id):
#     job = get_object_or_404(Job, pk=job_id)
#     jobseeker = request.user

#     if JobApplication.objects.filter(jobseeker=jobseeker, job=job).exists():
#         return redirect('jobseeker')

#     job_application = JobApplication.objects.create(jobseeker=jobseeker, job=job)

#     EmployerNotification.objects.create(
#         employer=job.employer_profile,
#         applicant=jobseeker,
#         job=job,
#         job_application=job_application,
#         application_date=datetime.now(),
#         is_read=False
        
#     )

#     return redirect('jobseeker')



# def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    jobseeker = request.user

    if JobApplication.objects.filter(jobseeker=jobseeker, job=job).exists():
        return redirect('jobseeker')

    job_application = JobApplication.objects.create(jobseeker=jobseeker, job=job)

    EmployerNotification.objects.create(
        employer=job.employer_profile,
        applicant=jobseeker,
        job=job,
        job_application=job_application,
        application_date=datetime.now(),
        is_read=False,
        notification_type='applied'  # Set the notification_type for applied jobs
    )

    return redirect('jobseeker')



def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    jobseeker = request.user

    existing_notification = EmployerNotification.objects.filter(
        employer=job.employer_profile,
        applicant=jobseeker,
        job=job,
        notification_type='applied',
    ).first()
    

    if existing_notification:
        return redirect('applied_jobs')

    job_application = JobApplication.objects.create(jobseeker=jobseeker, job=job)

    EmployerNotification.objects.create(
        employer=job.employer_profile,
        applicant=jobseeker,
        job=job,
        job_application=job_application,
        application_date=datetime.now(),
        is_read=False,
        notification_type='applied',
    )

    Notification.objects.create(
            job_seeker=jobseeker,
            jobs=job,
            notification_type='job_applied',
            is_read=False,
        )
    return redirect('jobseeker')








def applied_jobs(request):
    jobseeker = request.user
    applied_jobs = JobApplication.objects.filter(jobseeker=jobseeker).select_related('job')
    return render(request, 'applied_jobs.html', {'applied_jobs': applied_jobs, 'jobseeker': jobseeker})




# def employer_notifications(request):
    employer_profile = EmployerProfile.objects.get(user=request.user)
    notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
    notification_count = notifications.count()
    unread_notifications = EmployerNotification.objects.filter(is_read=False)
    notification_count = unread_notifications.count()
    read_notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=True)
    return render(request, 'employer_notifications.html', {'notifications': notifications, 'notification_count': notification_count, 'notifications': unread_notifications,'read_notifications': read_notifications })



# def employer_notifications(request):
    employer_profile = EmployerProfile.objects.get(user=request.user)
    notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
    notification_count = notifications.count()
    unread_notifications = EmployerNotification.objects.filter(is_read=False)
    notification_count = unread_notifications.count()
    read_notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=True)
    
    print("All notifications:", [n.id for n in notifications])
    print("Unread notifications:", [n.id for n in unread_notifications])
    print("Read notifications:", [n.id for n in read_notifications])

    return render(request, 'employer_notifications.html', {'notifications': notifications, 'notification_count': notification_count, 'unread_notifications': unread_notifications, 'read_notifications': read_notifications})



# def employer_notifications(request):
    employer_profile = EmployerProfile.objects.get(user=request.user)
    unread_notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
    read_notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=True)

    notification_count = unread_notifications.count()

    print("Notification count in employer_notifications view:", notification_count)

    return render(request, 'employer_notifications.html', {'unread_notifications': unread_notifications, 'read_notifications': read_notifications})


def employer_notifications(request):
    employer_profile = EmployerProfile.objects.get(user=request.user)
    unread_notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
    read_notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=True)
    for notification in unread_notifications:
        notification.mark_as_read()
        
        if notification.notification_type == 'applied':
                job_seeker = notification.applicant
                job_name = notification.job.designation
                message = f'Your profile has been viewed for the job "{job_name}"'
                JobSeekerNotification.objects.create(
                    job_seeker=job_seeker,
                    message=message,
                    notification_type='viewed'
                )
            
    notification_count = unread_notifications.count() 

    print("Unread notifications:", [n.id for n in unread_notifications])
    print("Read notifications:", [n.id for n in read_notifications])

    if notification_count > 0:
        messages.info(request, 'You have received new notifications.')

    return render(request, 'employer_notifications.html', {'unread_notifications': unread_notifications, 'read_notifications': read_notifications, 'notification_count': notification_count})

















# def employer_notifications(request, from_nav3=0):
#     employer_profile = EmployerProfile.objects.get(user=request.user)
#     unread_notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=False)
#     read_notifications = EmployerNotification.objects.filter(employer=employer_profile, is_read=True)

#     notification_count = unread_notifications.count()  # Debugging line

#     if from_nav3 == 0:
#         # Include job_posted_notifications only if accessed from other sections, not from nav3
#         job_posted_notifications = Notification.objects.filter(notification_type='job_posted', is_read=False)
#         notification_count += job_posted_notifications.count()

#     print("Unread notifications:", [n.id for n in unread_notifications])
#     print("Read notifications:", [n.id for n in read_notifications])

#     return render(request, 'employer_notifications.html', {'unread_notifications': unread_notifications, 'read_notifications': read_notifications, 'notification_count': notification_count})












def applicant_details(request, notification_id):
    notification = get_object_or_404(EmployerNotification, id=notification_id)
    notification.is_read = True
    notification.save()
    return render(request, 'applicant_details.html', {'notification': notification})





def nothired(request, notification_id):
    notification = get_object_or_404(EmployerNotification, id=notification_id)
    notification.is_read = True
    notification.save()
    return render(request, 'nothired.html', {'notification': notification})





def admin_jobs(request):
    jobs = Job.objects.filter(is_approved=True)
    return render(request, 'admin_jobs.html', {'jobs': jobs})


# def job_details(request, job_id):
#     job = get_object_or_404(Job, id=job_id)
#     if not job.is_approved:
#         messages.error(request, 'This job is not yet approved.')
#         return redirect('notifications')
#     jobs = Job.objects.filter(employer_profile=job.employer_profile).exclude(employer_profile__isnull=True)
#     return render(request, 'job_details.html', {'jobs': jobs})




def job_details(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    job = notification.jobs
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    if request.method == 'POST':
            
            if 'approve' in request.POST:
                job.is_approved = True
                job.save()
            elif 'disapprove' in request.POST:
                job.is_approved = False
                job.save()

                related_notifications = Notification.objects.filter(jobs=job, is_read=False)
                for related_notification in related_notifications:
                    related_notification.mark_as_read()
    return render(request, 'job_details.html', {'job': job})



def approve_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.is_approved = True
    job.save()
    return redirect('admin_jobs')




@login_required
def employer_account(request):
    employer_profile = EmployerProfile.objects.get(user=request.user)
    context = {'employer_profile': employer_profile}
    return render(request, 'employer_account.html', context)



# @login_required
# def edit_employer_profile(request):
#     if request.method == 'POST':
#         employer_profile = EmployerProfile.objects.get(user=request.user)
#         employer_profile.company_name = request.POST.get('company_name')
#         employer_profile.username = request.POST.get('username')
#         employer_profile.email = request.POST.get('email')
#         employer_profile.mobile = request.POST.get('mobile')
#         employer_profile.website = request.POST.get('website')
#         employer_profile.address = request.POST.get('address')
#         employer_profile.logo = request.FILES.get('logo')
#         employer_profile.save()
#         return redirect('employer_account')

#     employer_profile = EmployerProfile.objects.get(user=request.user)
#     context = {'employer_profile': employer_profile}
#     return render(request, 'edit_employer_profile.html', context)



# def edit_employer_profile(request):
#     if request.method == 'POST':
#         employer_profile = EmployerProfile.objects.get(user=request.user)
#         employer_profile.company_name = request.POST.get('company_name')
#         employer_profile.username = request.POST.get('username')
#         employer_profile.email = request.POST.get('email')
#         employer_profile.mobile = request.POST.get('mobile')
#         employer_profile.website = request.POST.get('website')
#         employer_profile.address = request.POST.get('address')

        
#         new_logo = request.FILES.get('logo')
#         if new_logo:
            
#             employer_profile.logo.save(new_logo.name, ContentFile(new_logo.read()), save=True)

#         employer_profile.save()
#         return redirect('employer_account')

#     employer_profile = EmployerProfile.objects.get(user=request.user)
#     context = {'employer_profile': employer_profile}
#     return render(request, 'edit_employer_profile.html', context)



from django.contrib import messages

def edit_employer_profile(request):
    employer_profile = get_object_or_404(EmployerProfile, user=request.user)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        # Check if the new username is already taken by another user
        if User.objects.filter(username=new_username).exclude(pk=request.user.id).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'edit_employer_profile.html', {'employer_profile': employer_profile})

        # Check if the new email is already taken by another user
        if User.objects.filter(email=new_email).exclude(pk=request.user.id).exists():
            messages.error(request, 'Email already exists. Please choose a different one.')
            return render(request, 'edit_employer_profile.html', {'employer_profile': employer_profile})

        employer_profile.company_name = request.POST.get('company_name')
        employer_profile.username = new_username
        employer_profile.email = new_email
        employer_profile.mobile = request.POST.get('mobile')
        employer_profile.website = request.POST.get('website')
        employer_profile.address = request.POST.get('address')

        new_logo = request.FILES.get('logo')
        if new_logo:
            employer_profile.logo.save(new_logo.name, ContentFile(new_logo.read()), save=True)

        employer_profile.save()
        # messages.success(request, 'Profile updated successfully!')
        return redirect('employer_account')

    return render(request, 'edit_employer_profile.html', {'employer_profile': employer_profile})











@login_required
def employer_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = User.objects.get(username=request.user.username)
        
        
        if user.check_password(old_password):
            
            if new_password == confirm_password:
                
                user.set_password(new_password)
                user.save()

                
                update_session_auth_hash(request, user)

                messages.success(request, 'Your password was successfully updated!')
                return redirect('employer_password')
            else:
                messages.error(request, 'New password and confirm password do not match.')
        else:
            messages.error(request, 'Old password is incorrect.')

    return render(request, 'employer_password.html')



def jobseeker_profile(request):
    jobseeker_profile = JobSeekerProfile.objects.get(user=request.user)
    return render(request, 'jobseeker_profile.html', {'jobseeker_profile': jobseeker_profile})




# def edit_jobseeker_profile(request):
#     jobseeker_profile = JobSeekerProfile.objects.get(user=request.user)

#     if request.method == 'POST':
#         jobseeker_profile.name = request.POST.get('name')
#         jobseeker_profile.email = request.POST.get('email')
#         jobseeker_profile.mobile = request.POST.get('mobile')
#         jobseeker_profile.dob = request.POST.get('dob')
#         jobseeker_profile.username = request.POST.get('username')  
        
#         new_profile_picture = request.FILES.get('profile_picture')
#         if new_profile_picture:  
#             jobseeker_profile.profile_picture = new_profile_picture

#         jobseeker_profile.educational_info = request.POST.get('educational_info')
#         jobseeker_profile.address = request.POST.get('address')

#         jobseeker_profile.save()
#         messages.success(request, '')
#         return redirect('jobseeker_profile')

#     return render(request, 'edit_jobseeker_profile.html', {'jobseeker_profile': jobseeker_profile})


# from django.contrib.auth.models import User

# def edit_jobseeker_profile(request):
#     jobseeker_profile = get_object_or_404(JobSeekerProfile, user=request.user)

#     if request.method == 'POST':
#         new_username = request.POST.get('username')

#         # Check if the new username is already taken by another user
#         if User.objects.filter(username=new_username).exclude(pk=request.user.id).exists():
#             messages.error(request, 'Username already exists. Please choose a different one.')
#             return render(request, 'edit_jobseeker_profile.html', {'jobseeker_profile': jobseeker_profile})

#         jobseeker_profile.name = request.POST.get('name')
#         jobseeker_profile.email = request.POST.get('email')
#         jobseeker_profile.mobile = request.POST.get('mobile')
#         jobseeker_profile.dob = request.POST.get('dob')
        
#         jobseeker_profile.username = new_username

#         new_profile_picture = request.FILES.get('profile_picture')
#         if new_profile_picture:
#             jobseeker_profile.profile_picture = new_profile_picture

#         jobseeker_profile.educational_info = request.POST.get('educational_info')
#         jobseeker_profile.address = request.POST.get('address')

#         jobseeker_profile.save()
#         # messages.success(request, '    ')
#         return redirect('jobseeker_profile')

#     return render(request, 'edit_jobseeker_profile.html', {'jobseeker_profile': jobseeker_profile})


from django.contrib.auth.models import User

def edit_jobseeker_profile(request):
    jobseeker_profile = get_object_or_404(JobSeekerProfile, user=request.user)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        # Check if the new username is already taken by another user
        if User.objects.filter(username=new_username).exclude(pk=request.user.id).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'edit_jobseeker_profile.html', {'jobseeker_profile': jobseeker_profile})

        # Check if the new email is already taken by another user
        if User.objects.filter(email=new_email).exclude(pk=request.user.id).exists():
            messages.error(request, 'Email already exists. Please choose a different one.')
            return render(request, 'edit_jobseeker_profile.html', {'jobseeker_profile': jobseeker_profile})

        jobseeker_profile.name = request.POST.get('name')
        jobseeker_profile.email = new_email
        jobseeker_profile.mobile = request.POST.get('mobile')
        jobseeker_profile.dob = request.POST.get('dob')
        jobseeker_profile.username = new_username

        new_profile_picture = request.FILES.get('profile_picture')
        if new_profile_picture:
            jobseeker_profile.profile_picture = new_profile_picture

        jobseeker_profile.educational_info = request.POST.get('educational_info')
        jobseeker_profile.address = request.POST.get('address')

        jobseeker_profile.save()
        # messages.success(request, 'Profile updated successfully!')
        return redirect('jobseeker_profile')

    return render(request, 'edit_jobseeker_profile.html', {'jobseeker_profile': jobseeker_profile})



# @login_required
# def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Check if the current password is correct
        if check_password(current_password, request.user.password):
            # Check if the new password and confirm new password match
            if new_password == confirm_new_password:
                # Update the user's password
                request.user.password = make_password(new_password)
                request.user.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('jobseeker_profile')
            else:
                messages.error(request, 'New password and confirm new password do not match.')
        else:
            messages.error(request, 'Incorrect current password.')

    return render(request, 'update_password.html')


def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if request.user.check_password(current_password):
            
            if new_password == confirm_new_password:
                
                request.user.set_password(new_password)
                request.user.save()

                update_session_auth_hash(request, request.user)

                messages.success(request, 'Your password was successfully updated!')
                return redirect('update_password')
            else:
                messages.error(request, 'New password and confirm new password do not match.')
        else:
            messages.error(request, 'Incorrect current password.')

    return render(request, 'update_password.html')



@login_required
def admin_profile(request):
    
    admin_user = request.user
    return render(request, 'admin_profile.html', {'admin_user': admin_user})



# @login_required
# def update_admin_password(request):
#     if request.method == 'POST':
#         current_password = request.POST.get('current_password')
#         new_password = request.POST.get('new_password')
#         confirm_new_password = request.POST.get('confirm_new_password')

#         # Check if the current password is correct
#         if check_password(current_password, request.user.password):
#             # Check if the new password and confirm new password match
#             if new_password == confirm_new_password:
#                 # Update the admin user's password
#                 request.user.password = make_password(new_password)
#                 request.user.save()
#                 messages.success(request, 'Your password was successfully updated!')
#                 return redirect('admin_profile')
#             else:
#                 messages.error(request, 'New password and confirm new password do not match.')
#         else:
#             messages.error(request, 'Incorrect current password.')

#     return render(request, 'update_admin_password.html')



from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def update_admin_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        
        if request.user.check_password(current_password):
            
            if new_password == confirm_new_password:
                
                request.user.set_password(new_password)
                request.user.save()

                
                update_session_auth_hash(request, request.user)

                # messages.success(request, ' ')
                return redirect('admin_profile')
            else:
                messages.error(request, 'New password and confirm new password do not match.')
        else:
            messages.error(request, 'Incorrect current password.')

    return render(request, 'update_admin_password.html')







# @login_required
# def edit_admin_profile(request):
#     if request.method == 'POST':
        
#         new_email = request.POST.get('new_email')
#         new_username = request.POST.get('new_username')

        
#         request.user.email = new_email
#         request.user.username = new_username
#         request.user.save()

#         messages.success(request, 'Your profile was successfully updated!')
#         return redirect('admin_profile')

    
#     admin_user = request.user
#     return render(request, 'edit_admin_profile.html', {'admin_user': admin_user})



from django.contrib import messages

def edit_admin_profile(request):
    admin_user = request.user

    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        new_username = request.POST.get('new_username')

        # Check if the new username is already taken by another user
        if User.objects.filter(username=new_username).exclude(pk=admin_user.id).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'edit_admin_profile.html', {'admin_user': admin_user})

        # Check if the new email is already taken by another user
        if User.objects.filter(email=new_email).exclude(pk=admin_user.id).exists():
            messages.error(request, 'Email already exists. Please choose a different one.')
            return render(request, 'edit_admin_profile.html', {'admin_user': admin_user})

        admin_user.email = new_email
        admin_user.username = new_username
        admin_user.save()

        # messages.success(request, 'Your profile was successfully updated!')
        return redirect('admin_profile')

    return render(request, 'edit_admin_profile.html', {'admin_user': admin_user})



#for approving by admin
def disapprove_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    
    job.is_approved = False
    job.save()

    
    return redirect('admin_jobs')  




def disapproved_jobs(request):
    
    disapproved_jobs = Job.objects.filter(is_approved=False)

    return render(request, 'disapproved_jobs.html', {'disapproved_jobs': disapproved_jobs})





# @login_required
# def jobseeker_notifications(request):
#     # Fetch job notifications for the current user
#     notifications = JobSeekerNotification.objects.filter(job_seeker=request.user)

#     # Mark notifications as read if not already read
#     for notification in notifications:
#         if not notification.is_read:
#             notification.mark_as_read()

#     return render(request, 'jobseeker_notifications.html', {'notifications': notifications})




# @login_required
# @never_cache
# def jobseeker_notifications(request):
    
#     notifications = JobSeekerNotification.objects.filter(job_seeker=request.user)

    
#     notification_count = notifications.filter(is_read=False).count()

    
#     unread_notifications = notifications.filter(is_read=False)
#     for notification in unread_notifications:
#         notification.mark_as_read()

    
#     context = {'notifications': notifications, 'notification_count': notification_count}

#     return render(request, 'jobseeker_notifications.html', context)


def jobseeker_notifications(request):
    # Retrieve all notifications for the current job seeker
    notifications = JobSeekerNotification.objects.filter(job_seeker=request.user)

    # Filter unread notifications
    unread_notifications = notifications.filter(is_read=False)

    # Mark all unread notifications as read
    for notification in unread_notifications:
        notification.mark_as_read()

    # Pass only unread notifications to the template
    context = {'notifications': unread_notifications}

    return render(request, 'jobseeker_notifications.html', context)



def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applicants = JobApplication.objects.filter(job=job)
    print("Job:", job) 
    print("Applicants:", applicants) 
    return render(request, 'view_applicants.html', {'job': job, 'applicants': applicants})



# def select_applicant(request, job_id, jobseeker_id):
#     job = get_object_or_404(Job, id=job_id)
#     jobseeker = get_object_or_404(User, id=jobseeker_id)

    
#     job_application = JobApplication.objects.get(jobseeker=jobseeker, job=job)
#     job_application.selected = True
#     job_application.save()
    
    
#     SelectedJob.objects.create(
#         job_seeker=jobseeker,
#         job=job,
#     )

    
#     JobSeekerNotification.objects.create(
#             job_seeker=jobseeker,
#             message=f'Congratulations! You have been selected for the job: {job.designation}',
#             is_read=False,
#         )   

#     messages.success(request, f'{jobseeker.username} has been selected for the job.')

#     return redirect('view_applicants', job_id=job_id)






from django.http import JsonResponse

def select_applicant(request, job_id, jobseeker_id):
    job = get_object_or_404(Job, id=job_id)
    jobseeker = get_object_or_404(User, id=jobseeker_id)

    job_application = JobApplication.objects.get(jobseeker=jobseeker, job=job)
    job_application.selected = True
    job_application.save()

    SelectedJob.objects.create(
        job_seeker=jobseeker,
        job=job,
    )

    JobSeekerNotification.objects.create(
        job_seeker=jobseeker,
        message=f'Congratulations! You have been selected for the job: {job.designation}',
        is_read=False,
    )

    messages.success(request, f'{jobseeker.username} has been selected for the job.')
    
    # Assuming you now have a 'selected' field in your JobApplication model
    applicants = JobApplication.objects.filter(job=job, selected=True)

    return render(request, 'view_applicants.html', {'job': job, 'applicants': applicants})



# def selected_jobs(request):
#     # Fetch selected job notifications for the current user
#     selected_jobs = JobSeekerNotification.objects.filter(
#         job_seeker=request.user,
#         notification_type__in=['selected', None],  # Filter by the notification type (including null)
#         is_read=True  # Display only read notifications (selected jobs)
#     )

#     return render(request, 'selected_jobs.html', {'selected_jobs': selected_jobs})



# def selected_jobs(request):
#     # Fetch selected job notifications for the current user
#     selected_jobs = JobSeekerNotification.objects.filter(
#         job_seeker=request.user,
#         notification_type__in=['selected', None],  # Filter by the notification type (including null)
#     ).exclude(is_read=False)  # Exclude unread notifications

#     return render(request, 'selected_jobs.html', {'selected_jobs': selected_jobs})



def selected_jobs(request):
    selected_jobs = SelectedJob.objects.filter(job_seeker=request.user)
    return render(request, 'selected_jobs.html', {'selected_jobs': selected_jobs})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse

@csrf_exempt
def toggle_verification(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id)

        # Determine the profile type (JobSeeker or Employer)
        if notification.job_seeker:
            profile = notification.job_seeker.jobseekerprofile
        elif notification.employer_profile:
            profile = notification.employer_profile
        else:
            # Handle the case where neither job_seeker nor employer_profile is present
            data = {'error': 'Invalid notification'}
            return JsonResponse(data, status=400)

        # Toggle the verification status
        profile.is_verified = not profile.is_verified
        profile.save()

        data = {'message': 'Verification status toggled successfully'}
        return JsonResponse(data)
    else:
        data = {'error': 'Invalid method'}
        return JsonResponse(data, status=400)




# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
# from .models import JobSeekerProfile, EmployerProfile, Notification

# def verify_jobseeker(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     jobseeker_profile = get_object_or_404(JobSeekerProfile, user=notification.user_profile.user)

#     jobseeker_profile.is_verified = True
#     jobseeker_profile.save()

#     notification.mark_as_read()

#     data = {'message': 'Job Seeker verified successfully'}
#     return JsonResponse(data)

# def verify_employer(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     employer_profile = get_object_or_404(EmployerProfile, user=notification.employer_profile.user)

#     employer_profile.is_verified = True
#     employer_profile.save()

#     notification.mark_as_read()

#     data = {'message': 'Employer verified successfully'}
#     return JsonResponse(data)








# def verify_jobseeker(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     jobseeker = get_object_or_404(JobSeekerProfile, email=notification.email)
#     jobseeker.is_verified = True
#     jobseeker.save()
#     data = {'message': 'Job Seeker verified successfully'}
#     return JsonResponse(data)


# def block_jobseeker(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     jobseeker_profile = get_object_or_404(JobSeekerProfile, email=notification.email)
#     jobseeker_profile.blocked = True
#     jobseeker_profile.save()
#     data = {'message': 'Job Seeker blocked successfully'}
#     return JsonResponse(data)

# def verify_jobseeker(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     jobseeker = get_object_or_404(JobSeekerProfile, email=notification.email)
#     jobseeker.is_verified = True
#     jobseeker.save()
#     notification.mark_as_read()  # Update the is_read field on the notification
#     data = {'message': 'Job Seeker verified successfully'}
#     return JsonResponse(data)

def block_jobseeker(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    jobseeker_profile = get_object_or_404(JobSeekerProfile, email=notification.email)
    jobseeker_profile.blocked = True
    jobseeker_profile.save()
    notification.mark_as_read()  # Update the is_read field on the notification
    data = {'message': 'Job Seeker blocked successfully'}
    return JsonResponse(data)




# def verify_employer(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     employer_profile = get_object_or_404(EmployerProfile, email=notification.email)
#     employer_profile.is_verified = True
#     employer_profile.save()
#     data = {'message': 'Employer verified successfully'}
#     notification.is_read = True
#     notification.save()
#     return JsonResponse(data)


# def block_employer(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     employer_profile = get_object_or_404(EmployerProfile, email=notification.email)
#     employer_profile.blocked = True
#     employer_profile.save()
#     notification.is_read = True
#     notification.save()
#     return JsonResponse({'message': 'Employer blocked successfully'})





# def verify_employer(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     employer_profile = get_object_or_404(EmployerProfile, email=notification.email)
#     employer_profile.is_verified = True
#     employer_profile.save()
#     notification.mark_as_read()  # Update the is_read field on the notification
#     data = {'message': 'Employer verified successfully'}
#     return JsonResponse(data)

def block_employer(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    employer_profile = get_object_or_404(EmployerProfile, email=notification.email)
    employer_profile.blocked = True
    employer_profile.save()
    notification.mark_as_read()  # Update the is_read field on the notification
    return JsonResponse({'message': 'Employer blocked successfully'})





# from django.shortcuts import get_object_or_404, render, redirect
# from django.http import JsonResponse
# from .models import Notification, JobSeekerProfile, EmployerProfile

# def verify_jobseeker(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     jobseeker_profile = get_object_or_404(JobSeekerProfile, email=notification.email)
#     jobseeker_profile.is_verified = True
#     jobseeker_profile.save()
#     data = {'message': 'Job Seeker verified successfully'}
#     return redirect('verified_users')

# def block_jobseeker(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     jobseeker_profile = get_object_or_404(JobSeekerProfile, email=notification.email)
#     jobseeker_profile.blocked = True
#     jobseeker_profile.save()
#     data = {'message': 'Job Seeker blocked successfully'}
#     return redirect('verified_users')

# def verify_employer(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     employer_profile = get_object_or_404(EmployerProfile, email=notification.email)
#     employer_profile.is_verified = True
#     employer_profile.save()
#     data = {'message': 'Employer verified successfully'}
#     notification.is_read = True
#     notification.save()
#     return redirect('verified_users')

# def block_employer(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     employer_profile = get_object_or_404(EmployerProfile, email=notification.email)
#     employer_profile.blocked = True
#     employer_profile.save()
#     notification.is_read = True
#     notification.save()
#     return redirect('verified_users')



def verification_success(request):
    return render(request, 'verification_success.html')



def jobseeker_details(request, notification_id):
    jobseeker = get_object_or_404(JobSeekerProfile, id=notification_id)
    return render(request, 'jobseeker_details.html', {'jobseeker': jobseeker})



def verified_users(request):
    # Fetch all verified users from the database
    verified_users = VerifiedUser.objects.all()

    return render(
        request,
        'verified_users.html',
        {'verified_users': verified_users}
    )
    




class NotificationCountAPIView(View):
    def get(self, request, *args, **kwargs):
        # Fetch the notification count
        notification_count = JobSeekerNotification.objects.filter(
            job_seeker=request.user,
            is_read=False
        ).count()

        # Return the count as JSON
        return JsonResponse({'count': notification_count})





@user_passes_test(lambda u: u.is_superuser)
def custom_notification_count_api(request, *args, **kwargs):
    print('CustomNotificationCountAPIView accessed by superuser.')
    notification_count = Notification.objects.filter(is_read=False).count()
    print(f'Notification count: {notification_count}')

    return JsonResponse({'count': notification_count})




def view_jobseekers(request):
    jobseekers = JobSeekerProfile.objects.all()
    return render(request, 'jobseekers_list.html', {'jobseekers': jobseekers})



from django.views.decorators.http import require_POST


@require_POST
def verify_jobseeker(request, jobseeker_id):
    jobseeker = get_object_or_404(JobSeekerProfile, id=jobseeker_id)

    # Toggle the verification status
    jobseeker.is_verified = not jobseeker.is_verified
    jobseeker.save()

    return JsonResponse({'status': 'success'})



def view_employers(request):
    employers = EmployerProfile.objects.all()
    return render(request, 'employers_list.html', {'employers': employers})



@require_POST
def verify_employer(request, employer_id):
   employer = get_object_or_404(EmployerProfile, id=employer_id)

   # Toggle the verification status
   employer.is_verified = not employer.is_verified
   employer.save()

   return JsonResponse({'status': 'success'})




# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.contrib.auth.models import User

# def reject_applicant(request, job_id, jobseeker_id):
#     job = get_object_or_404(Job, id=job_id)
    
#     # Retrieve the jobseeker user from the job
#     jobseeker_user = get_object_or_404(User, id=jobseeker_id)
    
#     # Retrieve the associated JobSeekerProfile
#     jobseeker_profile = get_object_or_404(JobSeekerProfile, user=jobseeker_user)

#     # Your existing logic to reject the applicant

#     # Update the job to mark it as rejected

#     # Create a RejectedJob instance
#     RejectedJob.objects.create(job_seeker=jobseeker_user, job=job, rejection_date=timezone.now())

#     # Create a rejection notification
#     message = f"You have been rejected for the job: {job.designation}"
#     notification = JobSeekerNotification(job_seeker=jobseeker_user, message=message, is_read=False, notification_type='other')
#     notification.save()

#     return HttpResponseRedirect(reverse('view_applicants', args=[job.id]))


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

def reject_applicant(request, job_id, jobseeker_id):
    job = get_object_or_404(Job, id=job_id)
    jobseeker_user = get_object_or_404(User, id=jobseeker_id)
    job_application = get_object_or_404(JobApplication, job=job, jobseeker=jobseeker_user)

    print(f"Before rejection: {job_application.rejected}")

    # Your existing logic to reject the applicant

    # Update the job application to mark it as rejected
    job_application.rejected = True
    job_application.save()

    print(f"After rejection: {job_application.rejected}")

    # Create a RejectedJob instance
    RejectedJob.objects.create(job_seeker=jobseeker_user, job=job, rejection_date=timezone.now())

    # Create a rejection notification
    message = f"You have been rejected for the job: {job.designation}"
    notification = JobSeekerNotification(job_seeker=jobseeker_user, message=message, is_read=False, notification_type='other')
    notification.save()

    return HttpResponseRedirect(reverse('view_applicants', args=[job.id]))







def rejected_jobs(request):
    # Retrieve rejected jobs for the current user
    rejected_jobs = RejectedJob.objects.filter(job_seeker=request.user)
    context = {'rejected_jobs': rejected_jobs}
    return render(request, 'rejected_jobs.html', context)





# def approve_jobseeker(request, notification_id):
#     jobseeker_notification = get_object_or_404(Notification, id=notification_id, notification_type='job_seeker_signup')

#     if jobseeker_notification.job_seeker:
#         job_seeker_profile = get_object_or_404(JobSeekerProfile, user=jobseeker_notification.job_seeker)
#         job_seeker_profile.is_approved = True
#         job_seeker_profile.save()

#         jobseeker_notification.is_approved = True
#         jobseeker_notification.save()
        
#         jobseeker_notification.mark_as_read()

#         print(f"Job Seeker approved successfully. Job Seeker ID: {job_seeker_profile.id}")
#         return JsonResponse({'status': 'success'})
#     else:
#         print('Job seeker not found')
#         return JsonResponse({'status': 'error', 'message': 'Job seeker not found'})


# def approve_employer(request, notification_id):
#     employer_notification = get_object_or_404(Notification, id=notification_id, notification_type='employer_signup')

#     if employer_notification.employer_profile:
#         employer_profile = get_object_or_404(EmployerProfile, user=employer_notification.employer_profile.user)
#         employer_profile.is_approved = True
#         employer_profile.save()

#         employer_notification.is_approved = True
#         employer_notification.save()

#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Employer profile not found'})



def approve_jobseeker(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    jobseeker_profile = get_object_or_404(JobSeekerProfile, email=notification.email)
    jobseeker_profile.is_approved = True
    jobseeker_profile.save()
    notification.mark_as_read()  # Update the is_read field on the notification
    data = {'message': 'Job Seeker approved successfully'}
    return JsonResponse(data)



def approve_employer(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    employer_profile = get_object_or_404(EmployerProfile, email=notification.email)
    employer_profile.is_approved = True
    employer_profile.save()
    notification.mark_as_read()  # Update the is_read field on the notification
    data = {'message': 'Employer approved successfully'}
    return JsonResponse(data)



from django.shortcuts import render, get_object_or_404
from .models import Notification

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Mark the notification as read
    notification.mark_as_read()

    # Perform any additional actions or rendering as needed

    return redirect('notifications')  # Redirect back to the notifications page





