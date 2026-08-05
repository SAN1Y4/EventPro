from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import ContactMessage
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from .forms import ProfileForm

from .models import (
    Service,
    Event,
    Booking,
    EventRegistration,
)

from .forms import (
    BookingForm,
    EventRegistrationForm,
    ContactForm,
    RegisterForm,
    LoginForm,
)

# ==========================
# HOME
# ==========================

def home(request):
    services = Service.objects.all()[:4]
    events = Event.objects.all()[:6]

    return render(request, "home/home.html", {
        "services": services,
        "events": events,
    })


# ==========================
# ABOUT
# ==========================

def about(request):
    return render(request, "about/about.html")


# ==========================
# CONTACT
# ==========================

def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "contact/success.html")

    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {
        "form": form
    })


# ==========================
# SERVICES
# ==========================

def services(request):

    query = request.GET.get("q")

    if query:
        services = Service.objects.filter(name__icontains=query)
    else:
        services = Service.objects.all()

    return render(request, "services/services.html", {
        "services": services,
        "query": query
    })


def service_detail(request, id):

    service = get_object_or_404(Service, id=id)

    return render(request, "services/service_detail.html", {
        "service": service
    })


# ==========================
# GALLERY
# ==========================

def gallery(request):
    return render(request, "gallery.html")


# ==========================
# NOTIFICATIONS
# ==========================

def notifications(request):
    return render(request, "notifications/notifications.html")


# ==========================
# BOOK SERVICE
# ==========================
@login_required
def book_service(request):

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            if booking.preferred_date < timezone.now().date():
                messages.error(
                    request,
                    "You cannot book a service for a past date."
                )

                return render(
                    request,
                    "booking/book_service.html",
                    {"form": form}
                )

            booking.user = request.user
            booking.save()

            messages.success(
                request,
                "Your booking has been submitted successfully!"
            )

            return redirect("my_bookings")

    else:
        form = BookingForm()

    return render(
        request,
        "booking/book_service.html",
        {
            "form": form
        }
    )
# ==========================
# PUBLIC EVENTS
# ==========================

def public_events(request):

    query = request.GET.get("q")

    if query:
        events = Event.objects.filter(title__icontains=query)
    else:
        events = Event.objects.all()

    return render(request, "public_events/events.html", {
        "events": events,
        "query": query
    })


def event_detail(request, id):

    event = get_object_or_404(Event, id=id)

    return render(request,
                  "public_events/event_detail.html",
                  {
                      "event": event
                  })


# ==========================
# EVENT REGISTRATION
# ==========================

# @login_required
# def register_event(request, id):

#     event = get_object_or_404(Event, id=id)

#     # Don't allow booking if sold out
#     if event.available_tickets <= 0:
#         return render(
#             request,
#             "public_events/sold_out.html",
#             {"event": event}
#         )

#     if request.method == "POST":

#         form = EventRegistrationForm(request.POST)

#         if form.is_valid():

#             registration = form.save(commit=False)
#             registration.user = request.user
#             registration.event = event

#             tickets = registration.number_of_tickets

#             # Check ticket availability
#             if tickets > event.available_tickets:

#                 form.add_error(
#                     "number_of_tickets",
#                     f"Only {event.available_tickets} ticket(s) available."
#                 )

#             else:

#                 registration.save()

#                 # Reduce available tickets
#                 event.available_tickets -= tickets
#                 event.save()

#                 return render(
#                     request,
#                     "public_events/registration_success.html",
#                     {
#                         "registration": registration,
#                         "event": event
#                     }
#                 )

#     else:

#         form = EventRegistrationForm()

#     return render(
#         request,
#         "public_events/register_event.html",
#         {
#             "event": event,
#             "form": form
#         }
#     )
from django.contrib import messages




@login_required
def register_event(request, id):

    event = get_object_or_404(Event, id=id)

    # Don't allow registration for past events
    if event.date < timezone.now().date():
        messages.error(
            request,
            "This event has already ended."
        )
        return redirect("public_events")

    # Don't allow registration if the event is sold out
    if event.available_tickets <= 0:
        messages.error(
            request,
            "Sorry! This event is sold out."
        )
        return redirect("event_detail", id=event.id)

    if request.method == "POST":

        form = EventRegistrationForm(request.POST)

        if form.is_valid():

            registration = form.save(commit=False)

            # Prevent duplicate registration
            if EventRegistration.objects.filter(
                user=request.user,
                event=event
            ).exists():

                messages.warning(
                    request,
                    "You have already registered for this event."
                )

                return redirect("my_events")

            tickets_requested = registration.number_of_tickets

            # Check ticket availability
            if tickets_requested > event.available_tickets:

                messages.error(
                    request,
                    f"Only {event.available_tickets} ticket(s) are available."
                )

            else:

                registration.user = request.user
                registration.event = event
                registration.save()

                event.available_tickets -= tickets_requested
                event.save()

                messages.success(
                    request,
                    "Your event registration was successful!"
                )

                return redirect("event_ticket", registration.id) 

    else:
        form = EventRegistrationForm()

    return render(
        request,
        "public_events/register_event.html",
        {
            "event": event,
            "form": form,
        }
    ) 

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect

# ==========================
# USER REGISTRATION
# ==========================

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("dashboard")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


# ==========================
# LOGIN
# ==========================

def user_login(request):

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)
        if form.is_valid():

            login(request, form.get_user())

            return redirect("dashboard")

    else:

        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


# ==========================
# LOGOUT
# ==========================

@login_required
def user_logout(request):

    logout(request)

    return redirect("home")


# ==========================
# USER DASHBOARD
# ==========================

@login_required
def dashboard(request):

    total_bookings = Booking.objects.filter(user=request.user).count()

    total_events = EventRegistration.objects.filter(
        user=request.user
    ).count()

    approved_bookings = Booking.objects.filter(
        user=request.user,
        status="Approved"
    ).count()

    pending_bookings = Booking.objects.filter(
        user=request.user,
        status="Pending"
    ).count()

    context = {
        "total_bookings": total_bookings,
        "total_events": total_events,
        "approved_bookings": approved_bookings,
        "pending_bookings": pending_bookings,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# ==========================
# MY BOOKINGS
# ==========================

@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(user=request.user)

    return render(
        request,
        "dashboard/my_bookings.html",
        {
            "bookings": bookings
        }
    )


# ==========================
# MY EVENTS
# ==========================

@login_required
def my_events(request):

    registrations = EventRegistration.objects.filter(
        user=request.user
    )

    return render(
        request,
        "dashboard/my_events.html",
        {
            "registrations": registrations
        }
    )


# ==========================
# PROFILE
# ==========================

@login_required
def profile(request):

    return render(
        request,
        "dashboard/profile.html"
    )
    
from django.contrib.auth.decorators import login_required

# @login_required
# def my_events(request):

#     registrations = EventRegistration.objects.filter(user=request.user)

#     return render(
#         request,
#         "dashboard/my_events.html",
#         {
#             "registrations": registrations
#         }
#     )
    
    
@login_required
def edit_profile(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = ProfileForm(instance=request.user)

    return render(
        request,
        "dashboard/edit_profile.html",
        {
            "form": form
        }
    )
    
    

from django.contrib.auth.models import User



# ==========================
# ADMIN DASHBOARD
# ==========================

@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("home")

    context = {
    "total_users": User.objects.count(),
    "total_services": Service.objects.count(),
    "total_events": Event.objects.count(),
    "total_bookings": Booking.objects.count(),
    "total_registrations": EventRegistration.objects.count(),
    "total_messages": ContactMessage.objects.count(),
}

    return render(
        request,
        "admin_dashboard/dashboard.html",
        context
    )


# ==========================
# MANAGE BOOKINGS
# ==========================

@staff_member_required
def manage_bookings(request):

    bookings = Booking.objects.all().order_by("-booking_date")

    return render(
        request,
        "admin_dashboard/manage_bookings.html",
        {
            "bookings": bookings
        }
    )


@staff_member_required
def approve_booking(request, id):

    booking = get_object_or_404(Booking, id=id)

    booking.status = "Approved"
    booking.save()

    return redirect("manage_bookings")


@staff_member_required
def cancel_booking(request, id):

    booking = get_object_or_404(Booking, id=id)

    booking.status = "Cancelled"
    booking.save()

    return redirect("manage_bookings")


# ==========================
# MANAGE EVENT REGISTRATIONS
# ==========================

@staff_member_required
def manage_registrations(request):

    registrations = EventRegistration.objects.select_related(
        "event",
        "user"
    )

    return render(
        request,
        "admin_dashboard/manage_registrations.html",
        {
            "registrations": registrations
        }
    )
    
    
from .forms import ServiceForm, EventForm
from django.contrib.admin.views.decorators import staff_member_required

# -----------------------------
# MANAGE SERVICES
# -----------------------------

@staff_member_required
def manage_services(request):

    services = Service.objects.all()

    return render(
        request,
        "admin_dashboard/manage_services.html",
        {
            "services": services
        }
    )


@staff_member_required
def add_service(request):

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("manage_services")

    else:
        form = ServiceForm()

    return render(
        request,
        "admin_dashboard/service_form.html",
        {
            "form": form,
            "title": "Add Service"
        }
    )


@staff_member_required
def edit_service(request, id):

    service = get_object_or_404(Service, id=id)

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)

        if form.is_valid():
            form.save()
            return redirect("manage_services")

    else:
        form = ServiceForm(instance=service)

    return render(
        request,
        "admin_dashboard/service_form.html",
        {
            "form": form,
            "title": "Edit Service"
        }
    )


@staff_member_required
def delete_service(request, id):

    service = get_object_or_404(Service, id=id)

    service.delete()

    return redirect("manage_services")


from .forms import EventForm

@staff_member_required
def manage_events(request):

    events = Event.objects.all()

    return render(
        request,
        "admin_dashboard/manage_events.html",
        {
            "events": events
        }
    )


@staff_member_required
def add_event(request):

    if request.method == "POST":

        form = EventForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()
            return redirect("manage_events")

        else:
            print(form.errors)   # <-- Add this line

    else:
        form = EventForm()

    return render(
        request,
        "admin_dashboard/event_form.html",
        {
            "form": form,
            "title": "Add Event"
        }
    )

@staff_member_required
def edit_event(request, id):

    event = get_object_or_404(Event, id=id)

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES,
            instance=event
        )

        if form.is_valid():

            form.save()

            return redirect("manage_events")

    else:

        form = EventForm(instance=event)

    return render(
        request,
        "admin_dashboard/event_form.html",
        {
            "form": form,
            "title": "Edit Event"
        }
    )


@staff_member_required
def delete_event(request, id):

    event = get_object_or_404(Event, id=id)

    event.delete()

    return redirect("manage_events")

@staff_member_required
def contact_messages(request):

    messages = ContactMessage.objects.all().order_by("-sent_at")

    return render(
        request,
        "admin_dashboard/contact_messages.html",
        {
            "messages": messages
        }
    )
    
@login_required
def event_ticket(request, id):

    registration = get_object_or_404(
        EventRegistration,
        id=id,
        user=request.user
    )

    return render(
        request,
        "tickets/event_ticket.html",
        {
            "registration": registration
        }
    )  

    
