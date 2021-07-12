from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
import psy

app = Flask(__name__)
api = Api(app)
CORS(app)
HEROKU_DB = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://puadyvppnbevtd:b99f0a910530926b54fd86b20c6f5a55abf2f2c830d7791b155a6610200cd2d0@ec2-18-206-20-102.compute-1.amazonaws.com:5432/d8dr6hi7dfq9bt'
db = SQLAlchemy(app)


word = reqparse.RequestParser()
word.add_argument("word", type=str, help="word field")
word.add_argument("primary_meaning", type=str, help="primary meaning of the word")
word.add_argument("secondary_meaning", type=str, help="secondary meaning of the word")
word.add_argument("sentence", type=str, help="example sentence")
word.add_argument("synonym", type=str, help="synonyms")
word.add_argument("antonym", type=str, help="antonyms")
#word.add_argument("date_added", type=str, help="date created")

resource_fields = {
    'id': fields.Integer,
    'word': fields.String,
    'primary_meaning': fields.String,
    'secondary_meaning': fields.String,
    'sentence': fields.String,
    'synonym' : fields.String,
    'antonym' : fields.String,
    #'date_added' : fields.DateTime(dt_format='rfc822')
}

class WordTable(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(150), nullable = False)
    primary_meaning = db.Column(db.String(1000), nullable = True)
    secondary_meaning = db.Column(db.String(1000), nullable = True)
    sentence = db.Column(db.String(5000), nullable = True)
    synonym = db.Column(db.String(500), nullable = True)
    antonym = db.Column(db.String(500), nullable = True)
    #date_added = db.Column(db.Date(), nullable = True)



class Word(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        word = WordTable.query.filter_by(id = id).first()
        return word, 200

    @marshal_with(resource_fields)
    def delete(self,id):
        word = WordTable.query.filter_by(id = id).first()
        db.session.delete(word)
        db.session.commit()
        return 204

    @marshal_with(resource_fields)
    def patch(self,id):
        args = word.parse_args()
        result = WordTable.query.filter_by(id=id).first()
        if not result:
            abort(409, message = "Word Not Found")
        result.word = args['word']
        result.primary_meaning = args['primary_meaning']
        result.secondary_meaning = args['secondary_meaning']
        result.sentence = args['sentence']
        result.synonym = args['synonym']
        result.antonym = args['antonym']
        
        db.session.commit()

    
    

class Words(Resource):
    @marshal_with(resource_fields)
    def get(self):
        words = WordTable.query.all()
        if not words:
            abort(404, message="Not found")
        return words
    
    @marshal_with(resource_fields)
    def post(self):
        args = word.parse_args()
        result = WordTable.query.filter_by(word = args['word']).first()
        if result:
            abort(409, message = "Word already present in DB")
        new_word = WordTable(word=args['word'], 
        primary_meaning = args['primary_meaning'], 
        secondary_meaning = args['secondary_meaning'],
        sentence = args['sentence'],
        synonym = args['synonym'],
        antonym = args['antonym'])
        #date_added = args['date_added'])
        db.session.add(new_word)
        db.session.commit()
        return new_word, 201


   

api.add_resource(Word, "/word/<int:id>")
api.add_resource(Words, "/words/")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)


