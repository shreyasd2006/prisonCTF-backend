import subprocess
import os
import uuid
import shutil
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# --- Configuration ---
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_default_dev_secret_key_for_local_testing')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ctf.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    problem_num = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(20), nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('submissions', lazy=True))

# --- Secure Code Runner ---
def run_code_with_subprocess(user_code, language, problem_num):
    unique_id = str(uuid.uuid4())
    temp_dir = os.path.join('/tmp', unique_id)
    try:
        os.makedirs(temp_dir, exist_ok=True)
        problem_dir_source = f'problems/problem {problem_num}'
        solution_filename = os.path.join(temp_dir, f'solution.{_get_ext(language)}')
        test_case_source = f'{problem_dir_source}/test_cases.{_get_ext(language)}'
        test_case_dest = os.path.join(temp_dir, f'test_cases.{_get_ext(language)}')
        
        if not os.path.exists(problem_dir_source) or not os.path.exists(test_case_source):
            return {'success': False, 'message': f'Problem {problem_num} files not found on server.'}

        with open(solution_filename, 'w') as f: f.write(user_code)
        shutil.copy(test_case_source, test_case_dest)

        if language == 'python':
            command = ['python3', test_case_dest]
        elif language == 'c':
            executable_path = os.path.join(temp_dir, 'a.out')
            compile_proc = subprocess.run(['gcc', test_case_dest, solution_filename, '-o', executable_path], capture_output=True, text=True, timeout=10)
            if compile_proc.returncode != 0: return {'success': False, 'message': 'Compilation Failed', 'output': compile_proc.stderr}
            command = [executable_path]
        else:
            return {'success': False, 'message': f'Language "{language}" not supported.'}

        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0: return {'success': True}
        else: return {'success': False, 'message': 'Tests Failed', 'output': result.stdout + result.stderr}

    except subprocess.TimeoutExpired:
        return {'success': False, 'message': 'Execution timed out.'}
    except Exception as e:
        return {'success': False, 'message': f'Server execution error: {str(e)}'}
    finally:
        if os.path.exists(temp_dir): shutil.rmtree(temp_dir)

# --- API Endpoints ---
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    return jsonify({'message': 'Login successful', 'userId': user.id})

@app.route('/validate', methods=['POST'])
def validate_solution():
    data = request.get_json()
    user_id, problem_num = data.get('userId'), data.get('problem')
    if not user_id: return jsonify({'message': 'Authentication required'}), 401

    if Submission.query.filter_by(user_id=user_id, problem_num=problem_num).first():
        return jsonify({'success': False, 'message': 'Problem already solved.'})

    # CRITICAL SECURITY NOTE: For a high-stakes competition, replace this with a Docker-based runner.
    result = run_code_with_subprocess(data['code'], data['language'], problem_num)
    
    if result.get('success'):
        new_submission = Submission(user_id=user_id, problem_num=problem_num, language=data['language'])
        db.session.add(new_submission)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Correct!'})
    else:
        return jsonify(result), 200

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    users_by_score = db.session.query(
        User.username,
        db.func.count(Submission.problem_num).label('score')
    ).join(Submission).group_by(User.username).order_by(db.desc('score')).all()
    leaderboard_data = [{'username': user, 'score': score} for user, score in users_by_score]
    return jsonify(leaderboard_data)

@app.route('/user_progress/<int:user_id>', methods=['GET'])
def user_progress(user_id):
    solved_problems = db.session.query(Submission.problem_num).filter_by(user_id=user_id).all()
    solved_list = [p[0] for p in solved_problems]
    return jsonify({'solved': solved_list})

# A command to initialize the database
@app.cli.command('init-db')
def init_db_command():
    db.create_all()
    print('Initialized the database.')

def _get_ext(language):
    return {'python': 'py', 'c': 'c'}.get(language, '')