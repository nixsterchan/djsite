from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages 
from .forms import NewUserForm

# Create your views here.
# For any actual view, pass 'request' always

# can accept a variable thru the url path
def single_slug(request, single_slug):
  # check if its a cat or tut url
  categories = [c.category_slug for c in TutorialCategory.objects.all()]
  if single_slug in categories:
    matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug) ## double _ before an attribute you want

    # key is obj, value is url
    series_urls = {}

    for m in matching_series.all():
      part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published") # returns all tut objs part of that tut series
      series_urls[m] = part_one.tutorial_slug # tut series obj


    return render(request,
                  "main/category.html",
                  {"part_ones": series_urls})
                  
  tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]

  if single_slug in tutorials:
    this_tutorial = Tutorial.objects.get(tutorial_slug = single_slug)
    
    ## creating sidebar
 
    tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")

    # we want the index of the specific tutorial. reason for that is so we can pop out the one we are currently on
    # as we iterate thru all the tutorials we need to know which one is out, hence the need for their indexes

    this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

    return render(request,
                  "main/tutorial.html",
                  {"tutorial":this_tutorial,
                    "sidebar": tutorials_from_series,
                    "this_tutorial_idx": this_tutorial_idx})

  return HttpResponse(f"{single_slug} does not correspond to anything") 

def homepage(request):
  return render(request=request,
                template_name="main/categories.html",
                context={"categories": TutorialCategory.objects.all})

## need to handle for post request in register funciton
def register(request):
  if request.method == "POST":
    form = NewUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username') ## clean before getting username
      messages.success(request, f"New Account Created: {username} ") ## the messages now exist temporarily
      login(request, user)
      messages.info(request, f"You are now logged on as: {username} ") 
      return redirect("main:homepage")
    else:
      for msg in form.error_messages:
        messages.error(request, f"{msg}: {form.error_messages} ") 
        


  form = NewUserForm
  return render(request,
                "main/register.html",
                context={"form":form})


def logout_request(request):
  logout(request)
  messages.info(request, "Logged out successfully")

  return redirect("main:homepage")

def login_request(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        messages.info(request, f"You are now logged on as: {username} ")
        return redirect("main:homepage")
      else:
        messages.error(request, "Invalid username or password")

    else:
        messages.error(request, "Invalid username or password")
      

  form = AuthenticationForm()
  return render(request,
                "main/login.html",
                {"form": form})
