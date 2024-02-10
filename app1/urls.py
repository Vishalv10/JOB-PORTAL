from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('jobseeker_signup', views.jobseeker_signup, name='jobseeker_signup'),
    path('employer_signup', views.employer_signup, name='employer_signup'),
    path('admin', views.admin, name='admin'),
    path('login1', views.login1, name='login1'),
    path('jobseeker', views.jobseeker, name='jobseeker'),
    path('employer', views.employer, name='employer'),
    path('notifications', views.notifications, name='notifications'),
    path('logoutviews', views.logoutview, name='logoutviews'),
    path('approve/<int:notification_id>/', views.approve_action, name='approve_action'),
    # path('disapprove/<int:notification_id>/', disapprove_action, name='disapprove_action'),
    path('post_job/', views.post_job, name='post_job'),
    path('jobposted', views.jobposted, name='jobposted'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('applied_jobs/', views.applied_jobs, name='applied_jobs'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('employer/notifications/', views.employer_notifications, name='employer_notifications'),
    path('applicant_details/<int:notification_id>/', views.applicant_details, name='applicant_details'),
    path('admin_jobs/', views.admin_jobs, name='admin_jobs'),
    path('job_details/<int:notification_id>/', views.job_details, name='job_details'),
    path('post_job/', views.post_job, name='post_job'),
    path('approve_job/<int:job_id>/', views.approve_job, name='approve_job'),
    path('nothired/<int:notification_id>/', views.nothired, name='nothired'),
    path('employer_account/', views.employer_account, name='employer_account'),
    path('edit-employer-profile/', views.edit_employer_profile, name='edit_employer_profile'),
    path('employer-password/', views.employer_password, name='employer_password'),
    path('filter_jobs/', views.filter_jobs, name='filter_jobs'),
    path('jobseeker_profile/', views.jobseeker_profile, name='jobseeker_profile'),
    path('edit_jobseeker_profile/', views.edit_jobseeker_profile, name='edit_jobseeker_profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('update_admin_password/', views.update_admin_password, name='update_admin_password'),
    path('edit_admin_profile/', views.edit_admin_profile, name='edit_admin_profile'),
    path('disapprove_job/<int:job_id>/', views.disapprove_job, name='disapprove_job'),
    path('disapproved_jobs/', views.disapproved_jobs, name='disapproved_jobs'),
    path('jobseeker_notifications/', views.jobseeker_notifications, name='jobseeker_notifications'),
    path('view_applicants/<int:job_id>/', views.view_applicants, name='view_applicants'),
    # path('select_applicant/<int:job_id>/<int:jobseeker_id>/', views.select_applicant, name='select_applicant'),
    path('select_applicant/<int:job_id>/<int:jobseeker_id>/', views.select_applicant, name='select_applicant'),

    
    
    path('selected_jobs/', views.selected_jobs, name='selected_jobs'),
    path('toggle_verification/<int:notification_id>/', views.toggle_verification, name='toggle_verification'),
   
    # path('verify_jobseeker/<int:notification_id>/', views.verify_jobseeker, name='verify_jobseeker'),
    path('block_jobseeker/<int:notification_id>/', views.block_jobseeker, name='block_jobseeker'),
    path('verification_success', views.verification_success, name='verification_success'),
    # path('verify_employer/<int:notification_id>/', views.verify_employer, name='verify_employer'),
    path('block_employer/<int:notification_id>/', views.block_employer, name='block_employer'),
    path('jobseeker_details/<int:notification_id>/', views.jobseeker_details, name='jobseeker_details'),
    path('verified_users/', views.verified_users, name='verified_users'),
    path('notification_count_api/', views.NotificationCountAPIView.as_view(), name='notification_count_api'),
    path('custom_notification_count_api/', views.custom_notification_count_api, name='custom_notification_count_api'),
    path('view_jobseekers/', views.view_jobseekers, name='view_jobseekers'),
    path('verify_jobseeker/<int:jobseeker_id>/', views.verify_jobseeker, name='verify_jobseeker'),
    path('view_employers/', views.view_employers, name='view_employers'),
    path('verify_employer/<int:employer_id>/', views.verify_employer, name='verify_employer'),
    path('reject_applicant/<int:job_id>/<int:jobseeker_id>/', views.reject_applicant, name='reject_applicant'),
    path('rejected_jobs/', views.rejected_jobs, name='rejected_jobs'),
    # path('approve_jobseeker/<int:notification_id>/', views.approve_jobseeker, name='approve_jobseeker'),
    # path('approve_employer/<int:notification_id>/', views.approve_employer, name='approve_employer'),
    path('approve_jobseeker/<int:notification_id>/', views.approve_jobseeker, name='approve_jobseeker'),
    path('approve_employer/<int:notification_id>/', views.approve_employer, name='approve_employer'),

    path('mark_notification_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),






]




