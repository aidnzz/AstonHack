from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '385-342-391'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='proposed')  # proposed, active, completed
    budget = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    project_title = db.Column(db.String, db.ForeignKey('project.title'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    project_title = db.Column(db.String, db.ForeignKey('project.title'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mandatory = db.Column(db.Float, default=0)
    essential = db.Column(db.Float, default=0)
    discretionary = db.Column(db.Float, default=0)
    total = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    project_title = db.Column(db.String, db.ForeignKey('project.title'), nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

@app.route("/")
def index():
    return "MAIN PAGE"

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'message': 'Please login first'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Authentication routes
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing credentials'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 401
        
    if check_password_hash(user.password, data['password']):
        session['username'] = user.username
        return jsonify({
            'message': 'Login successful',
            'user': {
                'name': user.name,
                'username': user.username
            }
        })
    
    return jsonify({'message': 'Invalid password'}), 401

@app.route('/auth/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully'})


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(name=data['name']).first():
        return jsonify({'message': 'Name already exists'}), 400
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        name=data['name'],
        username=data['username'],
        password=hashed_password
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'username': user.username} for user in users])

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'username': user.username})

@app.route('/user/<username>', methods=['PUT'])
def update_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='sha256')
    
    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# Project CRUD Operations
@app.route('/project', methods=['POST'])
def create_project():
    data = request.get_json()
    
    if not User.query.filter_by(username=data['created_by']).first():
        return jsonify({'message': 'User not found'}), 404
    
    new_project = Project(
        title=data['title'],
        description=data['description'],
        budget=data['budget'],
        created_by=data['created_by']
    )
    
    try:
        db.session.add(new_project)
        db.session.commit()
        return jsonify({'message': 'Project created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/project', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'status': project.status,
        'budget': project.budget,
        'created_by': project.created_by,
        'created_at': project.created_at
    } for project in projects])

@app.route('/project/<title>', methods=['GET'])
def get_project(title):
    project = Project.query.filter_by(title=title).first()
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    return jsonify({
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'status': project.status,
        'budget': project.budget,
        'created_by': project.created_by,
        'created_at': project.created_at
    })

@app.route('/project/<title>', methods=['PUT'])
def update_project(title):
    project = Project.query.filter_by(title=title).first()
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    data = request.get_json()
    if 'description' in data:
        project.description = data['description']
    if 'status' in data:
        project.status = data['status']
    if 'budget' in data:
        project.budget = data['budget']
    
    try:
        db.session.commit()
        return jsonify({'message': 'Project updated successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/project/<title>', methods=['DELETE'])
def delete_project(title):
    project = Project.query.filter_by(title=title).first()
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'Project deleted successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Contribution CRUD Operations
@app.route('/contribution', methods=['POST'])
def create_contribution():
    data = request.get_json()
    
    # Validate user and project exist
    if not User.query.filter_by(username=data['user_username']).first():
        return jsonify({'message': 'User not found'}), 404
    if not Project.query.filter_by(title=data['project_title']).first():
        return jsonify({'message': 'Project not found'}), 404
    
    new_contribution = Contribution(
        user_username=data['user_username'],
        project_title=data['project_title'],
        amount=data['amount']
    )
    
    try:
        db.session.add(new_contribution)
        db.session.commit()
        return jsonify({'message': 'Contribution created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/contribution', methods=['GET'])
def get_contributions():
    contributions = Contribution.query.all()
    return jsonify([{
        'id': contribution.id,
        'user_username': contribution.user_username,
        'project_title': contribution.project_title,
        'amount': contribution.amount,
        'date': contribution.date
    } for contribution in contributions])

@app.route('/contribution/<int:id>', methods=['GET'])
def get_contribution(id):
    contribution = Contribution.query.get(id)
    if not contribution:
        return jsonify({'message': 'Contribution not found'}), 404
    return jsonify({
        'id': contribution.id,
        'user_username': contribution.user_username,
        'project_title': contribution.project_title,
        'amount': contribution.amount,
        'date': contribution.date
    })

@app.route('/contribution/<int:id>', methods=['PUT'])
def update_contribution(id):
    contribution = Contribution.query.get(id)
    if not contribution:
        return jsonify({'message': 'Contribution not found'}), 404
    
    data = request.get_json()
    if 'amount' in data:
        contribution.amount = data['amount']
    
    try:
        db.session.commit()
        return jsonify({'message': 'Contribution updated successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/contribution/<int:id>', methods=['DELETE'])
def delete_contribution(id):
    contribution = Contribution.query.get(id)
    if not contribution:
        return jsonify({'message': 'Contribution not found'}), 404
    
    try:
        db.session.delete(contribution)
        db.session.commit()
        return jsonify({'message': 'Contribution deleted successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Vote CRUD Operations
@app.route('/vote', methods=['POST'])
def create_vote():
    data = request.get_json()
    
    # Validate user and project exist
    if not User.query.filter_by(username=data['user_username']).first():
        return jsonify({'message': 'User not found'}), 404
    if not Project.query.filter_by(title=data['project_title']).first():
        return jsonify({'message': 'Project not found'}), 404
    
    new_vote = Vote(
        user_username=data['user_username'],
        project_title=data['project_title'],
        vote_type=data['vote_type'],
        comment=data.get('comment')
    )
    
    try:
        db.session.add(new_vote)
        db.session.commit()
        return jsonify({'message': 'Vote created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/vote', methods=['GET'])
def get_votes():
    votes = Vote.query.all()
    return jsonify([{
        'id': vote.id,
        'user_username': vote.user_username,
        'project_title': vote.project_title,
        'vote_type': vote.vote_type,
        'comment': vote.comment,
        'date': vote.date
    } for vote in votes])

@app.route('/vote/<int:id>', methods=['GET'])
def get_vote(id):
    vote = Vote.query.get(id)
    if not vote:
        return jsonify({'message': 'Vote not found'}), 404
    return jsonify({
        'id': vote.id,
        'user_username': vote.user_username,
        'project_title': vote.project_title,
        'vote_type': vote.vote_type,
        'comment': vote.comment,
        'date': vote.date
    })

@app.route('/vote/<int:id>', methods=['PUT'])
def update_vote(id):
    vote = Vote.query.get(id)
    if not vote:
        return jsonify({'message': 'Vote not found'}), 404
    
    data = request.get_json()
    if 'vote_type' in data:
        vote.vote_type = data['vote_type']
    if 'comment' in data:
        vote.comment = data['comment']
    
    try:
        db.session.commit()
        return jsonify({'message': 'Vote updated successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/vote/<int:id>', methods=['DELETE'])
def delete_vote(id):
    vote = Vote.query.get(id)
    if not vote:
        return jsonify({'message': 'Vote not found'}), 404
    
    try:
        db.session.delete(vote)
        db.session.commit()
        return jsonify({'message': 'Vote deleted successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Budget CRUD Operations
@app.route('/budget', methods=['POST'])
def create_budget():
    data = request.get_json()
    
    # Validate user exists
    if not User.query.filter_by(username=data['created_by']).first():
        return jsonify({'message': 'User not found'}), 404
    
    total = data.get('mandatory', 0) + data.get('essential', 0) + data.get('discretionary', 0)
    
    new_budget = Budget(
        name=data['name'],
        mandatory=data.get('mandatory', 0),
        essential=data.get('essential', 0),
        discretionary=data.get('discretionary', 0),
        total=total,
        created_by=data['created_by']
    )
    
    try:
        db.session.add(new_budget)
        db.session.commit()
        return jsonify({'message': 'Budget created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/budget', methods=['GET'])
def get_budgets():
    budgets = Budget.query.all()
    return jsonify([{
        'id': budget.id,
        'name': budget.name,
        'mandatory': budget.mandatory,
        'essential': budget.essential,
        'discretionary': budget.discretionary,
        'total': budget.total,
        'created_by': budget.created_by,
        'created_at': budget.created_at
    } for budget in budgets])

@app.route('/budget/<int:id>', methods=['GET'])
def get_budget(id):
    budget = Budget.query.get(id)
    if not budget:
        return jsonify({'message': 'Budget not found'}), 404
    return jsonify({
        'id': budget.id,
        'name': budget.name,
        'mandatory': budget.mandatory,
        'essential': budget.essential,
        'discretionary': budget.discretionary,
        'total': budget.total,
        'created_by': budget.created_by,
        'created_at': budget.created_at
    })

@app.route('/budget/<int:id>', methods=['PUT'])
def update_budget(id):
    budget = Budget.query.get(id)
    if not budget:
        return jsonify({'message': 'Budget not found'}), 404
    
    data = request.get_json()
    if 'mandatory' in data:
        budget.mandatory = data['mandatory']
    if 'essential' in data:
        budget.essential = data['essential']
    if 'discretionary' in data:
        budget.discretionary = data['discretionary']
    if any(key in data for key in ['mandatory', 'essential', 'discretionary']):
        budget.total = budget.mandatory + budget.essential + budget.discretionary
    
    try:
        db.session.commit()
        return jsonify({'message': 'Budget updated successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/budget/<int:id>', methods=['DELETE'])
def delete_budget(id):
    budget = Budget.query.get(id)
    if not budget:
        return jsonify({'message': 'Budget not found'}), 404
    
    try:
        db.session.delete(budget)
        db.session.commit()
        return jsonify({'message': 'Budget deleted successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Create database tables
with app.app_context():
    db.create_all()

app.run(debug=True)