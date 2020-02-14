from django.shortcuts import render
from django.http import HttpResponse
from json import dumps

from .models import Greeting

class Person:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def to_json(self):
        return dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def users(request):
    alvin = Person('Alvin Nguyen', 'Data Scientist')
    print(alvin.to_json())
    # todo: Fire off the ml model work here ...
    # read input file
    # call the function with the input
    # const ret = ml_job(inp);
    # ret -> Ret(start_ts, end_ts, op_file, status)
    # response = HttpResponse(ret.toJSON())
    response = HttpResponse(alvin.to_json())
    response['Content-Type' ] = 'application/json'
    return response


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})
