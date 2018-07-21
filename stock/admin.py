from django.contrib import admin
from stock.models import Menu, Name, Pricedaily, Bigexchange

# Register your models here.
admin.site.register(Menu)
admin.site.register(Name)
admin.site.register(Pricedaily)
admin.site.register(Bigexchange)