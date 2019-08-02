from django.shortcuts import render, get_object_or_404

from django.http       import HttpResponse

from django.contrib.auth.mixins     import LoginRequiredMixin
from django.views.generic           import ListView, DetailView

from .models                        import Movie, Genre

# Create your views here.


class HomeView(ListView):
    model = Movie
    ordering = ['-movie_year','movie_name']
    paginate_by = 12
    template_name = 'index.html'

    def get(self, request):
        self.object_list = self.get_queryset()
        context = super(HomeView, self).get_context_data(object_list=self.object_list)
        context['genres'] = Genre.objects.all()
        return render(request, self.template_name, context)

    def post(self, request):
        genrekey = request.POST['genrekey']
        genre_movie_list = Genre.objects.filter(pk=genrekey)[0].movies.all()
        context = super(HomeView, self).get_context_data(object_list=genre_movie_list)
        context['genres'] = Genre.objects.all()
        return render(request, self.template_name, context)


class MovieDeatilView(DetailView):
    model = Movie
    template_name = 'detail.html'

    def get_object(self):
        return get_object_or_404(Movie, id=self.kwargs.get("id"))