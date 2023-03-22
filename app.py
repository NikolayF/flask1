from flask import Flask, request
from random import choice

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

about_me = {
    "name": "Евгений",
    "surname": "Юрченко",
    "email": "eyurchenko@specialist.ru"
}


quotes = [
{
"id": 1,
"author": "Rick Cook",
"text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
"rating" : 4
},
{
"id": 2,
"author": "Waldi Ravens",
"text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
"rating" : 5
},
{
"id": 3,
"author": "Mosher’s Law of Software Engineering",
"text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
"rating" : 1
},
{
"id": 4,
"author": "Yoggi Berra",
"text": "В теории, теория и практика неразделимы. На практике это не так.",
"rating" : 2
}
]

@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/about")
def about():
    return about_me

#Сериализация list -> str
@app.route("/quotes")
def get_quotes():
    return quotes


@app.route('/quotes/<int:quote_id>')
def show_quote(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote["text"]   
    return f"Quote with id={quote_id} not found", 404



@app.route('/quotes/count')
def quote_count():
    return {"Count": str(len(quotes))}



@app.route('/quotes/random')
def quote_random():
    return choice(quotes)

#####Практика: Часть 2
#####Выполнил вместе с дополнительными заданиями

@app.route("/quotes", methods=['POST'])
def create_quote():
   new_quote = request.json
   last_quote = quotes[-1]
   new_id = last_quote["id"] + 1
   new_quote["id"] = new_id
   if "rating" in new_quote:
       if new_quote["rating"] > 5:
           new_quote["rating"] = 1
   else:
       new_quote["rating"] = 1
   quotes.append(new_quote)
   return new_quote, 201


@app.route("/quotes/<id>", methods=['PUT'])
def edit_quote(id):
   new_data = request.json
   for quote in quotes:      
    if quote["id"] == int(id):
            try:                
                quote.update(author=new_data["author"])
            except:
                pass
            try:                               
                quote.update(text=new_data["text"])
            except:
                pass
            return quote, 200
    else:
        return f"Quote with id={id} not found", 404

   
@app.route("/quotes/<id>", methods=['DELETE'])
def delete(id):
   for quote in quotes:
       if quote["id"] == int(id):            
            del quotes[quotes.index(quote)] 
            return f"Quote with id {id} is deleted.", 200
   else:
       return f"Quote with id={id} not found", 404


@app.route("/quotes/filter", methods=['GET'])
def filter():
    args = request.args
    author = args.get('author')
    rating = args.get('rating')
    output = []
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
    return output



if __name__ == "__main__":
    app.run(debug=True)