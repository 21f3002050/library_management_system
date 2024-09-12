from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask_caching import Cache
import redis

app = Flask(__name__)

redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})
CORS(app, origins='*')
app.config['JWT_SECRET_KEY'] = 'library'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)



#####################-------MODELS---------##########################

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')
    issued_books = db.relationship('IssueRequest', backref='user', lazy=True)
    

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255), nullable=True)
    ebooks = db.relationship('Ebook', backref='section', lazy=True, cascade="all, delete-orphan")

class Ebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    date_issued = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    issued_to = db.relationship('IssueRequest', backref='ebook', lazy=True)

class IssueRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    issue_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='pending')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    date_given = db.Column(db.DateTime, default=datetime.utcnow)

#####################------LOGIN & SIGNUP----------########################

def create_default_librarian():
    librarian = User.query.filter_by(role='librarian').first()
    if not librarian:
        hashed_password = generate_password_hash('1234', method='sha256')
        librarian = User(
            username='librarian',
            email='librarian@example.com',
            password=hashed_password,
            role='librarian'
        )
        db.session.add(librarian)
        db.session.commit()

class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username cannot be blank")
        parser.add_argument('email', type=str, required=True, help="Email cannot be blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank")
        parser.add_argument('role', type=str, required=True, choices=('user', 'librarian'))
        data = parser.parse_args()

        # Check if the username already exists
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400

        # Hash the password
        hashed_password = generate_password_hash(data['password'], method='sha256')

        # Create a new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            role=data['role']
        )


        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Signup successful'}, 201
    
class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username cannot be blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank")
        data = parser.parse_args()

        # Check if the user exists
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return {'message': 'Invalid username or password'}, 401

        # Create a JWT token
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return {'access_token': access_token, 'role': user.role}, 200

##########################------------SECTION-CRUD-----------################################

@app.route('/api/sections', methods=['GET'])
@jwt_required()
@cache.cached(timeout=2)
def get_sections():
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    sections = Section.query.all()
    return jsonify([{
        'id': section.id,
        'name': section.name,
        'date_created': section.date_created,
        'description': section.description
    } for section in sections]), 200

@app.route('/api/sections', methods=['POST'])
@jwt_required()
def create_section():
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    data = request.json
    new_section = Section(
        name=data.get('name'),
        description=data.get('description')
    )
    db.session.add(new_section)
    db.session.commit()

    return jsonify({"message": "Section created successfully"}), 201

@app.route('/api/sections/<int:id>', methods=['PUT'])
@jwt_required()
def edit_section(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    section = Section.query.get_or_404(id)
    data = request.json

    section.name = data.get('name', section.name)
    section.description = data.get('description', section.description)
    db.session.commit()

    return jsonify({"message": "Section updated successfully"}), 200

@app.route('/api/sections/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_section(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    section = Section.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()

    return jsonify({"message": "Section deleted successfully"}), 200

#######################-------------EBOOK-CRUD----------------#############################

@app.route('/api/sections/<int:section_id>/ebooks', methods=['GET'])
@jwt_required()
@cache.cached(timeout=2)
def get_ebooks(section_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    section = Section.query.get_or_404(section_id)
    ebooks = Ebook.query.filter_by(section_id=section.id).all()

    return jsonify({
        'section_name': section.name,
        'ebooks': [{
            'id': ebook.id,
            'name': ebook.name,
            'author': ebook.author,
            'content': ebook.content
        } for ebook in ebooks]
    }), 200

@app.route('/api/sections/<int:section_id>/ebooks', methods=['POST'])
@jwt_required()
def create_ebook(section_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    data = request.json
    new_ebook = Ebook(
        name=data.get('name'),
        author=data.get('author'),
        content=data.get('content'),
        section_id=section_id
    )
    db.session.add(new_ebook)
    db.session.commit()

    return jsonify({"message": "E-book created successfully"}), 201

@app.route('/api/ebooks/<int:id>', methods=['PUT'])
@jwt_required()
def update_ebook(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    ebook = Ebook.query.get_or_404(id)
    data = request.json

    ebook.name = data.get('name', ebook.name)
    ebook.author = data.get('author', ebook.author)
    ebook.content = data.get('content', ebook.content)
    db.session.commit()

    return jsonify({"message": "E-book updated successfully"}), 200


@app.route('/api/ebooks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ebook(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    ebook = Ebook.query.get_or_404(id)
    db.session.delete(ebook)
    db.session.commit()

    return jsonify({"message": "E-book deleted successfully"}), 200

###################----------USER BACKEND-----------####################

@app.route('/api/user/sections', methods=['GET'])
@jwt_required()
def get_user_sections():
    current_user = get_jwt_identity()
    # Access allowed for all users
    sections = Section.query.all()
    return jsonify([{
        'id': section.id,
        'name': section.name,
        'date_created': section.date_created,
        'description': section.description
    } for section in sections]), 200

@app.route('/api/user/sections/<int:id>/ebooks', methods=['GET'])
@jwt_required()
def get_user_ebooks(id):
    current_user = get_jwt_identity()
    # Access allowed for all users
    section = Section.query.get_or_404(id)
    ebooks = Ebook.query.filter_by(section_id=section.id).all()

    return jsonify({
        'section_name': section.name,
        'ebooks': [{
            'id': ebook.id,
            'name': ebook.name,
            'author': ebook.author,
            'content': ebook.content
        } for ebook in ebooks]
    }), 200

############--------------SEARCH-FUNCTIONALITY-----------#############

class SectionSearch(Resource):
    def get(self):
        search_query = request.args.get('query', '')
        if not search_query:
            return jsonify({'sections': []})

        sections = Section.query.filter(
            (Section.name.ilike(f'%{search_query}%')) |
            (Section.description.ilike(f'%{search_query}%'))
        ).all()

        result = []
        for section in sections:
            result.append({
                'id': section.id,
                'name': section.name,
                'description': section.description,
                'date_created': section.date_created
            })

        return jsonify({'sections': result})
    
class EbookSearch(Resource):
    def get(self, section_id):
        search_query = request.args.get('query', '')
        if not search_query:
            return jsonify({'ebooks': []})

        ebooks = Ebook.query.filter(
            (Ebook.section_id == section_id) &
            ((Ebook.name.ilike(f'%{search_query}%')) |
             (Ebook.author.ilike(f'%{search_query}%')))
        ).all()

        result = []
        for ebook in ebooks:
            result.append({
                'id': ebook.id,
                'name': ebook.name,
                'author': ebook.author,
                'content': ebook.content
            })

        return jsonify({'ebooks': result})
    

###################----------MANAGE REQUESTS-----------#####################

@app.route('/api/user/ebooks/<int:ebook_id>/request', methods=['POST'])
@jwt_required()
def request_ebook(ebook_id):
    current_user = get_jwt_identity()
    user_id = User.query.filter_by(username=current_user['username']).first().id
    
    existing_request = IssueRequest.query.filter_by(user_id=user_id, ebook_id=ebook_id, status='pending').first()
    if existing_request:
        return jsonify({'message': 'E-book request already pending'}), 400

    new_request = IssueRequest(
        user_id=user_id,
        ebook_id=ebook_id,
        status='pending'
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'E-book request submitted successfully'}), 201

@app.route('/api/requests', methods=['GET'])
@jwt_required()
def get_requests():
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    requests = IssueRequest.query.all()
    return jsonify([{
        'id': req.id,
        'user_id': req.user_id,
        'ebook_id': req.ebook_id,
        'request_date': req.request_date,
        'issue_date': req.issue_date,
        'return_date': req.return_date,
        'status': req.status
    } for req in requests]), 200

@app.route('/api/requests/<int:id>', methods=['PUT'])
@jwt_required()
def update_request(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    req = IssueRequest.query.get_or_404(id)
    data = request.json

    if 'status' in data:
        req.status = data['status']
        if req.status == 'approved':
            req.issue_date = datetime.utcnow()
        elif req.status == 'returned':
            req.return_date = datetime.utcnow()

    db.session.commit()
    return jsonify({"message": "Request updated successfully"}), 200

@app.route('/api/user/requests', methods=['GET'])
@jwt_required()
def get_user_requests():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    requests = IssueRequest.query.filter_by(user_id=user.id).all()

    return jsonify([{
        'id': req.id,
        'ebook_id': req.ebook_id,
        'status': req.status,
        'request_date': req.request_date,
        'issue_date': req.issue_date,
        'return_date': req.return_date
    } for req in requests]), 200

@app.route('/api/user/ebooks/<int:ebook_id>/return', methods=['POST'])
@jwt_required()
def return_ebook(ebook_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    request = IssueRequest.query.filter_by(user_id=user.id, ebook_id=ebook_id, status='approved').first()
    
    if request:
        request.status = 'returned'
        request.return_date = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'E-book returned successfully'}), 200
    return jsonify({'message': 'No active request found for this e-book'}), 404

@app.route('/api/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        return jsonify({"message": "Access forbidden: Librarians only"}), 403

    total_requests = IssueRequest.query.count()
    total_ebooks = Ebook.query.count()
    total_sections = Section.query.count()
    total_feedbacks = Feedback.query.count()

    return jsonify({
        'total_requests': total_requests,
        'total_ebooks': total_ebooks,
        'total_sections': total_sections,
        'total_feedbacks': total_feedbacks
    }), 200

api.add_resource(EbookSearch, '/api/user/sections/<int:section_id>/ebooks/search')
api.add_resource(SectionSearch, '/api/user/sections/search')
api.add_resource(LoginResource, '/api/login')
api.add_resource(SignupResource, '/api/signup')





with app.app_context():
    db.create_all()
    create_default_librarian()

if __name__ =="__main__":
    app.run(debug=True)