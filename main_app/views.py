from django.shortcuts import render
from django.http import HttpResponse


class Fish:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.species = breed
        self.description = description
        self.age = age

fish = [
    Fish('Bob', 'Ryukin', 'Very shy', 2),
    Fish('Patrick', 'Comet', 'Kind of fancy', 0),
    Fish('Squidward', 'Ryukin', 'Very fancy', 6)
]


# Create your views here.
def home(request):
    return HttpResponse('Welcome to the Fish Collector')
    
def about(request):
    return render(request, 'about.html')

def fish_index(request):
    return render(request, 'fish/index.html', {'fish': fish})
