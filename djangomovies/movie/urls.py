
from django.urls    import path

from .views         import HomeView, MovieDeatilView
# from .views         import home_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('detail/<int:id>/', MovieDeatilView.as_view(), name='moviedetail'),
]
