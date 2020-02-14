from django.http import HttpResponse
from json import dumps


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return HttpResponse('polls response')
