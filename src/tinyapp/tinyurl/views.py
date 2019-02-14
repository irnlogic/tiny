from django.shortcuts import render

from django.http import HttpResponse
from tinyurl.models import Url 
from .lib.tiny import UrlHandler


def index(request):
	return HttpResponse("""
            <p> Usage: 
            <p> Shorten      ==> http://localhost:8000/tinyurl/tinyurl/?originalurl=ibm.com
            <p> Original Url ==> http://localhost:8000/tinyurl/originalurl/?tinyurl=9kexw
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
def url_tiny1(request):
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

def url_tiny(request):
    print ("url_tiny")
    originalurl = get_param_from_request(request, ORIGINAL_URL)

    if originalurl:
        tinyurl = UrlHandler.get_tinyurl(originalurl)
        context = {ORIGINAL_URL: originalurl, 'tinyurl': tinyurl}
    else:
        context = {ORIGINAL_URL: originalurl, 'tinyurl': ''}
    return render(request, "tiny.json", context)
  

def url_original(request):
    print('url_orginal')
    tinyurl = get_param_from_request(request, TINY_URL)
    context = {}
    context[TINY_URL] = None
    context[ORIGINAL_URL] = None

    print(tinyurl)
    if tinyurl:
        context[TINY_URL] = tinyurl
        context[ORIGINAL_URL] = UrlHandler.get_originalurl(tinyurl)
 
    return render(request, "tiny.json", context)



def get_param_from_request(request, key):
    print ("getParamFromRequest. GET = {} \n POST {} \n".format(request.GET, request.POST) )

    ret = None
    if key in request.GET:
        ret = request.GET[key]
    else:
        if key in request.POST:
            ret = request.POST[key]

    return ret