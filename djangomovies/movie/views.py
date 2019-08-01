from django.shortcuts import render

from django.contrib.auth.mixins     import LoginRequiredMixin
from django.views.generic           import ListView

from .models                        import Movie

# Create your views here.


class HomeView(ListView):
    paginate_by = 20
    ordering = ['-movie_year', 'movie_name']
    template_name = 'index.html'
    queryset = Movie.objects.all()


