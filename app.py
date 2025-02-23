from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime
from models import db, ChatSession, ChatMessage  




# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '385-342-391'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


from cba import CBAA
from models import ChatSession, ChatMessage

chatbot = CBAA()

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
    status = db.Column(db.String(20), default='proposed')
    budget = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_title = db.Column(db.String, db.ForeignKey('project.title'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    project_title = db.Column(db.String, db.ForeignKey('project.title'), nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)




# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'message': 'Please login first'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/chat/start', methods=['POST'])
def start_chat():
    chatbot = CBAA()
    session_id = chatbot.create_session(user_id=1)  # Default user_id=1 for testing
    return jsonify({'session_id': session_id})


@app.route('/chat/message/<int:session_id>', methods=['POST'])
def send_message(session_id):
    chatbot = CBAA()
    chatbot.current_session_id = session_id  # Attach to the current session

    # Get user message
    data = request.get_json(force=True)
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    # Check for termination keywords
    if user_message.lower() in ['bye', 'exit', 'quit', 'end']:
        chatbot.end_session()
        return jsonify({'message': 'Chat ended successfully'})

    # Ensure project basics have been collected
    history = chatbot.get_chat_history(session_id)

    if len(history) < 5:  # Assuming you have a context and 4 project basics
        if len(history) == 0:  # Initial request for project description
            prompt = "What would you like to do for your community? Tell me about your project idea:"
        elif len(history) == 1:  # Ask for budget
            prompt = "Do you have a specific amount of money you can use for this project?"
        elif len(history) == 2:  # Ask for timeline
            prompt = "When would you like to do this project? For example: next month, over the summer, etc."
        elif len(history) == 3:  # Ask for helpers
            prompt = "Who will help you with this project? For example: friends, neighbors, volunteers, etc."
        else:
            # All basics have been collected
            project_info = {
                'description': history[0].content,
                'budget': history[1].content,
                'timeline': history[2].content,
                'helpers': history[3].content
            }
            # Get budgeting advice based on collected info
            budget_advice = chatbot.get_budget_advice(project_info)
            return jsonify({'response': budget_advice})

        # Store the chatbot's prompt in chat history
        chatbot.store_message(prompt, is_user=False)
        return jsonify({'response': prompt})

    # If basics are collected, process the user message
    response = chatbot.get_response(user_message)
    return jsonify({'response': response})


@app.route('/chat/message2/<int:session_id>', methods=['POST'])
def send_message2(session_id):
    data = request.get_json(force=True)
    chatbot = CBAA()
    chatbot.current_session_id = session_id
    response = chatbot.get_response(data.get('message', ''))
    return jsonify({'response': response})

@app.route('/chat/history/<int:session_id>', methods=['GET'])
def get_history(session_id):
    chatbot = CBAA()
    messages = chatbot.get_chat_history(session_id)
    return jsonify([{
        'content': msg.content,
        'is_user': msg.is_user,
        'timestamp': str(msg.timestamp)
    } for msg in messages])

@app.route('/chat/end/<int:session_id>', methods=['POST']) 
def end_chat(session_id):
    chatbot = CBAA()
    chatbot.current_session_id = session_id
    chatbot.end_session()
    return jsonify({'message': 'Cheers'})

@app.route("/")
def index():
    return "MAIN PAGE"


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



#Expense CRUD Operations
@app.route('/expense', methods=['POST'])
def create_expense():
   data = request.get_json()
   new_expense = Expense(
       description=data['description'],
       amount=float(data['amount']),
       category=data['category'],
       project_title=data.get('project_title'),
       created_by=data['created_by']
   )
   db.session.add(new_expense)
   db.session.commit()
   return jsonify({'message': 'Expense created successfully'}), 201

@app.route('/expense', methods=['GET'])
def get_expenses():
   expenses = Expense.query.all()
   return jsonify([{
       'id': e.id,
       'description': e.description,
       'amount': e.amount,
       'category': e.category,
       'project_title': e.project_title,
       'created_by': e.created_by,
       'date': e.date
   } for e in expenses])


@app.route('/expense/<int:id>', methods=['GET'])
def get_expense(id):
   expense = Expense.query.get(id)
   return jsonify({
       'id': expense.id,
       'description': expense.description,
       'amount': expense.amount,
       'category': expense.category,
       'project_title': expense.project_title,
       'created_by': expense.created_by,
       'date': expense.date.isoformat()
   })

@app.route('/expense/<int:id>', methods=['PUT'])
def update_expense(id):
   expense = Expense.query.get(id)
   data = request.get_json()
   if 'description' in data: expense.description = data['description']
   if 'amount' in data: expense.amount = float(data['amount'])
   if 'category' in data: expense.category = data['category']
   if 'project_title' in data: expense.project_title = data['project_title']
   db.session.commit()
   return jsonify({'message': 'Expense updated successfully'})

@app.route('/expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
   expense = Expense.query.get(id)
   db.session.delete(expense)
   db.session.commit()
   return jsonify({'message': 'Expense deleted successfully'})

# Create database tables
with app.app_context():
    db.create_all()

app.run(debug=True)
