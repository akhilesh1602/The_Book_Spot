from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np
import os
import re



popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pts1.pkl','rb'))
books2 = pickle.load(open('books1.pkl','rb'))
similarity_scores =  pickle.load(open('similarity_scores1.pkl','rb'))

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///the-book-spot.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://mthwnkvmlsvjzp:ec522ca94a36167296640a3c861dc957da3d0ea3a5f41ee1d63dc5bc73807d89@ec2-44-205-177-160.compute-1.amazonaws.com:5432/d19lnnc3bfcl9n"



db = SQLAlchemy(app)

class Books(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    arrival = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(200), nullable=True)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.name} - {self.author}"

@app.route('/books_category', methods=['POST', 'GET'])
def category():
    if request.method == 'POST':
        category = request.form['category']
        books=Books.query.filter(Books.category==category).all()
        return render_template("books.html", books=books)
    
    else:
        return render_template("books.html")


@app.route('/books', methods=['POST', 'GET'])
def books():
    if request.method == 'POST':
        book_name = request.form['name']
        book_author = request.form['author']
        category = request.form['category']
        language = request.form['language']
        arrival = request.form['arrival']
        link = request.form['link']
        image = request.form['image']
        book=Books(name=book_name, author=book_author, category=category, language=language, link=link,arrival= arrival, image=image)
        db.session.add(book)
        db.session.commit()
        return redirect("/books")
    else:
        return render_template("books.html")


@app.route("/")
def home():
    books=Books.query.all()
    new_arrival=Books.query.filter(Books.arrival>=2022).all()
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['book-path'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values),
                           link=list(popular_df['book-link'].values)
                           , books=books, new_arrival=new_arrival)
                           
@app.route("/recommender")
def post():
    return render_template('recommender.html')



@app.route("/recommend_books", methods=["POST"])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]  # calculating index of a book
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[
                    0:6]  # similarity of 1984 book with other books

    data = []
    for i in similar_items:
        item = []
        temp_df = books2[books2['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['book-link'].values))

        data.append(item)
    print(data)
    return render_template('recommender.html',data=data)


if __name__ =="__main__":
    app.run(debug=True, port=8000)