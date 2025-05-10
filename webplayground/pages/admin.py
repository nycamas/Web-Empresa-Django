from django.contrib import admin
from .models import Page

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

# Inyectamos nuestro fichero css para que se viera en el panel admin
#    class Media:
#        css = {
#           'all': ('pages/css/custom_ckeditor.css',)
#        }
        
admin.site.register(Page, PageAdmin)
