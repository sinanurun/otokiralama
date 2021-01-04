from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Create your models here.


# otomobiller ve kategorileri için
from django.forms import ModelForm, TextInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Location(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    # def get_absolute_url(self):
    #     return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    # def get_absolute_url(self):
    #     return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


# otomobiller için

class Otomobil(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    VITES = (
        ('Duz', 'Düz'),
        ('Otomatik', 'Otomatik'),
        ('Triptonik', 'Triptonik'),
    )
    YAKIT = (
        ('Benzin', 'Benzin'),
        ('Dizel', 'Dizel'),
        ('Lpg','Lpg')
    )
    MAX_DAILY_KM = (
        (250, '250 Km'),
        (500, '500 Km'),
        (750,'750 Km'),
        (1000,'1000 Km'),
        (1250, '1250 Km'),
        (1500, '1500 Km')
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='None')  # many to one relation with Category
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default='None')  # many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True)
    gear = models.CharField(max_length=10, choices=VITES, default='Duz')
    fuel = models.CharField(max_length=10, choices=YAKIT, default='Benzin')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    min_age = models.IntegerField(default=18)
    min_cc = models.IntegerField(default=1)
    min_li_age = models.IntegerField(default=0)
    min_person = models.IntegerField(default=1)
    big_baggage = models.IntegerField(default=0)
    small_baggage = models.IntegerField(default=0)
    daily_km = models.IntegerField(choices=MAX_DAILY_KM, default=250)
    abs = models.CharField(max_length=10, choices=STATUS, default='False')
    driver_airbag = models.CharField(max_length=10, choices=STATUS, default='True')
    passenger_airbag = models.CharField(max_length=10, choices=STATUS, default='True')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    ## method to create a fake table field in read only mode
    def image_tag2(self):
        if self.image.url is not None:
            return mark_safe('{}'.format(self.image.url))
        else:
            return ""


class Images(models.Model):
    otomobil = models.ForeignKey(Otomobil, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="250"/>'.format(self.image.url))
        else:
            return ""

    ## method to create a fake table field in read only mode
    def image_tag2(self):
        if self.image.url is not None:
            return mark_safe('{}'.format(self.image.url))
        else:
            return ""

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    otomobil = models.ForeignKey(Otomobil, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


class Kira(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    otomobil = models.ForeignKey(Otomobil, on_delete=models.CASCADE, default='None')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rezdate = models.DateField()
    returndate = models.DateField()
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    days = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    def __str__(self):
        return self.otomobil.title

    def cat(self):
        return self.otomobil.category

    def _get_days(self):
        if self.days == 0:
            self.days = (self.returndate - self.rezdate).days
            super().save()
        return self.days


    def _get_total(self):
        if self.total == 0:
            self.total = (self.returndate - self.rezdate).days * self.otomobil.price
            super().save()
        return self.total


