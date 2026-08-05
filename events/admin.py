from django.contrib import admin
from .models import Service, Event, Booking, EventRegistration


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "organizer",
        "location",
        "date",
        "time",
        "ticket_price",
        "available_tickets",
        "is_active",
    )

    list_filter = (
        "date",
        
        "is_active",
    )

    search_fields = (
        "title",
        "organizer",
        "location",
    )

    list_editable = (
        "available_tickets",
        "is_active",
    )

    ordering = ("date",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "email", "service", "status")
    search_fields = ("customer_name", "email")
    list_filter = ("status",)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "event", "number_of_tickets")
    search_fields = ("full_name", "email")
    
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "subject",
        "sent_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
    )

    list_filter = (
        "sent_at",
    )
    
from django.urls import reverse
from django.utils.html import format_html    