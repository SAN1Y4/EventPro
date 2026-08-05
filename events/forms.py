
from django import forms
from .models import Booking, EventRegistration
class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            'service',
            'customer_name',
            'email',
            'phone',
            'preferred_date',
            'guest_count',
            'location',
            'budget',
            'special_request',
        ]

        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'special_request': forms.Textarea(attrs={'rows': 4}),
        }
class EventRegistrationForm(forms.ModelForm):

    phone = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "maxlength": "10",
            "pattern": "[0-9]{10}",
            "placeholder": "Enter 10-digit phone number"
        })
    )

    class Meta:
        model = EventRegistration

        fields = [
            "full_name",
            "email",
            "phone",
            "number_of_tickets",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "number_of_tickets": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return phone

from .models import ContactMessage

class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }),

            "subject": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Subject"
            }),

            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write your message"
            }),
        }
from .models import Service, Event

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            "title",
            "organizer",
            "location",
            "date",
            "time",
            "description",
            "ticket_price",
            "total_tickets",
            "available_tickets",
            "image",
            "is_active",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"     

from django.contrib.auth.models import User
from django import forms

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
        }  
        
