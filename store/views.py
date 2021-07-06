from django.http import HttpResponse
from .models import ALBUMS
import json

def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def listing(request):
    albums = ["<li>{}</li>".format(album['name']) for album in ALBUMS]
    message = """<ul>{}</ul>""".format("\n".join(albums))
    return HttpResponse(message)

def detail(request, albumId):
  id = int(albumId)
  album = ALBUMS[id]
  artists = ", ".join([artist['name'] for artist in album['artists']])
  message = "Pour l'id {}, le nom de l'album est {}. Il a été écrit par {}".format(albumId, album['name'], artists)
  return HttpResponse(message)

def search(request):
  query = request.GET.get('query')
  if not query:
    message = "Aucun artiste n'est demandé"
  else:
    albums = [album for album in ALBUMS
                if query in " ".join(artist['name'] for artist in album['artists'])
              ]
    if len(albums) == 0:
      message = "Misère de misère, nous n'avons rien trouvé"
    else:
      albums = ["<li>{}</li>".format(album['name']) for album in albums]
      message = """
          Nous avons trouvé les albums correspondant à votre requête ! Les voici :
          <ul>
              {}
          </ul>
      """.format("</li><li>".join(albums))
  return HttpResponse(message)

