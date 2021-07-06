from django.http import HttpResponse
from .models import Album

message = "Salut tout le monde !"

def index(request):
  albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
  formattedAlbums = ["<li>{}</li>".format(album.title) for album in albums]
  message = """<ul>{}</ul>""".format("\n".join(formattedAlbums))
  return HttpResponse(message)

def listing(request):
  albums = Album.objects.filter(available=True)
  formattedAlbums = ["<li>{}</li>".format(album.title) for album in albums]
  message = """<ul>{}</ul>""".format("\n".join(formattedAlbums))
  return HttpResponse(message)

def detail(request, albumId):
  album = Album.objects.get(pk=albumId)
  artists = ", ".join([artist.name for artist in album.artists.all()])
  message = "Pour l'id {}, le nom de l'album est {}. Il a été écrit par {}".format(albumId, album.title, artists)
  return HttpResponse(message)

def search(request):
  query = request.GET.get('query')
  if not query:
    albums = Album.objects.all()
  else:
    albums = Album.objects.filter(title__icontains = query)
  if not albums.exists():
    albums = Album.objects.filter(artists__name__icontains = query)
  if not albums.exists():
    message = "Misère de misère, nous n'avons rien trouvé"
  else:
    albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """
        Nous avons trouvé les albums correspondant à votre requête ! Les voici :
        <ul>{}</ul>
    """.format("\n".join(albums))
  return HttpResponse(message)

