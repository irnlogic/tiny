from django.shortcuts import render

from django.http import HttpResponse
from tinyurl.models import Url 
from .lib.tiny import UrlHandler


def index(request):
	return HttpResponse("Hello, this is the famous tinyurl app")


# Create your views here.
def url_detail_view(request):
    url = Url.objects.get(id=1)
    context = {'originalurl': url.originalurl}
    #context = {'object': url}
    return render(request, "detail.html", context)

ORIGINAL_URL = 'originalurl'
TINY_URL = 'tinyurl'
def url_tiny(request):
    print (request.GET[ORIGINAL_URL])
    originalurl = None
    if ORIGINAL_URL in request.GET:
        originalurl = request.GET[ORIGINAL_URL]
    else:
        if ORIGINAL_URL in request.POST:
            originalurl = request.POST[ORIGINAL_URL]

    if originalurl:
        tinyurl = UrlHandler.get_tinyurl(originalurl)
        context = {ORIGINAL_URL: originalurl, 'tinyurl': tinyurl}
    else:
        context = {ORIGINAL_URL: originalurl, 'tinyurl': ''}
    return render(request, "tiny.json", context)
    

def url_original(request):
    tinyurl = request.GET.get(ORIGINAL_URL)
    context = {}
    context[TINY_URL] = None
    context[ORIGINAL_URL] = None
    if not tinyurl:
        tinyurl = request.POST.get(ORIGINAL_URL)

    if tinyurl:
        context[TINY_URL] = tinyurl
        context[ORIGINAL_URL] = UrlHandler.get_originalurl(tinyurl)
 
    return render(request, "tiny.json", context)



