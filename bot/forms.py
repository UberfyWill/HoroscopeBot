from django import forms

from .models import Horoscope


class HoroscopeForm(forms.ModelForm):
	class Meta:
		model = Horoscope
		fields = ['horoscope_date', 'sign', 'horoscope']
		### exclude = ['full_name']