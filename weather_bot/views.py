from django.views.generic import ListView

from weather_bot.models import Profile


class HomeView(ListView):
    model = Profile
    template_name = 'weather_bot/home.html'
    ordering = ['id_user']
