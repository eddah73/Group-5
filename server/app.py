from flask import Flask, request, jsonify, session
from flask_restful import Resource, Api
from flask_migrate import Migrate
from datetime import datetime
from models import db, Note ,User # Adjust as necessary for your file structure

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eddahpr:eddahpr123@localhost/diarynotes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)



class Login(Resource):
  def post(self):
        json = request.get_json()   
        email = json.get('email')
        user= User.query.filter( User.email == email).first()
        password = json.get('password')
  
        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 201

        return {'message': 'Invalid credentials, Try logging in again'}, 401

class CheckSession(Resource):
    def get (self):
        user_id=session.get('user_id')
        if user_id:
            user=User.query.filter(user_id=user_id).first
            return user.to_dict(), 200
        return {'error': 'User not Signed in,please sign in'}, 400
class NotesResource(Resource):
    def get(self):
        notes = Note.query.all()
        return jsonify([note.note_serialize() for note in notes])

    def post(self):
        title = request.json['title']
        content = request.json['content']
        tags = request.json['tags']
        date_str = request.json['date']
        date=datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') 
        new_note = Note(
            title=title,
            content=content, 
            tags=tags,
            date=date
        )
        db.session.add(new_note)
        db.session.commit()
        return new_note.note_serialize(), 201  

class NoteByIdResource(Resource):
    def get(self, id):
        note = Note.query.get(id)
        if not note:
            return {'error': 'Note not found'}, 404
        return jsonify(note.note_serialize())

    def patch(self, id):
        note = Note.query.get(id)
        if not note:
            return {'error': 'Note not found'}, 404
        else:
                  
            note.title = request.json.get('title', note.title)
            note.content = request.json.get('content', note.content)
            note.tags = request.json.get('tags', note.tags)
            note.date = request.json.get('date', note.date)

            db.session.commit()
            return jsonify(note.note_serialize())

    def delete(self, id):
        note = Note.query.get(id)
        if not note:
            return {'error': 'Note not found'}, 404
        
        db.session.delete(note)
        db.session.commit()
        return {'message': 'Note deleted succesfully!'}, 200

class NoteByTitleResource(Resource):
    def get(self, title):
        note = Note.query.filter_by(title=title).first()
        if not note:
            return {'error': 'Note not found'}, 404
        return jsonify(note.note_serialize())

api.add_resource(NotesResource, '/notes')           
api.add_resource(NoteByIdResource, '/notes/<int:id>')
api.add_resource(NoteByTitleResource, '/notes/<string:title>') 


if __name__ == '__main__':
    app.run(port=5555, debug=True)
