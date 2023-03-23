from flask import Flask, request, jsonify, abort, g
from pathlib import Path
import sqlite3
from werkzeug.exceptions import HTTPException

BASE_DIR = Path(__name__).parent
DATABASE = BASE_DIR / "test.db"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code

#Сериализация list -> str
@app.route("/quotes")
def get_quotes():
    conn = get_db()
    cursor = conn.cursor()
    select_quotes = "SELECT * FROM quotes"
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchall()
    keys = ["id", "author", "text"]
    #quotes = [dict(zip(keys, quote_db)) for quote_db in quotes_db]  # аналог строк с 52 по 55
    quotes = []
    for quote_db in quotes_db:
        quote = dict(zip(keys, quote_db))
        quotes.append(quote)
    return jsonify(quotes)


@app.route('/quotes/<int:quote_id>')
def show_quote(quote_id):
    conn = get_db()
    cursor = conn.cursor()
    select_quotes = f"SELECT * FROM quotes WHERE id = {quote_id}"
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchone() #Возвращает кортеж или None если нет такой строки
    keys = ["id", "author", "text"]
    if quotes_db is not None:
        quotes = dict(zip(keys, quotes_db))
        return jsonify(quotes), 200
    else:
        return abort(404, f"Quote with id={quote_id} not found")





@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    conn = get_db()
    if "rating" in new_quote:
       if new_quote["rating"] > 5:
           new_quote["rating"] = 1
    else:
       new_quote["rating"] = 1
    cursor = conn.cursor()
    add_quotes = "INSERT INTO quotes (author,text) VALUES (?, ?)"
    cursor.execute(add_quotes, (new_quote['author'], new_quote['text']))
    conn.commit()
    id = cursor.lastrowid
    return f"Insert new quote, id = {id}", 201

##ДЗ по PUT и DELETE

@app.route("/quotes/<id>", methods=['PUT'])
def edit_quote(id):
   new_data = request.json
   conn = get_db()
   cursor = conn.cursor()
   for value in new_data:            
       update_quotes = f"UPDATE quotes SET {value} = ? WHERE ID = ?"
       cursor.execute(update_quotes, (new_data[value], id))
       conn.commit()
   row_count = cursor.rowcount    
   if  row_count > 0:
       return f"Update quote, id = {id}", 200
   else:
       return abort(404, f"Quote with id={id} not found")


   
@app.route("/quotes/<id>", methods=['DELETE'])
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    delete_quotes = f"DELETE FROM quotes WHERE id = ?"
    cursor.execute(delete_quotes, [id])
    row_count = cursor.rowcount
    conn.commit()      
    return f"{row_count} rows deleted. Quote with id {id} is deleted.", 200


@app.route("/quotes/filter", methods=['GET'])
def filter():
    args = request.args
    author = args.get('author')
    rating = args.get('rating')
    output = []
    #for quote in quotes:
        #if all(True if args[key] == str(quote[key] else Flase for key in args)):
        #output.append(quote)
    if author != None and rating == None:
        for quote in quotes:
            if quote["author"] == author:
                output.append(quote)
    elif author == None and rating != None:
        for quote in quotes:
            print(f"{quote['rating']} = {rating}")
            if quote["rating"] == int(rating):
                output.append(quote)
    elif author != None and rating != None:
        for quote in quotes:
            if quote["rating"] == int(rating) and quote["author"] == author:
                output.append(quote)
    return jsonify(output), 200



if __name__ == "__main__":
    app.run(debug=True)