from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# Session Secret Key
app.secret_key = "tea_house_secret_key"


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
    SELECT teas.tea_name,
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

# Logout
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

#Admin
@app.route('/admin')
def admin():

    if 'email' not in session:
        return redirect('/login')

    if session['email'] != "admin@gmail.com":
        return redirect('/dashboard')

    return render_template('admin.html')

@app.route('/admin-login', methods=['POST'])
def admin_login():

    email = request.form['email']
    password = request.form['password']

    if email == "admin@gmail.com" and password == "admin123":

        session['email'] = email
        session['role'] = "admin"

        return redirect('/admin')

    return "<h1>Invalid Admin Credentials</h1>"

@app.route('/admin')
def admin():

    if 'role' not in session:
        return redirect('/admin-login')

    if session['role'] != "admin":
        return redirect('/')

    return render_template('admin.html')

@app.route('/admin-login')
def admin_login_page():
    return render_template('admin-login.html')