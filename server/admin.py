from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Store)
admin.site.register(ProductType)
admin.site.register(Inventory)
admin.site.register(SalesRecord)