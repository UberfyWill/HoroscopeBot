from django.contrib import admin
# Register your models here.

from .forms import HoroscopeForm
from .models import Horoscope

class HoroscopeAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "horoscope_date", "sign", "horoscope"]
	form = HoroscopeForm
	# class Meta:
	# 	model = SignUp



admin.site.register(Horoscope, HoroscopeAdmin)
