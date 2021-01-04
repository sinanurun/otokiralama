from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm1
from otomobil.forms import SearchForm2, RezForm
from otomobil.models import Category, Otomobil, Images, Comment, CommentForm, Kira
from home.models import Setting
import datetime

def category_otomobils(request, id, slug):
    setting = Setting.objects.get(pk=1)
    catdata = Category.objects.get(pk=id)
    otomobils = Otomobil.objects.filter(category_id=id,status=True)
    category = Category.objects.all()
    sform1 = SearchForm1()
    context = {'otomobils': otomobils,
               'category': category,
               'catdata': catdata,
               'setting':setting,
               'sform1':sform1,}
    return render(request, 'category.html', context)

def otomobil_details(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.filter(status=True).all()
    otomobil = Otomobil.objects.get(pk=id)
    images = Images.objects.filter(otomobil=id).all()
    comments = Comment.objects.filter(otomobil=id, status=True).all()
    sform1 = SearchForm1()
    rezform = RezForm()
    context = {'setting': setting,
               'otomobil': otomobil,
               'comments': comments,
               'images': images,
               'category': category,
               'sform1':sform1,
               'rezform':rezform,
               }
    return render(request, 'otomobil_details.html', context)

def otomobils_search(request,id=0):
    sform1 = SearchForm1()
    sform2= SearchForm2()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    if request.method == 'POST' and id == 0:  # check post
        form = SearchForm1(request.POST)
        if form.is_valid():
            otomobils = Otomobil.objects.filter(category=form.cleaned_data['category'],
                                                location=form.cleaned_data['location'],
                                                gear=form.cleaned_data['gear'],
                                                fuel=form.cleaned_data['fuel'],
                                                status=True)


    if request.method == 'POST' and id == 1:
        arabalar = []
        form = SearchForm2(request.POST)
        if form.is_valid():
            otomobils = Otomobil.objects.filter(category=form.cleaned_data['category'],
                                                location=form.cleaned_data['location'],
                                                gear=form.cleaned_data['gear'],
                                                fuel=form.cleaned_data['fuel'],
                                                daily_km__lte=form.cleaned_data['daily_km'],
                                                price__lte=form.cleaned_data['price'],
                                                status=True)

            for otomobil in otomobils:
                baslangic=form.cleaned_data['baslangic']
                print(type(baslangic))
                bitis=form.cleaned_data['bitis']
                kiralar = Kira.objects.filter(otomobil=otomobil,status=True)
                kira_say = kiralar.__len__()
                a = 0
                for kira in kiralar:
                    if (baslangic < kira.rezdate and bitis < kira.rezdate) or (
                            baslangic > kira.rezdate and baslangic > kira.returndate):
                        a = a + 1
                if a != kira_say:
                    arabalar.append(otomobil)

        otomobils = arabalar


    elif id == 1:
        otomobils = Otomobil.objects.filter(status=True)


    context = {'otomobils': otomobils,
               'category': category,
               'setting':setting,
               'sform1':sform1,
               'sform2':sform2,}
    return render(request, 'search.html', context)

def addrezervation(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = RezForm(request.POST)
      if form.is_valid():
          otomobil = Otomobil.objects.filter(id=id)
          baslangic = form.cleaned_data['baslangic']
          print(type(baslangic))
          bitis = form.cleaned_data['bitis']
          kiralar = Kira.objects.filter(otomobil=otomobil, status=True)
          try:
              kira_say = kiralar.__len__()

              a = 0
              for kira in kiralar:
                  if (baslangic < kira.rezdate and bitis < kira.rezdate) or (
                          baslangic > kira.rezdate and baslangic > kira.returndate):
                      a = a + 1
              if a != kira_say:
                  pass
          except:
              data = Kira()  # create relation with model
              data.rezdate = form.cleaned_data['baslangic']
              data.returndate = form.cleaned_data['bitis']
              data.ip = request.META.get('REMOTE_ADDR')
              data.otomobil_id = id
              current_user = request.user
              data.user_id = current_user.id
              data.save()  # save data to table
              messages.success(request, "Your rezervation is done. Thank you for your interest.")
              return HttpResponseRedirect(url)
   return HttpResponseRedirect(url)

def addcomment(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = CommentForm(request.POST)
      if form.is_valid():
         data = Comment()  # create relation with model
         data.subject = form.cleaned_data['subject']
         data.comment = form.cleaned_data['comment']
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.otomobil_id=id
         current_user= request.user
         data.user_id=current_user.id
         data.save()  # save data to table
         messages.success(request, "Your review has ben sent. Thank you for your interest.")
         return HttpResponseRedirect(url)

   return HttpResponseRedirect(url)