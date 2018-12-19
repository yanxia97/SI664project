from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django_filters.views import FilterView

from .models import Artwork, Artist

# Create your views here.

def index(request):
    return HttpResponse("Hello World. You're at the Gallery Artworks index page.")

class AboutPageView(generic.TemplateView):
    template_name = 'artworks/about.html'


class HomePageView(generic.TemplateView):
    template_name = 'artworks/home.html'

# @method_decorator(login_required, name='dispatch')
class ArtWorkListView(generic.ListView):
    model = Artwork
    context_object_name = 'artworks'
    template_name = 'artworks/artwork.html'
    paginate_by = 500

    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Artwork.objects.all().select_related('artist_role').order_by('accession_number')

# @method_decorator(login_required, name='dispatch')
class ArtWorkDetailView(generic.DetailView):
    model = Artwork
    context_object_name = 'artwork'
    template_name = 'artworks/artwork_detail.html'

    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ArtistListView(generic.ListView):
    model = Artist
    context_object_name = 'artists'
    template_name = 'artworks/artist.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Artist.objects\
            .select_related('gender')\
            .order_by('artist_name')

@method_decorator(login_required, name='dispatch')          
class ArtistDetailView(generic.DetailView):
    model = Artist
    context_object_name = 'artist'
    template_name = 'artworks/artist_detail.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# @method_decorator(login_required, name='dispatch')
# class ArtWorkCreateView(generic.View):
#     model = Artwork
#     form_class = HeritageSiteForm
#     success_message = "Heritage Site created successfully"
#     template_name = 'heritagesites/site_new.html'
#     # fields = '__all__' <-- superseded by form_class
#     # success_url = reverse_lazy('heritagesites/site_list')

#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request):
#         form = HeritageSiteForm(request.POST)
#         if form.is_valid():
#             site = form.save(commit=False)
#             site.save()
#             for country in form.cleaned_data['country_area']:
#                 HeritageSiteJurisdiction.objects.create(heritage_site=site, country_area=country)
#             return redirect(site) # shortcut to object's get_absolute_url()
#             # return HttpResponseRedirect(site.get_absolute_url())
#         return render(request, 'heritagesites/site_new.html', {'form': form})

#     def get(self, request):
#         form = HeritageSiteForm()
#         return render(request, 'heritagesites/site_new.html', {'form': form})

# @method_decorator(login_required, name='dispatch')
# class SiteUpdateView(generic.UpdateView):
#     model = HeritageSite
#     form_class = HeritageSiteForm
#     # fields = '__all__' <-- superseded by form_class
#     context_object_name = 'site'
#     # pk_url_kwarg = 'site_pk'
#     success_message = "Heritage Site updated successfully"
#     template_name = 'heritagesites/site_update.html'

#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def form_valid(self, form):
#         site = form.save(commit=False)
#         # site.updated_by = self.request.user
#         # site.date_updated = timezone.now()
#         site.save()

#         # Current country_area_id values linked to site
#         old_ids = HeritageSiteJurisdiction.objects\
#             .values_list('country_area_id', flat=True)\
#             .filter(heritage_site_id=site.heritage_site_id)

#         # New countries list
#         new_countries = form.cleaned_data['country_area']

#         # TODO can these loops be refactored?

#         # New ids
#         new_ids = []

#         # Insert new unmatched country entries
#         for country in new_countries:
#             new_id = country.country_area_id
#             new_ids.append(new_id)
#             if new_id in old_ids:
#                 continue
#             else:
#                 HeritageSiteJurisdiction.objects \
#                     .create(heritage_site=site, country_area=country)

#         # Delete old unmatched country entries
#         for old_id in old_ids:
#             if old_id in new_ids:
#                 continue
#             else:
#                 HeritageSiteJurisdiction.objects \
#                     .filter(heritage_site_id=site.heritage_site_id, country_area_id=old_id) \
#                     .delete()

#         return HttpResponseRedirect(site.get_absolute_url())
#         # return redirect('heritagesites/site_detail', pk=site.pk)

# @method_decorator(login_required, name='dispatch')
# class SiteDeleteView(generic.DeleteView):
#     model = HeritageSite
#     success_message = "Heritage Site deleted successfully"
#     success_url = reverse_lazy('site')
#     context_object_name = 'site'
#     template_name = 'heritagesites/site_delete.html'

#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()

#         # Delete HeritageSiteJurisdiction entries
#         HeritageSiteJurisdiction.objects \
#             .filter(heritage_site_id=self.object.heritage_site_id) \
#             .delete()

#         self.object.delete()

#         return HttpResponseRedirect(self.get_success_url())

# class SiteFilterView(FilterView):
#     filterset_class = HeritageSiteFilter
#     template_name = 'heritagesites/site_filter.html'