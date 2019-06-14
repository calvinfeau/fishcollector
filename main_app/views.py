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

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def fish_index(request):
    fish = Fish.objects.filter(user=request.user)
    return render(request, 'fish/index.html', {'fish': fish})

@login_required
def fish_detail(request, fish_id):
  single_fish = Fish.objects.get(id=fish_id)
  decor_single_fish_doesnt_have = Decor.objects.exclude(id__in=single_fish.decors.all().values_list('id'))
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()
  return render(request, 'fish/detail.html', {
    # pass the cat and feeding_form as context
    'single_fish': single_fish, 
    'feeding_form': feeding_form,
    # Add the toys to be displayed
    'decors': decor_single_fish_doesnt_have
  })

@login_required
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

@login_required
def delete_feeding(request, fish_id, feeding_id):
  Feeding.objects.get(pk=feeding_id).delete()
  return redirect ('detail', fish_id=fish_id)

@login_required
def assoc_decor(request, fish_id, decor_id):
  # Note that you can pass a decors id instead of the whole object
  Fish.objects.get(id=fish_id).decors.add(decor_id)
  return redirect('detail', fish_id=fish_id)

@login_required
def remove_decor(request, fish_id, decor_id):
  # Note that you can pass a decors id instead of the whole object
  Fish.objects.get(id=fish_id).decors.remove(decor_id)
  return redirect('detail', fish_id=fish_id)

@login_required
def delete_photo(request, fish_id, photo_id):
  Photo.objects.get(pk=photo_id).delete()
  return redirect('detail', fish_id=fish_id)

@login_required
def add_photo(request, fish_id):
    # photo-file was the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object
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
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credentials - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



class FishCreate(CreateView):
  model = Fish
  fields = ['name', 'species', 'description', 'age']
  success_url = '/fish/'
  # This method is called when a valid
  # cat form has being submitted
  def form_valid(self, form):
    # Assign the logged in user
    form.instance.user = self.request.user
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class FishUpdate( UpdateView):
  model = Fish
  # Let's make it impossible to rename a cat :)
  fields = ['species', 'description', 'age']

class FishDelete(DeleteView):
  model = Fish
  success_url = '/fish/'

class DecorList(ListView):
  model = Decor

class DecorDetail(DetailView):
  model = Decor

class DecorCreate(CreateView):
  model = Decor
  fields = '__all__'
  success_url = '/decors/'

class DecorUpdate(UpdateView):
  model = Decor
  fields = ['name', 'color']

class DecorDelete(DeleteView):
  model = Decor
  success_url = '/decors/'