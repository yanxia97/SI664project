from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django_filters.views import FilterView

from .models import Artwork

# Create your views here.

def index(request):
    return HttpResponse("Hello World. You're at the Gallery Artworks index page.")

class AboutPageView(generic.TemplateView):
    template_name = 'artworks/about.html'


class HomePageView(generic.TemplateView):
    template_name = 'artworks/home.html'

class ArtWorkListView(generic.ListView):
    model = Artwork
    context_object_name = 'artwork'
    template_name = 'artworks/artwork.html'
    paginate_by = 50

    def get_queryset(self):
        return Artwork.objects.all().select_related('artist_role').order_by('accession_number')

class ArtWorkDetailView(generic.DetailView):
    model = Artwork
    context_object_name = 'artwork'
    template_name = 'artworks/artwork_detail.html'