from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import ModelForm, TextInput, FileInput, Select
from django import forms
from otomobil.models import Otomobil, Category, Location


class OtomobilForm(ModelForm):
    class Meta:
        model = Otomobil

        fields = ['category', 'location', 'title', 'keywords', 'description', 'image',
                  'price', 'detail', 'slug']
        widgets = {
            'category': Select(attrs={'class': 'input', 'placeholder': 'Category'}, choices=Category.objects.all()),
            'location': Select(attrs={'class': 'input', 'placeholder': 'Location'}, choices=Location.objects.all()),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Title'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'Keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'Description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'Image', }),
            'price': TextInput(attrs={'class': 'input', 'placeholder': 'Price'}),
            'detail': CKEditorUploadingWidget(),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
        }

class SearchForm2(ModelForm):
    baslangic = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))
    bitis = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))
    class Meta:
        model = Otomobil

        fields = ['category', 'location', 'gear', 'fuel',
                  'daily_km','price','baslangic','bitis','min_li_age']


class RezForm(ModelForm):
    baslangic = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))
    bitis = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))
    class Meta:
        model = Otomobil
        fields = ['baslangic','bitis']
