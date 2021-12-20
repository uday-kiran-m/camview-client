from django.contrib import admin
from . import models
# Register your models here.
class Cam(admin.ModelAdmin):
    list_display = ('camname','url','note')
admin.site.register(models.cams,Cam)

admin.site.site_header = "Camview"