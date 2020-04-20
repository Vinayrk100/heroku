import flask
from flask import Flask
from flask_mail import Mail, Message

from promotion import rfm_score
# from recommendation import recommend_books
from unique_books import read_book_details
from books_recommendation_for_user import recommend_books_userbased
from content_based_recommendation import content

app = flask.Flask(__name__, template_folder='templates')
# email = flask.request.form.get('email')

mail = Mail()

app = Flask(__name__)

app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'vinayrk100@gmail.com'
app.config["MAIL_PASSWORD"] = 'Vinay@1996'

mail.init_app(app)


# # Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    # if flask.request.method == 'GET':
    return flask.render_template('welcome.html')


@app.route('/books', methods=['GET', 'POST'])
def api_books():
    if flask.request.method == "POST":
        # name = flask.request.form["name"]
        uid = int(flask.request.form["uid"])
        purchased_books, recommendations_genre, recommendations_author, \
        recommendations_bookpages = recommend_books_userbased(uid)
        segment, promo, colors = rfm_score(uid)
    return flask.render_template('booksdetails.html',
                                 uid=uid,
                                 segment=segment,
                                 promo=promo.values.tolist(),
                                 colors=colors,
                                 purchased_books=purchased_books.values.tolist(),
                                 recommendations_genre=recommendations_genre.values.tolist(),
                                 recommendations_author=recommendations_author.values.tolist(),
                                 recommendations_bookpages=recommendations_bookpages.values.tolist())


@app.route('/recommendation', methods=['POST'])
def api_reco():
    first_line = True
    title = flask.request.form["title"]
    uid = int(flask.request.form["uid"])
    book, user = read_book_details(title, uid)
    return flask.render_template('recommendation.html',
                                 book_details=book.values.tolist(),
                                 user=user.values.tolist())


@app.route('/purchase', methods=['POST'])
def api_purchase():
    sub = flask.request.form["sub"]
    uname = flask.request.form["uname"]
    uid = flask.request.form["uid"]
    # booktitle = flask.request.form["booktitle"]
    booktitle = "the secret life of bees"

    if sub == "Purchase":
        booktitle = flask.request.form["booktitle"]
        price = flask.request.form["price"]
        email = flask.request.form["email"]

        msg = Message('Recommendation', sender='vinayrk100@gmail.com', recipients=[email])
        msg.body = "Hi, Please find your recommended books below" + booktitle + price

        mail.send(msg)
        # form details
        # book = content(booktitle)
        return flask.render_template('purchase.html', uname=uname)
    else:
        book = content(booktitle)
        return flask.render_template('content_based_suggestions.html',
                                     book_details=book.values.tolist(),
                                     user=uid)


if __name__ == '__main__':
    app.run(debug=True)
