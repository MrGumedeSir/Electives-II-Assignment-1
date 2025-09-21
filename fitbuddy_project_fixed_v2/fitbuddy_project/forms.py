from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password','password2')

class ActivityLogForm(forms.Form):
    title = forms.CharField(max_length=200)
    duration_minutes = forms.IntegerField(min_value=1, initial=10)

class HydrationForm(forms.Form):
    amount_ml = forms.IntegerField(min_value=10, initial=250)
class ReminderForm(forms.Form):
    message = forms.CharField(max_length=255)
    remind_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))