from io import BytesIO

from django.contrib import admin

# Register your models here.
from django.http import FileResponse, HttpResponse
from mptt.admin import DraggableMPTTAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from otomobil.models import Category, Otomobil, Location, Images, Comment, Kira



def make_published(modeladmin, request, queryset):
    queryset.update(status='True')
make_published.short_description = "Mark selected stories as published"


def some_view(modeladmin,request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    print(queryset)
    a = 20
    for kira in queryset:
        bilgiler = [kira.user.username, kira.otomobil.title, str(kira.rezdate), str(kira.returndate), kira.total]
        p.drawString(20, a, str(bilgiler))
        a = a + 40
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
some_view.short_description = "pdf create"



class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_otomobils_count', 'related_otomobils_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [Category]
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Otomobil,
                'category',
                'otomobils_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Otomobil,
                 'category',
                 'otomobils_count',
                 cumulative=False)
        return qs

    def related_otomobils_count(self, instance):
        return instance.otomobils_count
    related_otomobils_count.short_description = 'Related otomobils (for this specific category)'

    def related_otomobils_cumulative_count(self, instance):
        return instance.otomobils_cumulative_count
    related_otomobils_cumulative_count.short_description = 'Related otomobils (in tree)'

admin.site.register(Category, CategoryAdmin2)

class LocationAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_otomobils_count', 'related_otomobils_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [Category]
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Location.objects.add_related_count(
                qs,
                Otomobil,
                'location',
                'otomobils_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Location.objects.add_related_count(qs,
                 Otomobil,
                 'location',
                 'otomobils_count',
                 cumulative=False)
        return qs

    def related_otomobils_count(self, instance):
        return instance.otomobils_count
    related_otomobils_count.short_description = 'Related otomobils (for this specific location)'

    def related_otomobils_cumulative_count(self, instance):
        return instance.otomobils_cumulative_count
    related_otomobils_cumulative_count.short_description = 'Related otomobils (in tree)'

admin.site.register(Location, LocationAdmin2)



class OtomobilImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('image_tag',)
    extra = 5


class OtomobilAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'status', 'category']
    list_filter = ['status', 'category']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [OtomobilImageInline]

admin.site.register(Otomobil, OtomobilAdmin)


class KiraAdmin(admin.ModelAdmin):
    list_display = ['user','otomobil','_get_total','_get_days', 'status','cat','rezdate','returndate']
    list_filter = ['otomobil__category',
        ('rezdate', DateRangeFilter), ('returndate', DateTimeRangeFilter),
    ]
    search_fields = ['user__username','otomobil__category__title']
    actions = [make_published, some_view]


admin.site.register(Kira, KiraAdmin)


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','otomobil','image_tag']

admin.site.register(Images,ImagesAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status','create_at']
    list_filter = ['status']
    readonly_fields = ('subject','comment','ip','user','otomobil','rate','id')

admin.site.register(Comment,CommentAdmin)

