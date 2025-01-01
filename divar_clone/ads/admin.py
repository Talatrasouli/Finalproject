from django.contrib import admin
from .models import Category,City,Advertisement

# Register your models here.
@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display=('title','slug')
    search_fields=('title','slug',' parent')
    prepopulated_fields={
        'slug':('title',)
    }

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('name',)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display=['title','category','created_at']
    list_filter=['title','category','created_at']
    search_fields=['title','category','created_at','overview']
    prepopulated_fields={
        'slug':('title',)
    }