import db

def get_user(user_id):
    sql = "SELECT id, username, image IS NOT NULL has_image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_recipes(user_id):
    sql = """SELECT r.id,
                    r.name
             FROM recipes r
             WHERE r.user_id = ?
             ORDER BY r.sent_at DESC"""
    return db.query(sql, [user_id])

def get_messages(user_id):
    sql = """SELECT m.id,
                    r.name,
                    m.sent_at
             FROM recipes r, messages m
             WHERE r.id = m.recipe_id AND
                   m.user_id = ?
             ORDER BY m.sent_at DESC"""
    return db.query(sql, [user_id])

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id ])

def get_image(user_id):
    pass #TODO

