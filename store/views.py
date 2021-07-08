from django.shortcuts import render, get_object_or_404
from .models import Album, Contact, Booking
from .forms import ContactForm, ParagraphErrorList
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError

@transaction.non_atomic_requests
def index(request):
  albums = Album.objects.filter(available=True).order_by('-created_at')[:3]
  context = {'albums':albums}
  return render(request, 'store/index.html', context)

def listing(request):
  albums_list = Album.objects.filter(available=True)
  paginator = Paginator(albums_list, 6)
  page = request.GET.get('page')
  try:
    albums = paginator.page(page)
  except PageNotAnInteger:
    albums = paginator.page(1)
  except EmptyPage:
    albums = paginator.page(paginator.num_pages)
  context = {'albums':albums, 'paginate':True}
  return render(request, 'store/listing.html', context)

@transaction.atomic
def detail(request, albumId):
  album = get_object_or_404(Album, pk=albumId)
  artists = [artist.name for artist in album.artists.all()]
  artistsName = ", ".join(artists)
  context = {'album_title': album.title, 'artists_name': artistsName, 'album_id':albumId, 'thumbnail':album.picture}
  if request.method == 'POST':
    form = ContactForm(request.POST, error_class=ParagraphErrorList)
    if form.is_valid():
      email = form.cleaned_data['email']
      name = form.cleaned_data['name']
      try:
        with transaction.atomic():
          contact = Contact.objects.filter(email=email)
          if not contact.exists():
            contact = Contact.objects.create(email=email, name=name)
          else:
            contact = contact.first()
          album = get_object_or_404(Album, id=albumId)
          Booking.objects.create(contact=contact, album=album)

          album.available = False
          album.save()
          context = {'album_title': album.title}
          return render(request, 'store/thankyou.html', context)
      except IntegrityError:
        form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."
    context['errors'] = form.errors.items()
  else:
    form = ContactForm()
  context['form'] = form
  return render(request, 'store/detail.html', context)

def search(request):
  query = request.GET.get('query')
  if not query:
    albums = Album.objects.all()
  else:
    albums = Album.objects.filter(title__icontains = query)
  if not albums.exists():
    albums = Album.objects.filter(artists__name__icontains = query)
  title = "Résultats pour la requête %s"%query
  context = {
    'albums': albums,
    'title': title
  }
  return render(request, 'store/search.html', context)

