import asyncio

from django.shortcuts import redirect
from django.views.generic import ListView

from main_bot import send_weather
from weather_bot.models import Profile


class HomeView(ListView):
    model = Profile
    template_name = 'weather_bot/home.html'
    ordering = ['first_name']


def send_weather_in_moscow(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    asyncio.run(send_weather(profile.id_user, 'Moscow'))
    return redirect(profile.get_absolute_url())
