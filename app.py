from flask import Flask, render_template, request, redirect, session, g, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import recipes
import users
import sqlite3
import time
import secrets
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br>")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    recipe_list = recipes.get_recipes()
    return render_template("index.html", recipes=recipe_list)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])
        if len(result) == 0:
            message = "VIRHE: väärä tunnus tai salasana"
            return render_template("index.html", message=message)
        user = result[0]
        user_id = user["id"]
        password_hash = user["password_hash"]

        recipe_list = recipes.get_recipes()

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            message = "VIRHE: väärä tunnus tai salasana"
            return render_template("index.html", message=message, recipes=recipe_list)

def check_csrf():
    if request.form.get("csrf_token") != session.get("csrf_token"):
        abort(403)

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/logout")
def logout():
    session.clear()
    recipe_list = recipes.get_recipes()
    message = "Olet nyt kirjautunut ulos"
    return render_template("index.html", message=message, recipes=recipe_list)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        message = "VIRHE: salasanat eivät ole samat"
        return render_template("register.html", message=message)
    password_hash = generate_password_hash(password1)
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        message = "VIRHE: tunnus on jo varattu"
        return render_template("register.html", message=message)
    message = "Tunnus luotu"
    recipe_list = recipes.get_recipes()
    return render_template("index.html", message=message, recipes=recipe_list)

@app.route("/new_recipe", methods=["GET", "POST"])
def new_recipe():
    if request.method == "POST":
        check_csrf()
        name = request.form["name"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        user_id = session["user_id"]

        recipe_id = recipes.add_recipe(name, ingredients, instructions, user_id)
        return redirect("/recipe/" + str(recipe_id))

    if request.method == "GET":
        return render_template("new_recipe.html")

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    print(dict(recipe))
    return render_template("recipe.html", recipe=recipe)

@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    if request.method == "GET":
        return render_template("edit.html", recipe=recipe)
    if request.method == "POST":
        check_csrf()
        name = request.form["name"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        recipes.update_recipe(recipe_id, name, ingredients, instructions)
        return redirect(f"/recipe/{recipe_id}")

@app.route("/remove/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)

    if request.method == "GET":
        return render_template("remove.html", recipe=recipe)
    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            recipes.remove_recipe(recipe_id)
        return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("query")
    results = recipes.search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/user/<int:user_id>", strict_slashes=False)
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    recipes = users.get_recipes(user_id)
    messages = users.get_messages(user_id)
    return render_template("user.html", user=user, recipes=recipes, messages=messages)

@app.route("/add_profile_image", methods=["GET", "POST"])
def add_profile_image():
    require_login()
    if request.method == "GET":
        return render_template("add_profile_image.html")
    if request.method == "POST":
        check_csrf()
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            message = "VIRHE: väärä tiedostomuoto"
            return render_template("add_profile_image.html", message=message)
        image = file.read()
        if len(image) > 100 * 1024:
            message = "VIRHE: liian suuri kuva"
            return render_template("add_profile_image.html", message=message)
        user_id = session["user_id"]
        users.update_image(user_id, image)
        print("image uploaded")
        return redirect("/user/" + str(user_id))

@app.route("/profile_image/<int:user_id>", strict_slashes=False)
def show_profile_image(user_id):
    image = users.get_image(user_id)
    if not image:
        print("no image")
        abort(404)
    print("image exists")
    response = make_response(image)
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response




