from django.urls import path

from .views import HomeView

app_name = 'weather_bot'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
