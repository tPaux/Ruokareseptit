from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import recipes

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    recipe_list = recipes.get_recipes()
    return render_template("index.html", recipes=recipe_list)

@app.route("/login", methods=["POST"])
def login():
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
        return redirect("/")
    else:
        message = "VIRHE: väärä tunnus tai salasana"
        return render_template("index.html", message=message, recipes=recipe_list)

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
    if request.method == "GET":
        return render_template("new_recipe.html")

    name = request.form["name"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    user_id = session["user_id"]

    recipe_id = recipes.add_recipe(name, ingredients, instructions, user_id)
    return redirect("/recipe/" + str(recipe_id))

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
        if "continue" in request.form:
            recipes.remove_recipe(recipe_id)
        return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("query")
    results = recipes.search(query) if query else []
    return render_template("search.html", query=query, results=results)



