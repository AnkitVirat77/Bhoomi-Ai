from flask import Flask , render_template , redirect , url_for , request, session,flash
import bcrypt
import re
import pyodbc
# from flask import Flask , render_template , redirect , url_for , request
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

app.secret_key = "baa64ccd1d64a499e0e0480a409905754637cc1ed5132430f4fd15bcea84dd86"

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='Your_secret_id',
    client_secret='your_secret_key',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=localhost\SQLEXPRESS;"
    "DATABASE=flaskdb;"
    "Trusted_Connection=yes;"
)


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup():
    email_error = session.pop('email_error', False)
    print("SESSION READ:", email_error)
    password_error = session.pop('password_error', False)

    return render_template(
        'sign_up.html',
        email_error=email_error,
        password_error=password_error
    )

@app.route('/login' , methods = ['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user:
        stored_password = user[4]

    if stored_password is None:
        return "Password missing"
    
    if stored_password is None:
        return "Please login using Google"

    

    # 🔥 FIX HERE
    stored_password = stored_password.encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        session['user'] = email
        return render_template('Dashboard.html', name=user[1] , email = user[2] , mobile = user[3])
    else:
        return "Invalid password"
   

    session['user'] = email

@app.route('/login/google')
def login_google():
    return google.authorize_redirect(url_for('google_callback', _external=True))


@app.route('/auth/google/callback')
def google_callback():
    token = google.authorize_access_token()
    user_info = google.get('https://openidconnect.googleapis.com/v1/userinfo').json()

    email = user_info['email']
    name = user_info['name']

    cursor = conn.cursor()

    # Check user
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    # If new user → insert
    if not user:
        cursor.execute(
            "INSERT INTO users (name, email, mobile, password) VALUES (?, ?, ?, ?)",
            (name, email, None, None)
        )
        conn.commit()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

    session['user'] = email

    return render_template(
        'Dashboard.html',
        name=user[1],
        email=user[2],
        mobile=user[3]
    )

@app.route('/profile', methods=['POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    email_session = session['user']

    name = request.form.get('name') 
    mobile = request.form.get('mobile')
    location = request.form.get('location')
    crop = request.form.get('crop')
    language = request.form.get('language')

    cursor = conn.cursor()

    # ✅ Check if already exists
    cursor.execute("SELECT * FROM user_details WHERE email = ?", (email_session,))
    existing = cursor.fetchone()

    if existing:
        # ✅ UPDATE instead of insert
        cursor.execute("""
            UPDATE user_details
            SET name=?, mobile=?, location=?, crop_type=?, language=?
            WHERE email=?
        """, (name, mobile, location, crop, language, email_session))
    else:
        # ✅ INSERT only first time
        cursor.execute("""
            INSERT INTO user_details(name, mobile, email, location, crop_type, language)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, mobile, email_session, location, crop, language))

    conn.commit()

    # ✅ reload dashboard with correct data
    cursor.execute("SELECT * FROM users WHERE email = ?", (email_session,))
    user = cursor.fetchone()

    return render_template(
        'Dashboard.html',
        name=user[1],
        email=user[2],
        mobile=user[3]
    )

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    password = request.form.get('password')

    if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email):
        return "Only @gmail.com emails are allowed"

    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'

    # if not re.match(password_pattern, password):
    #     flash("Weak password", "error")
    #     return redirect(url_for('signup'))
    
    if not re.match(password_pattern, password):
        flash("Password must include uppercase, lowercase, number and special character", "password_error")
        return redirect(url_for('signup'))

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        flash("Email already exists", "email_error")
        return redirect(url_for('signup'))

    # ✅ correct hashing
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    print("INSERTING:", name, email)  # debug

    cursor.execute(
        'INSERT INTO users(name, email, mobile, password) VALUES (?, ?, ?, ?)',
        (name, email, mobile, hashed)
    )
    conn.commit()

    return redirect(url_for('login_page'))

    # cursor.execute('insert into users(name , email , mobile , password)values(? , ? ,? ,?)',(name , email , mobile , hashed ))
    
    # conn.commit()
    # return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


