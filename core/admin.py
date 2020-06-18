from django.contrib import admin
from core import models

# Register your models here.
# change admin site view
admin.site.site_title = "wkapp"
admin.site.site_header = "wkapp"
admin.site.index_title = "wkapp"

# Register your models here.
admin.site.register(models.Content)
