from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('services/', views.services, name='services'),
    path('services/<int:id>/', views.service_detail, name='service_detail'),
    path('book-service/', views.book_service, name='book_service'),
    
    
    
    path('my-events/', views.my_events, name='my_events'),
    path('profile/', views.profile, name='profile'),
   
    path('events/', views.public_events, name='public_events'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),
    path('events/<int:id>/register/', views.register_event, name='register_event'),
    
    path('gallery/', views.gallery, name='gallery'),
    path('notifications/', views.notifications, name='notifications'),
   
   path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard",
    ),
   
   path(
    "manage-bookings/",
    views.manage_bookings,
    name="manage_bookings",
    ),
   
   path(
    "booking/<int:id>/approve/",
    views.approve_booking,
    name="approve_booking",
    ),

    path(
    "booking/<int:id>/cancel/",
    views.cancel_booking,
    name="cancel_booking",
    ),
    
    path(
    "manage-registrations/",
    views.manage_registrations,
    name="manage_registrations",
    ),
    
    
path(
    "manage-services/",
    views.manage_services,
    name="manage_services",
),

path(
    "add-service/",
    views.add_service,
    name="add_service",
),

path(
    "edit-service/<int:id>/",
    views.edit_service,
    name="edit_service",
),

path(
    "delete-service/<int:id>/",
    views.delete_service,
    name="delete_service",
),


path(
    "manage-events/",
    views.manage_events,
    name="manage_events",
),

path(
    "add-event/",
    views.add_event,
    name="add_event",
),

path(
    "edit-event/<int:id>/",
    views.edit_event,
    name="edit_event",
),

path(
    "delete-event/<int:id>/",
    views.delete_event,
    name="delete_event",
),

path(
    "contact-messages/",
    views.contact_messages,
    name="contact_messages",
),

path(
    "edit-profile/",
    views.edit_profile,
    name="edit_profile",
),

path(
    "password-change/",
    auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html"
    ),
    name="password_change",
),

path(
    "password-change/done/",
    auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"
    ),
    name="password_change_done",
),

path(
    "ticket/<int:id>/",
    views.event_ticket,
    name="event_ticket",
),
]