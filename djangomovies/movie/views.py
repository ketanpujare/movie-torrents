from django.shortcuts import render

from django.contrib.auth.mixins     import LoginRequiredMixin
from django.views.generic           import ListView

from .models                        import Movie, Genre

# Create your views here.


class HomeView(ListView):
    model = Movie
    ordering = ['-movie_year', 'movie_name']
    template_name = 'index.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        queryset = Genre.objects.filter(genre="Comedy")[0].movies.all()
        return queryset