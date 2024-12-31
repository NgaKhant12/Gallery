from django.shortcuts import render,redirect
from .models import Category,Photo

from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterFormm

import pymongo

from GalleryProject import settings
from django.core.mail import send_mail

# Create your views here.

@login_required
def Gallery(request):
    category = request.GET.get('category')
    submit = request.POST.get('submit')
    photosss = Photo.objects.all()
    count = photosss.count()
    search_val = request.GET.get("search_name") or ''

    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name__contains = category)
       
    if search_val:
        photos = Photo.objects.filter(category__name__icontains = search_val)

    categories = Category.objects.all()
    context = {'categories':categories,'photos':photos,"count":count}

    renderobj = render(request,"GalleryApp/gallery.html",context)
    return renderobj

@login_required
def View(request,pk):
    photo = Photo.objects.get(id=pk)
    views_input = request.GET.get('views')
    return render(request,"GalleryApp/viewphoto.html",{'photo':photo,"views":views_input})


@login_required
def Add(request):
    categories = Category.objects.all()
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get('image')
        
        if data['category'] != "none":
            category = Category.objects.get(id=data['category'])
        elif data['new_category'] != '':
            category , created = Category.objects.get_or_create(name=data['new_category'])
        else:
            category = None
        
        photo = Photo.objects.create(
            category = category,
            description = data['description'],
            image = image,
        )
    
        tit = category.name
        des = data["description"]

        client = pymongo.MongoClient("localhost",27017)

        db = client['MyfirstDB']

        collect= db['MyfirstCollection']

        
        return redirect("gallery")
  
    context = {'categories':categories}
    return render(request,"GalleryApp/addphoto.html",context)


class Update(LoginRequiredMixin,UpdateView):
    model = Photo
    fields = "__all__"
    template_name = 'GalleryApp/update.html'
    success_url = reverse_lazy('gallery')


class Delete (LoginRequiredMixin,DeleteView):
    model = Photo
    fields = "__all__"
    template_name = "GalleryApp/delete.html"
    success_url = reverse_lazy('gallery')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("uname")
        upassword = request.POST.get("upassword")

        user = authenticate(request,username=username,password=upassword)

        if user is not None:
            login (request,user)
            return redirect("gallery")
        else:
            messages.error(request,"Invalid Username Or Password")

    return render(request,"GalleryApp/login.html")
        

# class Signin(LoginView):
#     template_name = "GalleryApp/login&signup.html"
#     fields = "__all__"
#     redirect_authenticated_user = True
    
#     def get_success_url(self):
#         return reverse_lazy("gallery")
    
@login_required
def Contact(request):
    if request.method == "POST":
        c_name = request.POST.get("contact_name")
        c_email = request.POST.get("contact_email")
        c_message = request.POST.get("contact_message")
        return redirect("gallery")

    return render(request, "GalleryApp/contact.html")

@login_required
def views(request):
    photos = Photo.objects.all()
    return render (request,"GalleryApp/view.html",{"photos":photos})

def send_welcome_email(uname,recevier_email):
    subject = "Welcome to Our Service"
    message = "Hello {%s}, /n Thank you for sending me an email. I'm so glad to have you! Since you recognize My Portfolio ",uname
    recipient_list = [recevier_email]  # လက်ခံမယ့် email ၊ list နဲ့ မဖြစ်မနေထားရမယ်။
    from_email = settings.EMAIL_HOST_USER
    
    send_mail(subject, message, from_email, recipient_list)

def register(request):
    form = RegisterFormm()
    if request.method == "POST":
        form = RegisterFormm(request.POST)
        name = form['username'].value()
        email = form['email'].value()
        send_welcome_email(name,email)
        
        if form.is_valid():
            form.save()
            return redirect("gallery")
        else:
            messages.error(request,str(form.errors))
    context = {"form":form}
    return render(request,"GalleryApp/register.html",context)