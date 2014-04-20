from django.shortcuts import render_to_response, HttpResponse
from django.db.models import Q, Max

from oge.models import *



def index(request):

    lastchecked = Official.objects.all().aggregate(lastchecked=Max('lastchecked'))['lastchecked']

    if not request.GET or not request.GET['q'] or len(request.GET['q'])<3:
        q = ''
        results = Document.objects.all().order_by('-date')[:60]

    else:    
        q = request.GET['q']
        results = Document.objects.search(q)
                                   
    return render_to_response('oge_index.html', {'results': results, 'q': q, 'updated': lastchecked })



def text(request,id):

    lastchecked = Official.objects.all().aggregate(lastchecked=Max('lastchecked'))['lastchecked']

    o = Official.objects.get(pk=id)
    q = o.name
    
    results = o.document_set.all().order_by('-date')
                               
    return render_to_response('oge_index.html', {'results': results, 'q': q, 'updated': lastchecked })
           


