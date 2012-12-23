from django.shortcuts import render_to_response, HttpResponse, redirect

from quarterback.oge.models import *


def index(request):

    if request.GET and request.GET['q'] and len(request.GET['q'])>2:
        q = request.GET['q']
        results = Document.objects.filter(text__icontains=q).order_by('-date')
    else:
        q = ''
        results = Document.objects.all().order_by('-date')
           
    return render_to_response('oge_index.html', {'results': results, 'q': q })

