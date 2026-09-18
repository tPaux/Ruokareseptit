import db

def get_recipes():
    sql= """SELECT r.id, r.name, u.username
            FROM recipes r
            LEFT JOIN users u ON r.user_id = u.id
            GROUP BY r.id
            ORDER BY r.id DESC"""
    return db.query(sql)

def get_recipe(recipe_id):
    sql= """SELECT id, name, ingredients, instructions, user_id
            FROM recipes
            WHERE id = ?"""
    result = db.query(sql, [recipe_id])
    if len(result) == 0:
        return None
    return result[0]

def add_recipe(name, ingredients, instructions, user_id):
    sql = "INSERT INTO recipes (name, ingredients, instructions, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [name, ingredients, instructions, user_id])
    recipe_id = db.last_insert_id()
    return recipe_id

def update_recipe(recipe_id, name, ingredients, instructions):
    sql = """
        UPDATE recipes
        SET name = ?, ingredients = ?, instructions = ?
        WHERE id = ?
        """
    db.execute(sql, [name, ingredients, instructions, recipe_id])

def search(query):
    sql = """SELECT r.id,
                    r.name,
                    u.username
             FROM recipes r
              JOIN users u ON r.user_id = u.id
             WHERE (r.ingredients LIKE ?
                OR r.instructions LIKE ?
                OR r.name LIKE ?
                OR u.username LIKE ?)
             ORDER BY r.name DESC"""
    search_term = "%" + query + "%"
    return db.query(sql, [search_term, search_term, search_term, search_term])

def remove_recipe(recipe_id):
    sql = "DELETE FROM  recipes WHERE id = ?"
    db.execute(sql, [recipe_id])
