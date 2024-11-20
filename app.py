from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/api/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json

    if not data or not all(k in data for k in ("username", "email", "password", "birthdate")):
        return jsonify({"error": "Dados inválidos"}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        birthdate=data['birthdate']
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    users = User.query.all()
    return jsonify([{
        "username": user.username,
        "email": user.email,
        "birthdate": user.birthdate
    } for user in users])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)