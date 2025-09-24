import subprocess
import os
import uuid
import shutil
import time
import re
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
    score = db.Column(db.Integer, nullable=False, default=0)
    time_taken = db.Column(db.Float, nullable=False, default=0.0)
    
    user = db.relationship('User', backref=db.backref('submissions', lazy=True))

# --- Secure Code Runner ---
def run_code_with_subprocess(user_code, language, problem_num):
    unique_id, temp_dir = str(uuid.uuid4()), None
    try:
        temp_dir = os.path.join('/tmp', unique_id)
        os.makedirs(temp_dir, exist_ok=True)
        
        problem_dir_source = f'problems/problem {problem_num}'
        ext = _get_ext(language)
        solution_filename = os.path.join(temp_dir, f'solution.{ext}')
        test_case_source = f'{problem_dir_source}/test_cases.{ext}'
        test_case_dest = os.path.join(temp_dir, f'test_cases.{ext}')

        if not os.path.exists(test_case_source):
            return {'success': False, 'message': f'Test cases for Problem {problem_num} ({language}) not found.'}

        with open(solution_filename, 'w') as f:
            f.write(user_code)
        shutil.copy(test_case_source, test_case_dest)

        command = []
        execution_timeout = 20

        if language == 'python':
            command = ['python3', test_case_dest]
        elif language == 'c':
            executable_path = os.path.join(temp_dir, 'a.out')
            compile_proc = subprocess.run(
                ['gcc', test_case_dest, solution_filename, '-o', executable_path],
                capture_output=True, text=True, timeout=10
            )
            if compile_proc.returncode != 0:
                return {
                    'success': False,
                    'score': 0,
                    'message': 'Compilation Failed',
                    'output': compile_proc.stderr
                }
            command = [executable_path]
        else:
            return {'success': False, 'message': f'Language "{language}" is not supported.'}

        start_time = time.time()
        result = subprocess.run(command, capture_output=True, text=True, timeout=execution_timeout)
        end_time = time.time()
        
        output = result.stdout + result.stderr
        time_taken = round(end_time - start_time, 4)

        score = 0
        if language == 'python':
            # unittest format
            if result.returncode == 0 and "OK" in output:
                # Try to parse "Ran X tests" line
                match = re.search(r"Ran (\d+) test", output)
                score = int(match.group(1)) if match else 0
            else:
                score = 0
        elif language == 'c':
            # C prints PASS for each test
            score = output.upper().count('PASS')

        if result.returncode == 0:
            return {
                'success': True,
                'score': score,
                'time_taken': time_taken,
                'message': f'All tests passed! ({score} cases)'
            }
        else:
            return {
                'success': False,
                'score': score,
                'time_taken': time_taken,
                'message': f'Tests failed. ({score} cases passed)',
                'output': output
            }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'score': 0,
            'time_taken': execution_timeout,
            'message': 'Execution timed out.',
            'output': 'Your code took too long to complete.'
        }
    except Exception as e:
        return {
            'success': False,
            'score': 0,
            'message': f'Server execution error: {str(e)}'
        }
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

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
    if not user_id:
        return jsonify({'message': 'Authentication required'}), 401

    if Submission.query.filter_by(user_id=user_id, problem_num=problem_num).first():
        return jsonify({'success': False, 'message': 'Problem already solved.'})

    result = run_code_with_subprocess(data['code'], data['language'], problem_num)
    
    if result.get('success'):
        new_submission = Submission(
            user_id=user_id, 
            problem_num=problem_num, 
            language=data['language'],
            score=result.get('score', 0),
            time_taken=result.get('time_taken', 0.0)
        )
        db.session.add(new_submission)
        db.session.commit()
    return jsonify(result), 200

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    leaderboard_query = db.session.query(
        User.username,
        db.func.sum(Submission.score).label('total_score'),
        db.func.sum(Submission.time_taken).label('total_time')
    ).join(Submission).group_by(User.username).order_by(
        db.desc('total_score'), 
        db.asc('total_time')
    ).all()
    
    leaderboard_data = [
        {'username': user, 'score': score, 'time': round(time, 4)}
        for user, score, time in leaderboard_query
    ]
    return jsonify(leaderboard_data)

@app.route('/user_progress/<int:user_id>', methods=['GET'])
def user_progress(user_id):
    solved_problems = db.session.query(Submission.problem_num).filter_by(user_id=user_id).all()
    solved_list = [p[0] for p in solved_problems]
    return jsonify({'solved': solved_list})

# --- Helper Functions and DB Commands ---
@app.cli.command('init-db')
def init_db_command():
    db.create_all()
    print('Initialized the database.')

@app.cli.command('reset-db')
def reset_db_command():
    db.drop_all()
    db.create_all()
    print('Database has been reset.')

@app.cli.command('clear-leaderboard')
def clear_leaderboard_command():
    try:
        num_rows_deleted = db.session.query(Submission).delete()
        db.session.commit()
        print(f'Leaderboard has been cleared. Deleted {num_rows_deleted} submission(s).')
    except Exception as e:
        db.session.rollback()
        print(f'An error occurred: {e}')

def _get_ext(language):
    return {'python': 'py', 'c': 'c'}.get(language, '')
