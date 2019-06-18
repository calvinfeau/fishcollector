from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FeedingForm
import uuid
import boto3
from .models import Fish, Decor, Photo, Feeding

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'calvinstorage'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def fish_index(request):
    fish = Fish.objects.filter(user=request.user)
    return render(request, 'home.html', {'fish': fish})

@login_required
def fish_detail(request, fish_id):
  single_fish = Fish.objects.get(id=fish_id)
  decor_single_fish_doesnt_have = Decor.objects.exclude(id__in=single_fish.decors.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'fish/detail.html', {
    'single_fish': single_fish, 
    'feeding_form': feeding_form,
    'decors': decor_single_fish_doesnt_have
  })

@login_required
def add_feeding(request, fish_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.fish_id = fish_id
    new_feeding.save()
  return redirect('detail', fish_id=fish_id)

@login_required
def delete_feeding(request, fish_id, feeding_id):
  Feeding.objects.get(pk=feeding_id).delete()
  return redirect ('detail', fish_id=fish_id)

@login_required
def assoc_decor(request, fish_id, decor_id):
  Fish.objects.get(id=fish_id).decors.add(decor_id)
  return redirect('detail', fish_id=fish_id)

@login_required
def remove_decor(request, fish_id, decor_id):
  Fish.objects.get(id=fish_id).decors.remove(decor_id)
  return redirect('detail', fish_id=fish_id)

@login_required
def delete_photo(request, fish_id, photo_id):
  Photo.objects.get(pk=photo_id).delete()
  return redirect('detail', fish_id=fish_id)

@login_required
def add_photo(request, fish_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, single_fish_id=fish_id)
            print("it's working")
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', fish_id=fish_id)

@login_required
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credentials - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



class FishCreate(LoginRequiredMixin, CreateView):
  model = Fish
  fields = ['name', 'species', 'description', 'age']
  success_url = '/fish/'
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class FishUpdate(LoginRequiredMixin, UpdateView):
  model = Fish
  fields = ['name', 'species', 'description', 'age']

class FishDelete(LoginRequiredMixin, DeleteView):
  model = Fish
  success_url = '/fish/'


class DecorCreate(LoginRequiredMixin, CreateView):
  model = Decor
  fields = '__all__'
  success_url = '/decors/'
  
class DecorList(LoginRequiredMixin, ListView):
  model = Decor

class DecorDetail(LoginRequiredMixin, DetailView):
  model = Decor

class DecorUpdate(LoginRequiredMixin, UpdateView):
  model = Decor
  fields = ['name', 'color']

class DecorDelete(LoginRequiredMixin, DeleteView):
  model = Decor
  success_url = '/decors/'