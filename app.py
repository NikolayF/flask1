from flask import Flask
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
"text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
},
{
"id": 2,
"author": "Waldi Ravens",
"text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
},
{
"id": 3,
"author": "Mosher’s Law of Software Engineering",
"text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
},
{
"id": 4,
"author": "Yoggi Berra",
"text": "В теории, теория и практика неразделимы. На практике это не так."
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

#Задание 1 и 2
@app.route('/quotes/<int:quote_id>')
def show_quote(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote["text"]   
    return f"Quote with id={quote_id} not found", 404


#Задание 3
@app.route('/quotes/count')
def quote_count():
    return {"Count": str(len(quotes))}


#Задание 4
@app.route('/quotes/random')
def quote_random():
    return choice(quotes)


if __name__ == "__main__":
    app.run(debug=True)