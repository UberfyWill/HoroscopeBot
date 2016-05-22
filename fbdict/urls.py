from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'bot.views.home', name='home'),
    url(r'^webhook', 'bot.views.webhook', name='webhook'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^get_horoscope', 'bot.views.get_horoscope', name='get_horoscope'),
    url(r'^admin/', include(admin.site.urls)),
]
