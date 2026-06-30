from flask import Flask, render_template, request, redirect, session
import sqlite3

from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Session Secret Key
app.secret_key = "tea_house_secret_key"

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Register Page
@app.route('/register')
def register_page():
    return render_template('register.html')


# Register User
@app.route('/register', methods=['POST'])
def register():

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()

    except:
        return "<h1>Email Already Exists</h1>"

    finally:
        conn.close()

    return redirect('/login')


# Login Page
@app.route('/login')
def login_page():
    return render_template('login.html')


# Login User
@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        session['user'] = user[1]   # name
        session['email'] = user[2]  # email

        if user[2] == "admin@gmail.com":
            return redirect('/admin')

        return redirect('/dashboard')

    return "<h1>Invalid Email or Password</h1>"



# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        username=session['user']
    )

@app.route('/menu')
def menu():

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teas")

    teas = cursor.fetchall()

    conn.close()

    return render_template(
        'menu.html',
        teas=teas
    )

@app.route('/add_cart/<int:tea_id>')
def add_cart(tea_id):

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE name=?",
        (session['user'],)
    )

    user = cursor.fetchone()

    cursor.execute(
        "INSERT INTO cart(user_id, tea_id) VALUES(?,?)",
        (user[0], tea_id)
    )

    conn.commit()
    conn.close()

    return redirect('/cart')

@app.route('/cart')
def cart():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE name=?",
        (session['user'],)
    )

    user = cursor.fetchone()

    cursor.execute("""
   SELECT cart.id,
       teas.tea_name,
       teas.price,
       cart.quantity
    FROM cart
    JOIN teas
    ON cart.tea_id = teas.id
    WHERE cart.user_id = ?
    """, (user[0],))

    cart_items = cursor.fetchall()

    conn.close()

    return render_template(
        'cart.html',
        cart_items=cart_items
    )

# Delete Cart Item
@app.route('/delete_cart/<int:cart_id>')
def delete_cart(cart_id):

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM cart WHERE id=?",
        (cart_id,)
    )

    conn.commit()
    conn.close()

    return redirect('/cart')

#User profile

@app.route('/profile')
def profile():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (session['email'],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
        'profile.html',
        user=user
    )

#Edit profile route

@app.route('/edit-profile')
def edit_profile():

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (session['email'],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_profile.html',
        user=user
    )

@app.route('/edit-profile', methods=['POST'])
def update_profile():

    name = request.form['name']

    image = request.files['image']

    filename = ""

    if image:

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET name=?, image=?
        WHERE email=?
        """,
        (
            name,
            filename,
            session['email']
        )
    )

    conn.commit()
    conn.close()

    session['user'] = name

    return redirect('/profile')

#Admin
@app.route('/admin')
def admin():

    if 'role' not in session:
        return redirect('/admin-login')

    return render_template('admin.html')

@app.route('/admin-login', methods=['POST'])
def admin_login():

    email = request.form['email']
    password = request.form['password']

    if email == "admin@gmail.com" and password == "admin123":

        session['role'] = "admin"

        return redirect('/admin')

    return "<h1>Invalid Admin Credentials</h1>"

@app.route('/admin-login')
def admin_login_page():
    return render_template('admin-login.html')

#Admin manage product like add delete
@app.route('/manage-products')
def manage_products():

    if 'role' not in session:
        return redirect('/admin-login')

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teas")

    products = cursor.fetchall()

    conn.close()

    return render_template(
        'manage_products.html',
        products=products
    )

#admin can add product
@app.route('/add-product')
def add_product_page():
    return render_template('add_product.html')

@app.route('/add-product', methods=['POST'])
def add_product():

    tea_name = request.form['tea_name']
    price = request.form['price']
    description = request.form['description']

    image = request.files['image']

    filename = ""

    if image:

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO teas
        (tea_name, price, description, image)
        VALUES (?, ?, ?, ?)
        """,
        (
            tea_name,
            price,
            description,
            filename
        )
    )

    conn.commit()
    conn.close()

    return redirect('/manage-products')

#for deleting product
@app.route('/delete-product/<int:id>')
def delete_product(id):

    conn = sqlite3.connect('tea_house.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM teas WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/manage-products')

#for image add to my product 
#admin checks orders
@app.route('/orders')
def orders():

    if 'role' not in session:
        return redirect('/admin-login')

    return render_template('orders.html')

#user html file route
@app.route('/users')
def users():
    return render_template('users.html')

#analytics and the setting part
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

# Logout
@app.route('/logout')
def logout():

    session.pop('user', None)
    session.pop('email', None)
    session.pop('role', None)

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
