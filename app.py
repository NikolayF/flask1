from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.exceptions import HTTPException

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False)
    text = db.Column(db.String(255), unique=False)
    rating = db.Column(db.Integer, unique=False)

    def __init__(self, author, text, rating = 1):
        self.author = author
        self.text = text
        self.rating = rating

    def __repr__(self):
        return f"Quote({self.author}, {self.text}, {self.rating})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "rating": self.rating
        }

@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code

# Сериализация list[quotes] -> list[dict] -> str

@app.route("/quotes")
def get_quotes():
    quotes = QuoteModel.query.all()
    quotes_as_dict = []
    for quote in quotes:
        quotes_as_dict.append(quote.to_dict())
    return jsonify(quotes_as_dict), 200

#Задание 2.2

@app.route('/quotes/<int:quote_id>')
def show_quote(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is not None:
        return jsonify(quote.to_dict()), 200
    else:
        return abort(404, f"Quote with id={quote} not found")


@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    quote = QuoteModel(new_quote["author"], new_quote["text"])
    db.session.add(quote)
    db.session.commit()
    return jsonify(quote.to_dict()), 201

#Задание 2.2  

@app.route("/quotes/<id>", methods=['PUT'])
def edit_quote(id):
    new_data = request.json
    quote = QuoteModel.query.get(id)
    if quote is not None:
        quote.author = new_data['author']
        quote.text = new_data['text']
        db.session.commit()
        return f"Update quote, id = {id}", 200
    else:
        return abort(404, f"Quote with id={id} not found")

#Задание 2.2

@app.route("/quotes/<id>", methods=['DELETE'])
def delete(id):
    quote = QuoteModel.query.get(id)
    if quote is not None:
        db.session.delete(quote)
        db.session.commit()
        return f"Quote with id {id} is deleted.", 200
    else:
        return abort(404, f"Quote with id={id} not found")

#Задание 2.2

@app.route("/quotes/filter", methods=['GET'])
def filter():
    args = request.args
    author_param = args.get('author')
    rating_param = args.get('rating')
    output = []
    if author_param is not None and rating_param is None:
        quote = QuoteModel.query.filter_by(author=author_param).all()
        for q in quote:
            output.append(q)
    elif author_param is None and rating_param is not None:
        quote = QuoteModel.query.filter_by(rating=rating_param).all()
        for q in quote:
            output.append(q)
    elif author_param is not None and rating_param is not None:
        quote = QuoteModel.query.filter_by(rating=rating_param, author=author_param).all()
        for q in quote:
            output.append(q)
    return jsonify(str(output)), 200


if __name__ == "__main__":
    app.run(debug=True)
