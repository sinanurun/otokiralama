from django.forms import ModelForm, TextInput, Textarea, Select

from home.models import ContactMessage
from otomobil.models import Otomobil, Category, Location


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Your Message', 'rows': '5'}),
        }

class SearchForm1(ModelForm):
    class Meta:
        model = Otomobil
        fields = ['category', 'location', 'gear', 'fuel']



