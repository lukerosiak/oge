from django.shortcuts import render_to_response, HttpResponse, redirect
from django.template import loader, Context

from quarterback.oge.models import *
from quarterback.oge.aws import AWS_BUCKET

def index(request):

    if not request.GET or not request.GET['q'] or len(request.GET['q'])<3:
        return redirect('http://s3.amazonaws.com/%s/oge.html' % AWS_BUCKET)
    
    q = request.GET['q']
    results = Document.objects.filter(text__icontains=q).order_by('-date')
           
    return render_to_response('oge_index.html', {'results': results, 'q': q })



