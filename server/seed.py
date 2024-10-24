from models import db,Note
from app import app

with  app.app_context():
    db.create_all()
    db.session.add(Note(title='First Note', content='This is the first note.', tags='tag1,tag2'))
    db.session.add(Note(title='Second Note', content='This is the second note.', tags='tag3'))
    db.session.add(Note(title='Third Note', content='This the third note.', tags='tag'))
    db.session.commit()