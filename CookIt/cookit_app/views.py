from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from . import models
from .models import User, Category, Instruction, Ingredient, Recipe, Review

# This function to display the main page of the website
def index(request):

    context = {
        "categories" : Category.objects.all()
    }
    
    return render(request, 'index.html', context)

# This function check if any user logged in 
def check_user_logged_in(request):
    if not request.session.get('id'):
        return redirect('/')
    try:
        user = User.objects.get(id=request.session['id'])
    except (User.DoesNotExist, KeyError) :
        return redirect('/')

# This function to display the home page of the website after the user has logged in
def home(request): 
    check_user_logged_in(request)
    user_id = request.session.get('id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('/')

    context = {
        
        'user': user,
        "categories" : Category.objects.all()

    }
    return render(request, 'home.html', context)

# This function renders the register page
def register_page(request):
        return render(request, 'register.html')

# This function renders the login page
def login_page(request): 
    return render(request, 'login.html')


# This function validates the login and logs the user in
def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_page')
    else:
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/home')

# This function validates the registration information and creates a new user
def register(request):
    errors = User.objects.validate_register(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register_page')
    else:
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/home')

# This function clears the session data and redirects the user to the main page
def logout(request):
    request.session.clear()
    return redirect('/')

def my_reciepes(request):
    if 'id' in request.session:
        context = {
        "recipes" :Recipe.objects.filter(user=User.objects.get(id=request.session['id'])),
        }
        return render(request, "my_reciepes.html", context)
    return redirect("/")
    

def all_reciepes(request):
    return render(request, "all_reciepes.html")

def category_reciepes(request): 
    return render(request, "category_reciepes.html")

def add_reciepe_page(request):
    if 'id' in request.session:
        context = {
        "categories" :['Breakfast','Lunch','Dinner','Juice','Salad'],
        }
        return render(request, "add_reciepe.html", context)
    return redirect("/")

def reciepe_details(request):
    return render(request, "reciepe_details.html")

def categories(request):
    context = {
        "categories" : Category.objects.all()
    }
    return render(request, "category_reciepes.html", context)



def add_recipe(request):
    recipe_creator=User.objects.get(id=request.session['id'])
    information=[request.POST['name'],request.POST['category'],request.POST['description'], request.FILES['image'], request.POST['preparation_time'], request.POST['cooking_time'], request.POST['serving_people']]
    recipe = Recipe.objects.create(name=information[0],category=information[1],description=information[2],recipe_img=information[3], preparation_time=information[4], cooking_time=information[5], serving_people=information[6], user = recipe_creator )
    

    for i in range(int(request.POST['number_of_ingredients'])):
        ingredient_name='ingredient_name_'+ str(i)
        ingredient_quantity='ingredient_quantity_'+ str(i)
        ingredient=Ingredient.objects.create(name=request.POST[ingredient_name], quantity=request.POST[ingredient_quantity])
        recipe.ingredients.add(ingredient)

    for i in range(int(request.POST['number_of_instructions'])):
        instruction_specification='instruction_specification_'+ str(i)
        Instruction.objects.create(specification=request.POST[instruction_specification], recipe=recipe)
        

    return redirect('/my_reciepes')