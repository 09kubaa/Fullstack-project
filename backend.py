from flask import Flask, request, jsonify,render_template,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/index')
def index():
    return render_template('index.html')  # Wczytanie szablonu index.html

# Formularz rejestracji
@app.route('/formularz')
def formularz():
    return render_template('formularz.html')  # Wczytanie szablonu formularz.html

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

        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Name, email, and password are required"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 400

        hashed_password = generate_password_hash(data['password'])

        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        # Przekierowanie na panel po utworzeniu użytkownika
        return redirect(url_for('show_panel'))
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
    app.run(debug=True)
