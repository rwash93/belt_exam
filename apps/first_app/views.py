from django.shortcuts import render,redirect
from apps.first_app.models import*
import bcrypt
from django.contrib import messages





def index(request):
    return render(request,"first_app/index.html")

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(),
        bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], 
        last_name= request.POST['last_name'], 
        email = request.POST["email"],
        confirm_password=hash1,
        password = hash1)
        request.session['loggedin'] =user.id
        return redirect('/')

def login (request):
    email = request.POST['email']
    errors=User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['loggedin'] = user.id
        return redirect('/dashboard')

def dashboard (request):
    if 'loggedin' not in request.session:
        return redirect('/')
    context={
        "key": Wish.objects.all(),
        'user': User.objects.get(id=request.session['loggedin'])
    }
    return render(request,"first_app/dashboard.html",context)

def addpage(request):
    return render(request,'first_app/add.html')

def add(request):

    if 'loggedin' not in request.session:
        return redirect('/')
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0: 
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/addpage')
    else:
    # valid user
        if 'loggedin' not in request.session:
            return redirect('/')
    # variables
    curr_user=User.objects.get (id = request.session['loggedin'])

    wish = Wish.objects.create(
        title = request.POST["wish_title"], 
        description= request.POST["wish_description"],
        user= curr_user
    )
    return redirect('/dashboard')

def edit (request, number):
    if 'loggedin' not in request.session:
        return redirect('/')
    context={
        "key":Wish.objects.get(id=number)
    }
    return render (request, 'first_app/edit.html',context)

def edit_page(request, id):
    
    if 'loggedin' not in request.session:
        return redirect('/')
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/edit/{}'.format(id))
    else:
        s= Wish.objects.get(id=id)
        s.title = request.POST["wish_title"]
        s.description = request.POST["wish_description"]
        s.save()
    return redirect ('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def go_back(request):
    return render(request,'first_app/dashboard.html')

def destroy(request,number):
    context ={
        'wish':Wish.objects.get(id=number).delete()
    }
    return redirect('/dashboard',context)


# Create your views here.
