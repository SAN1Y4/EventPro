from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name


class Event(models.Model):

    title = models.CharField(max_length=150)

    organizer = models.CharField(max_length=150)

    # service = models.ForeignKey(Service, on_delete=models.CASCADE)

    location = models.CharField(max_length=150)

    date = models.DateField()

    time = models.TimeField()

    description = models.TextField()

    image = models.ImageField(upload_to='events/')

    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)

    total_tickets = models.PositiveIntegerField()

    available_tickets = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title


class Booking(models.Model):

    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    # Logged-in user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
    max_length=10,
    validators=[phone_validator]
)

    preferred_date = models.DateField()

    guest_count = models.PositiveIntegerField()

    location = models.CharField(max_length=200)

    budget = models.DecimalField(max_digits=10, decimal_places=2)

    special_request = models.TextField(blank=True)

    booking_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    def __str__(self):
        return f"{self.customer_name} - {self.service.name}"


class EventRegistration(models.Model):

    # Logged-in user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
    max_length=10,
    validators=[phone_validator]
)

    number_of_tickets = models.PositiveIntegerField(default=1)

    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"
    

class ContactMessage(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    subject = models.CharField(max_length=200)

    message = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject