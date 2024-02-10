from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    dob = models.DateField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    educational_info = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    blocked = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)


    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         # If it's a new instance, generate username and password
    #         user = User.objects.create_user(username=self.email, password=None)
    #         self.username = user.username
    #         self.password = user.password

    #     super(JobSeekerProfile, self).save(*args, **kwargs)


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True,blank=True, null=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='employer_logos/')
    website = models.URLField()
    address = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128,blank=True, null=True)  
    blocked = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    

class Job(models.Model):
    employer_profile = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, null=True)
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    designation = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='job_images/', null=True, blank=True)
    last_date = models.DateField()
    posting_date = models.DateField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    location = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=20, choices=[('Full time', 'Full Time'), ('Part time', 'Part Time')],null=True, blank=True)




class Notification(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True, blank=True)
    action = models.CharField(max_length=50, null=True)
    company_name = models.CharField(max_length=255, null=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    job_seeker = models.ForeignKey(User, related_name='job_seeker_notifications', null=True, blank=True, on_delete=models.CASCADE)
    employer_profile = models.ForeignKey(EmployerProfile, null=True, blank=True, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=50, null=True)
    jobs = models.ForeignKey(Job, null=True, blank=True, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    
    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        self.is_read = False
        self.save()



class JobApplication(models.Model):
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    selected = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    




@receiver(post_save, sender=JobApplication)
def create_notification(sender, instance, **kwargs):
    # Check if a notification for the same job and applicant already exists
    existing_notification = EmployerNotification.objects.filter(
        employer=instance.job.employer_profile,
        applicant=instance.jobseeker,
        job=instance.job,
        job_application=instance,
        application_date=instance.application_date,
        is_read=False
    ).first()

    # Create a new notification only if it doesn't exist
    if not existing_notification:
        EmployerNotification.objects.create(
            employer=instance.job.employer_profile,
            applicant=instance.jobseeker,
            job=instance.job,
            job_application=instance,
            application_date=instance.application_date,
            is_read=False
        )




class EmployerNotification(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE,null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE,null=True)
    application_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(
        max_length=50,
        choices=[('applied', 'Applied Job'), ('selected', 'Selected Job')],
        null=True
    )

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()




class JobSeekerNotification(models.Model):
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50, choices=[('selected', 'Selected Job'), ('other', 'Other')], null=True)


    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()





class SelectedJob(models.Model):
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class VerifiedUser(models.Model):
    name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=50) 

    def __str__(self):
        return self.name



class RejectedJob(models.Model):
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    rejection_date = models.DateTimeField(auto_now_add=True)





