from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from datetime import datetime
def home(request):
    return render(request,'home.html',{'search_enabled': False})
def login(request):
  
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        
        print(f"Username from POST: {username}, Password from POST: {password}")

        try:
            user = User.objects.get(username=username)
            print(f"User exists: {user}")
        except User.DoesNotExist:
            messages.error(request, "Invalid username")
            return redirect('/login/')

        # Debugging: Check if user is active
        print(f"User is active: {user.is_active}")

        if not user.is_active:
            messages.error(request, "Inactive user")
            return redirect('/login/')

        # Authenticate user
        authenticated_user = authenticate(request, username=username, password=password)

        
        if authenticated_user is None:
            print(f"Authenticated user is None: {authenticated_user}")
            messages.error(request, "Invalid password")
            return redirect('/login/')
        else:
            print(f"Authenticated user: {authenticated_user}")
            auth_login(request, authenticated_user)
            messages.success(request, "Login successful")
            return redirect('/recipes')
            
    return render(request, 'login.html')
    
    
def validate_password(password):
    has_special_character=any(char in "!@#$%^&*()-_=+[{]};:'\",<.>/?`" for char in password)
    has_capital_alphabet=any(char.isupper() for char in password)
    has_digit=any(char.isdigit() for char in password)

    if not (has_special_character and has_capital_alphabet and has_digit):
       return False

    return True

def register(request):
     if request.method == 'POST':
        data=request.POST
        username=data.get('username')
        email=data.get('email')
        password=data.get('password')
        confirm_password=data.get('confirm_password')
        user=User.objects.filter(username=username)
        if user.exists():
            messages.error(request,"username already exists")  
            return redirect('/register')
        if not username or not email or not password  or not confirm_password: 
            messages.error(request,"pleare fill all the fields")  
            return redirect('/register')
        if len(password)<8:
            messages.error(request,"password should be minimum 8 characters")  
            return redirect('/register')
        if not validate_password(password):
            messages.error(request,"password should have alphanumeric characters")
            return redirect('/register')
        
        if password!=confirm_password:
            messages.error(request,"password should be match the password")  
            return redirect('/register')
        user=User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        
       
        messages.success(request,"Account Created Successfully ") 
        return redirect('/login')    
     return render(request,'register.html')

@login_required(login_url="/login")
def logout(request):
    auth_logout(request)
    messages.error(request, "Logout successful")
    return redirect('/login')

@login_required(login_url="/login")
def recipes(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        current_date = datetime.now().date()

        Recipe.objects.create(
            user=request.user,
            title=title,
            description=description,
            image=image,
            date=current_date
        )
        messages.success(request,"Successfully Recipe Added")
        return redirect('/recipes')

    context = {
        'current_date': datetime.now().date()
    }
   

    return render(request,"recipes.html",context)


@login_required(login_url="/login")
def recipe_view(request):
    view=Recipe.objects.filter(user=request.user)
    if request.method=="GET":

     select=request.GET.get("search")
    if select:
       view = Recipe.objects.filter(title__icontains=select)

    return render(request,"recipe_view.html",{'view':view,'search': True})


def all_recipe_view(request):
    if request.user.is_authenticated:
     view=Recipe.objects.exclude(user=request.user).order_by('-view')
     
    
  
    
    else:
        view=Recipe.objects.all().order_by('-view')

        
    if request.method=="GET":

     select=request.GET.get("search")
     if select:
       view = Recipe.objects.filter(title__icontains=select)
    return render(request,"all_recipe_view.html",{'view':view,'search': True})


@login_required(login_url="/login")
def get_recipe(request,pk):
    recipe=get_object_or_404(Recipe,pk=pk)
    recipe.view=recipe.view+1
    recipe.save()
    existing_feedback=Feedback.objects.filter(user=request.user,recipe=recipe).exists()
    if request.method=="POST" and not existing_feedback:
        data=request.POST
        feedback=data.get('feedback')
        Feedback.objects.create(user=request.user, recipe=recipe, feedback=feedback)
        Notification.objects.create(user=recipe.user,message=f"{request.user.username} has left feedback on your recipe {recipe.title}.",recipe=recipe)
        existing_feedback=True
        return redirect("get_recipe",pk=pk)



         
        
    return render(request,"get_recipe.html",{'recipe':recipe, 'existing_feedback':existing_feedback})


@login_required(login_url="/login")
def get_recipe2(request,pk):
    recipe=get_object_or_404(Recipe,pk=pk)
    feedback=Feedback.objects.filter(recipe=recipe)
    return render(request,"get_recipe2.html",{'recipe':recipe ,'feedback':feedback})



@login_required(login_url="/login")
def like_recipe(request,pk):
    recipe=get_object_or_404(Recipe,pk=pk)
    if request.user not in recipe.likes.all():
        recipe.likes.add(request.user)
        Notification.objects.create(user=recipe.user,message=f"{request.user.username} has left like on your recipe {recipe.title}.",recipe=recipe )
        recipe.save()
    else:
        recipe.likes.remove(request.user)
        recipe.save()

    return redirect('get_recipe',pk=pk)



@login_required(login_url="/login")
def notification(request):
    notification = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request,"notification.html",{'notification':notification})



