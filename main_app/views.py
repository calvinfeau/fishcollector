from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Fish
from .forms import FeedingForm

class FishCreate(CreateView):
  model = Fish
  fields = '__all__'

class FishUpdate(UpdateView):
  model = Fish
  # Let's make it impossible to rename a cat :)
  fields = ['species', 'description', 'age']

class FishDelete(DeleteView):
  model = Fish
  success_url = '/fish/'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def fish_index(request):
    fish = Fish.objects.all()
    return render(request, 'fish/index.html', {'fish': fish})

def fish_detail(request, fish_id):
  single_fish = Fish.objects.get(id=fish_id)
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()
  return render(request, 'fish/detail.html', {
    # pass the cat and feeding_form as context
    'single_fish': single_fish, 
    'feeding_form': feeding_form
  })

def add_feeding(request, fish_id):
  # create the ModelForm using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.fish_id = fish_id
    new_feeding.save()
  return redirect('detail', fish_id=fish_id)