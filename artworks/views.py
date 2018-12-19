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
from .forms import ArtworkForm
from .models import ArtworkSubject

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

@method_decorator(login_required, name='dispatch')
class ArtWorkCreateView(generic.View):
    model = Artwork
    form_class = ArtworkForm
    success_message = "Artwork created successfully"
    template_name = 'artworks/artwork_new.html'
    # fields = '__all__' <-- superseded by form_class
    # success_url = reverse_lazy('artworks/site_list')

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        form = ArtworkForm(request.POST)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.save()
            for subject in form.cleaned_data['subject']:
                ArtworkSubject.objects.create(Artwork=artwork, Subject=subject)
            return redirect(artwork) # shortcut to object's get_absolute_url()
            # return HttpResponseRedirect(artwork.get_absolute_url())
        return render(request, 'artworks/artwork_new.html', {'form': form})

    def get(self, request):
        form = ArtworkForm()
        return render(request, 'artworks/artwork_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ArtWorkUpdateView(generic.UpdateView):
    model = Artwork
    form_class = ArtworkForm
    # fields = '__all__' <-- superseded by form_class
    context_object_name = 'artwork'
    # pk_url_kwarg = 'artwork_pk'
    success_message = "Artwork updated successfully"
    template_name = 'artworks/artwork_update.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        artwork = form.save(commit=False)
        # site.updated_by = self.request.user
        # site.date_updated = timezone.now()
        artwork.save()

        # Current subject_id values linked to site
        old_ids = ArtworkSubject.objects\
            .values_list('subject_id', flat=True)\
            .filter(artwork_id=artwork.artwork_id)

        # New subject list
        new_subjects = form.cleaned_data['subject']

        # New ids
        new_ids = []

        # Insert new unmatched subject entries
        for subject in new_subjects:
            new_id = subject.subject_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                ArtworkSubject.objects \
                    .create(artwork=artwork, subject=subject)

        # Delete old unmatched subject entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                ArtworkSubject.objects \
                    .filter(artwork_id=artwork.artwork_id, subject_id=old_id) \
                    .delete()

        return HttpResponseRedirect(artwork.get_absolute_url())
        # return redirect('artworks/artwork_detail', pk=site.pk)

@method_decorator(login_required, name='dispatch')
class ArtWorkDeleteView(generic.DeleteView):
    model = Artwork
    success_message = "Artwork deleted successfully"
    success_url = reverse_lazy('artwork')
    context_object_name = 'artwork'
    template_name = 'artworks/artwork_delete.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Delete ArtworkSubject entries
        ArtworkSubject.objects \
            .filter(artwork_id=self.object.artwork_id) \
            .delete()

        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

# class SiteFilterView(FilterView):
#     filterset_class = HeritageSiteFilter
#     template_name = 'heritagesites/site_filter.html'