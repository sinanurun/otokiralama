from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request

# Create your views here.
from otomobil.models import Otomobil, Category
from home.forms import ContactForm, SearchForm1
from home.models import Setting, FAQ, ContactMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    otomobil_slider = Otomobil.objects.filter(status=True).order_by('-id')[:4]  # last 4
    category = Category.objects.filter(status=True).all()
    otomobil_picked = Otomobil.objects.all().order_by('?')[:4]  # Random selected 4
    sform1 = SearchForm1()
    context = {'setting': setting,
               'sliderdata': otomobil_slider,
               'otomobils_picked': otomobil_picked,
               'category': category,
               'sform1':sform1}
    return render(request, "index.html", context)
    """aşağıdaki kısım direk bir içerik döndürmek için yukarıdaki kısım ise
     bir html view döndürmek için """
    # return HttpResponse("Karşılama Sayfası %s." % text)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    sform1 = SearchForm1()
    context = {'setting': setting,
               'category': category,
               'sform1':sform1}
    return render(request, "aboutus.html", context)


def contact(request):
    category = Category.objects.all()
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    form = ContactForm
    setting = Setting.objects.get(pk=1)
    sform1 = SearchForm1()
    context = {'setting': setting,
               'category': category,
               'form': form,
               'sform1':sform1}
    return render(request, 'contact.html', context)


def referances(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    sform1 = SearchForm1()
    context = {'setting': setting,
               'category': category,
               'sform1':sform1}
    return render(request, "referances.html", context)


def faq(request):
    faq = FAQ.objects.filter(status="True")
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    sform1 = SearchForm1()
    context = {'setting': setting,
               'category': category,
               'faq': faq,
               'sform1':sform1,
               }
    return render(request, 'fag.html', context)
