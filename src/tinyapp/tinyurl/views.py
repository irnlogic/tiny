from django.shortcuts import render

from django.http import HttpResponse
from tinyurl.models import Url 
from .lib.tiny import UrlHandler


## display help
def index(request):
	return HttpResponse("""
            <p> Usage: 
            <p> Shorten      ==> http://localhost:8000/maketiny/www.ibm.com
            <p> Original Url ==> http://localhost:8000/25t52/
            """
            )


# Create your views here.
def url_detail_view(request):
    url = Url.objects.get(id=1)
    context = {'originalurl': url.originalurl}
    #context = {'object': url}
    return render(request, "detail.html", context)

ORIGINAL_URL = 'originalurl'
TINY_URL = 'tinyurl'

## make tiny url
def make_tiny(request, url=None):
    if url:
        tinyurl = UrlHandler.get_tinyurl(url)
        context = {ORIGINAL_URL: url, 'tinyurl': get_full_url(request, tinyurl) }
    else:
        context = {ORIGINAL_URL: url, 'tinyurl': ''}

    return render(request, "maketiny.json", context)
  
## given the url code return tinyurl
def get_original(request, tinycode=None):
    context = {}
    context[TINY_URL] = ''
    context[ORIGINAL_URL] = ''

    if tinycode:
        tinyurl = get_full_url(request, tinycode)
        if tinycode:
            context[TINY_URL] = tinyurl if tinyurl else ''
            original_url = UrlHandler.get_originalurl(tinycode)
            context[ORIGINAL_URL] = original_url if original_url else ''
        else:
            print("Invalid url code")
    else:
        print ("Missing url code")

    return render(request, "geturl.json", context)

def get_full_url (request, path):
    return  request.scheme + "://" +  request.get_host() + "/" + path

def get_param_from_request(request, key):
    print ("getParamFromRequest. GET = {} \n POST {} \n".format(request.GET, request.POST) )

    ret = None
    if key in request.GET:
        ret = request.GET[key]
    else:
        if key in request.POST:
            ret = request.POST[key]

    return ret