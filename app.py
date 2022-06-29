import random
from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests
import os

from forms import LoginForm, UserAddForm, UserEditForm
from models import db, connect_db, User, Recipe

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///cooky_cap')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.drop_all()
db.create_all()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "HelloSecret1")

# API_KEY = "19269c3c0c1e463da6cd2157f3303d8b"
API_KEY = "1e856b6073e54d8a8c0c7234a720cd5a"

############################# User signup/login/logout ######################################################
@app.before_request
def add_user_to_g():
    """If we're logged in, add current user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create a new user and redirect to the homepage
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                profile_pic=form.profile_pic.data or User.profile_pic.default.arg,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken. Try a different one.", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Log the user out"""
    do_logout()
    flash("You have logged out successfully", 'success')
    return redirect('/login')

####################### General Routes and HomePage for the USER #######################


@app.route('/', methods=['GET', 'POST'])
def homepage():
    """Show the homepage for each user"""

    populars = requests.get(f"https://api.spoonacular.com/recipes/random?number=6&apiKey={API_KEY}")

    favorites = (Recipe.query.limit(100).all())
    intolerances = ["Dairy","Egg","Gluten","Grain","Peanut","Seafood","Sesame","Shellfish","Soy","Sulfite","Tree Nut","Wheat"]
    cuisines = ["African",
                "American",
                "British",
                "Cajun",
                "Caribbean",
                "Chinese",
                "Eastern European",
                "European",
                "French",
                "German",
                "Greek",
                "Indian",
                "Irish",
                "Italian",
                "Japanese",
                "Jewish",
                "Latin American",
                "Mediterranean",
                "Mexican",
                "Middle Eastern",
                "Nordic",
                "Southern",
                "Spanish",
                "Thai",
                "Vietnamese"]
    diets = ["Ketogenic", "Vegetarian", "Lacto-Vegetarian","Ovo-Vegetarian","Vegan","Pescatarian","Paleo","Primal","Low FODMAP", "Whole30"]
    
    
    resp = []
    
    if request.method == 'POST':
        cuisine = request.form.get('home-cuisine')
        query = request.form.get('home-search')
        

        recipe_results = requests.get(f'https://api.spoonacular.com/recipes/complexSearch?query={query}&cuisine={cuisine}&number=28&apiKey={API_KEY}')
        resp=recipe_results.json()
        # return render_template('users/find_recipe.html', intolerances=intolerances, cuisines=cuisines, diets=diets, resp=recipe_results.json())
    
        return render_template('users/find_recipe.html', intolerances=intolerances, cuisines=cuisines, diets=diets, resp=resp)

    return render_template('home.html', populars=populars.json(), cuisines=cuisines)

@app.route('/search', methods=['GET', 'POST'])
def search_recipes():
    """Users and non-users can search the site for recipes using the info gathered from the API."""
    intolerances = ["Gluten Free","Dairy","Egg","Gluten","Grain","Peanut","Seafood","Sesame","Shellfish","Soy","Sulfite","Tree Nut","Wheat"]
    cuisines = ["African",
                "American",
                "British",
                "Cajun",
                "Caribbean",
                "Chinese",
                "Eastern European",
                "European",
                "French",
                "German",
                "Greek",
                "Indian",
                "Irish",
                "Italian",
                "Japanese",
                "Jewish",
                "Latin American",
                "Mediterranean",
                "Mexican",
                "Middle Eastern",
                "Nordic",
                "Southern",
                "Spanish",
                "Thai",
                "Vietnamese"]
    diets = ["Ketogenic", "Vegetarian", "Lacto-Vegetarian","Ovo-Vegetarian","Vegan","Pescatarian","Paleo","Primal","Low FODMAP", "Whole30"]
    resp = []
    # favorites = (Recipe.query.limit(100).all())

    if request.method == 'POST':
        cuisine = request.form.get('cuisine', '""') 
        max_protein = request.form.get('max-protein', 1000) or 1000
        max_carbs = request.form.get('max-carbs', 1000) or 1000
        max_fat = request.form.get('max-fat', 1000) or 1000
        diet = request.form.get('diet', '""')
        intolerance = request.form.get('intolerance', '""')
        query = request.form.get('search', '""')
        
        
        print(f'https://api.spoonacular.com/recipes/complexSearch?query={query}&maxProtein={max_protein}&maxCarbs={max_carbs}&maxFat={max_fat}&cuisine={cuisine}&diet={diet}&intolerance={intolerance}&number=28&apiKey={API_KEY}')
        recipe_results = requests.get(f'https://api.spoonacular.com/recipes/complexSearch?query={query}&maxProtein={max_protein}&maxCarbs={max_carbs}&maxFat={max_fat}&cuisine={cuisine}&diet={diet}&intolerance={intolerance}&number=28&apiKey={API_KEY}')
        print(recipe_results)
        resp=recipe_results.json()
        # return render_template('users/find_recipe.html', intolerances=intolerances, cuisines=cuisines, diets=diets, resp=recipe_results.json())
    
    return render_template('users/find_recipe.html', intolerances=intolerances, cuisines=cuisines, diets=diets, resp=resp)

@app.route('/contact')
def contact_info():
    """Renders form for user to send feedback or get help from us."""
    return render_template('contact.html')

@app.route('/recipes')
def random_recipes():
    """Renders page with random recipes for user to look through"""
    randoms = requests.get(f"https://api.spoonacular.com/recipes/random?number=25&apiKey={API_KEY}")
    return render_template('users/recipes.html', randoms=randoms.json())

@app.route('/recipe/<int:id>')
def show_recipe(id):
    """Shows details of chosen recipe"""
    recipe = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?includeNutrition=true&apiKey={API_KEY}")
    return render_template('users/recipe.html', recipe=recipe.json())

@app.route('/my_profile/<int:user_id>')
def user_show(user_id):
    """Show the user's profile"""

    if CURR_USER_KEY in session:
        user = User.query.get_or_404(user_id)
        favorites = (Recipe.query.limit(100).all())
        return render_template('users/my_profile.html', user=user, favorites=favorites)
    
    return render_template('error404.html')

@app.route('/my_profile/')
def user_404_show():
    """when user is not logged in and clicks 'my account' it should bring to 404 page."""
    return render_template('error404.html')
    
    
    

@app.route('/user/edit', methods=["GET", "POST"])
def edit_profile():
    """Edit profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.name = form.name.data
            user.email = form.email.data
            user.profile_pic = form.profile_pic.data or "/static/images/default-pic.png"
            user.bio = form.bio.data
            user.fav_cuisine = form.fav_cuisine.data
            user.fav_spices = form.fav_spices.data
            user.fav_appliances = form.fav_appliances.data

            db.session.commit()
            return redirect(f"/my_profile/{user.id}")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit1.html', form=form, user_id=user.id)

################################################### API ROUTES ###########################################################

@app.route('/api/get-recipe-results', methods=["POST"])
def get_results():
    """gets results from api using advanced search values"""
    max_protein = request.json['max_protein']
    max_carbs = request.json['max_carbs']
    max_fat = request.json['max_fat']
    cuisine = request.json['cuisine']
    diet = request.json['diet']
    intolerance = request.json['intolerance']
    query = request.json['query']

    recipe_response = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?query={query}&maxProtein={max_protein}&maxCarbs={max_carbs}&maxFat={max_fat}&cuisine={cuisine}&diet={diet}&intolerance={intolerance}&apiKey={API_KEY}")
    print(recipe_response.json())
    return recipe_response.json()

@app.route('/api/recipe/<int:id>')
def getRecipe(id):
    # if not g.user:
    #     flash("Access unauthorized.", "danger")
    #     return redirect("/login")

    recipe = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?includeNutrition=true&apiKey={API_KEY}")
    print(recipe.json())

    return render_template('api/recipe.html', recipe=recipe.json())

    ############################################### Recipe Database Routes #########################################################

@app.route('/api/recipe/favs', methods=["POST"])
def favs_add():
    """Add a recipe to favorited recipes for user"""
    id = request.json['id']
    title_text = request.json['title']
    img_url = request.json['img_url']
    print(id, title_text, img_url)

    fav_recipe = Recipe(
        id = id,
        user_id = g.user.id,
        title = title_text,
        recipe_img = img_url
    )
    db.session.add(fav_recipe)
    db.session.commit()

    recipe_response = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?includeNutrition=true&apiKey={API_KEY}")
    return recipe_response.json()

@app.route('/api/recipe/remove_favs', methods=["POST"])
def favs_delete():
    """Remove favorite from the recipes table"""
    id = request.json['id']
    print(id)
    deleted_favorite = Recipe.query.get_or_404(id)

    try:
        db.session.delete(deleted_favorite)
        db.session.commit()
        """Might return to a certain url when you are refreshing in favorites page."""
    except: 
        flash("Whoops, there was an issue with removing favorite.")

    

    recipe_response = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?includeNutrition=true&apiKey={API_KEY}")
    return recipe_response.json()
    
@app.route('/api/recipe/remove', methods=["POST"])
def delete():
    """Remove favorite from the recipes table and returns to profile. """
    id = request.json['id']
    print(id)
    deleted_favorite = Recipe.query.get_or_404(id)

    try:
        db.session.delete(deleted_favorite)
        db.session.commit()
        """Might return to a certain url when you are refreshing in favorites page."""
    except: 
        flash("Whoops, there was an issue with removing favorite.")

    

   
    return 'success'
    





