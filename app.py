from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from flask_migrate import Migrate

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'quotes.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AuthorModel(db.Model):
   __tablename__ = 'authors'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(32), unique=True)
   quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic')
   surname = db.Column(db.String(32), unique=False)

   def __init__(self, name, surname=''):
       self.name = name
       self.surname = surname

   def to_dict(self):
       return {
           "id": self.id,
           "name": self.name,
           "surname": self.surname
       }

class QuoteModel(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    text = db.Column(db.String(255), unique=False)
    rating = db.Column(db.Integer, nullable=False)


    def __init__(self, author, text, rating=1):
        self.author_id = author.id
        self.text = text
        self.rating = rating


    def __repr__(self):
        return f"Quote({self.author.name}, {self.text}, {self.rating})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author.to_dict(),
            "text": self.text,
            "rating": self.rating,
        }

# Resource: Author

#Задание 3.1
@app.route("/authors")
def get_authors():
    authors = AuthorModel.query.all()
    authors_as_dict = []
    for author in authors:
        authors_as_dict.append(author.to_dict())
    return jsonify(authors_as_dict), 200

#Задание 3.1
@app.route("/authors/<int:author_id>")
def get_author_by_id(author_id):
    author = AuthorModel.query.get(author_id)
    if author is not None:
        return jsonify(author.to_dict()), 200
    else:
        return abort(404, f"Author with id={author} not found")


@app.route("/authors", methods=["POST"])
def create_author():
       author_data = request.json
       author = AuthorModel(author_data["name"])
       db.session.add(author)
       db.session.commit()
       return author.to_dict(), 201

#Задание 3.1
@app.route("/authors/<author_id>", methods=['PUT'])
def edit_author(author_id):
    new_data = request.json
    author = AuthorModel.query.get(author_id)
    if author is not None:
        for key, value in new_data.items():
            setattr(author, key, value)
        db.session.commit()
        return author.to_dict(), 200
    else:
        return abort(404, f"Author with id={author_id} not found")

#Задание 3.1
@app.route("/authors/<author_id>", methods=['DELETE'])
def delete_author(author_id):
    author = AuthorModel.query.get(author_id)
    #return author
    if author is not None:
        db.session.delete(author)
        db.session.commit()
        return f"Author with id {author_id} is deleted.", 200
    else:
        return abort(404, f"Author with id={author_id} not found")


# Resource: Quotes
# Сериализация list[quotes] -> list[dict] -> str

@app.route("/quotes")
def get_quotes():
    quotes = QuoteModel.query.all()
    quotes_as_dict = []
    for quote in quotes:
        quotes_as_dict.append(quote.to_dict())
    return jsonify(quotes_as_dict), 200


@app.route('/quotes/<int:quote_id>')
def show_quote(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is not None:
        return jsonify(quote.to_dict()), 200
    else:
        return abort(404, f"Quote with id={quote} not found")


#Задание 3.1
@app.route("/authors/<int:id>/quotes")
def get_author_quotes(id):
    quotes = QuoteModel.query.filter_by(author_id = id)
    quotes_as_dict = []
    if quotes is not None:
        for quote in quotes:
            quotes_as_dict.append(quote.to_dict())
        return jsonify(quotes_as_dict), 200
    else:
        return abort(404, f"Quote with id={quote} not found")




@app.route("/authors/<int:author_id>/quotes", methods=['POST'])
def create_quote(author_id):
    author = AuthorModel.query.get(author_id)
    new_quote = request.json
    q = QuoteModel(author, **new_quote)
    db.session.add(q)
    db.session.commit()
    return jsonify(q.to_dict()), 201



#Задание 3.1
@app.route("/quotes/<id>", methods=['PUT'])
def edit_quote(id):
    new_data = request.json
    quote = QuoteModel.query.get(id)
    if quote is not None:
        for key, value in new_data.items():
            setattr(quote, key, value)
        db.session.commit()
        return f"Update quote, id = {id}", 200
    else:
        return abort(404, f"Quote with id={id} not found")


#Задание 3.1
@app.route("/quotes/<id>", methods=['DELETE'])
def delete(id):
    quote = QuoteModel.query.get(id)
    if quote is not None:
        db.session.delete(quote)
        db.session.commit()
        return f"Quote with id {id} is deleted.", 200
    else:
        return abort(404, f"Quote with id={id} not found")



@app.route("/quotes/filter", methods=['GET'])
def filter():
    args = request.args
    quotes = QuoteModel.query.filter_by(**args).all()
    result = [quote.to_dict() for quote in quotes]
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)
