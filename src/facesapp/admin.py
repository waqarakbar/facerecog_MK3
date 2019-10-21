from django.contrib import admin
from .models import Image as ImageModel, Comparison

# Register your models here.
admin.site.register(ImageModel)
admin.site.register(Comparison)