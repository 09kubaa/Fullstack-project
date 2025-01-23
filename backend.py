from flask import Flask, request, jsonify,render_template,redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

with app.app_context():
    db.create_all()

def admin_required(f):
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/index')
def index():
    return render_template('index.html')  # Wczytanie szablonu index.html

# Admin - login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        app.logger.info(f"Username: {username}, Password: {password}")
        # Prosta weryfikacja loginu i hasła
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('admin_login.html', error='Niepoprawne dane logowania')

    return render_template('admin_login.html')

@app.route('/admin/logout', methods=['GET', 'POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


#Admin - panel
@app.route('/admin', methods=['GET'])
@admin_required
def admin_panel():
    users = User.query.all()
    return render_template('admin_panel.html', users=users)

#Usuwanie
@app.route('/admin/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    return "User not found", 404

#Edycja
@app.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        new_name = request.form.get('name', user.name)
        new_email = request.form.get('email', user.email)
        new_password = request.form.get('password')

        # Sprawdź, czy email już istnieje w bazie danych i nie należy do tego samego użytkownika
        existing_email_user = User.query.filter(User.email == new_email, User.id != user_id).first()
        if existing_email_user:
            return render_template(
                'edit_user.html',
                user=user,
                error="Adres email już istnieje"
            )

        # Sprawdź, czy nazwa użytkownika już istnieje w bazie danych i nie należy do tego samego użytkownika
        existing_name_user = User.query.filter(User.name == new_name, User.id != user_id).first()
        if existing_name_user:
            return render_template(
                'edit_user.html',
                user=user,
                error="Nazwa użytkownika już istnieje"
            )

        # Aktualizuj dane użytkownika
        user.name = new_name
        user.email = new_email
        if new_password:
            user.password = generate_password_hash(new_password)
        db.session.commit()
        return redirect(url_for('admin_panel'))

    return render_template('edit_user.html', user=user)


# Formularz rejestracji
@app.route('/formularz')
def formularz():
    app.logger.info("Wywołano trasę /formularz")
    return render_template('formularz.html')

# Panel użytkownika
@app.route('/panel')
def panel():
    users = User.query.all()  # Pobierz użytkowników z bazy danych (przykład)
    return render_template('panel.html', users=users)  # Wczytanie szablonu panel.html

    
@app.route('/users', methods=['POST'])
def create_user():
    try:
        if request.content_type == 'application/json':
            data = request.json
        elif request.content_type == 'application/x-www-form-urlencoded':
            data = request.form.to_dict()
        else:
            return jsonify({"error": "Unsupported Media Type"}), 415

        app.logger.info(f"Received data: {data}")

        # Weryfikacja wymaganych pól
        if not data.get('name') or not data.get('email') or not data.get('password') or not data.get('confirm_password'):
            return render_template('formularz.html', error="Wypełnij wszystkie pola")
        if data['password'] != data['confirm_password']:
            return render_template('formularz.html', error="Hasła się nie zgadzają")

        if User.query.filter_by(email=data['email']).first():
            return render_template('formularz.html', error="Podany adres email jest już zajęty")
        
        if User.query.filter_by(name=data['name']).first():
            return render_template('formularz.html', error="Podana nazwa użytkownika jest już zajęta")
        
        hashed_password = generate_password_hash(data['password'])

        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('panel'))
    except Exception as e:
        app.logger.error(f"Error: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
    
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad request"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5500)
