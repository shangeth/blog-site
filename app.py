from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from models import *
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://odsvlqckromdtx:aabce53cdcb5040d092e396505cfe6064cde7f7ea79d811dcb28338687bddf37@ec2-54-221-192-231.compute-1.amazonaws.com:5432/d6vulp02317s80'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route('/')
def index():
    posts = Blogpost.query.all()

    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    date = post.date_posted.strftime('%d %B, %Y')
    return render_template('post.html',post=post,date_posted=date)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "GET":
        return render_template('add.html')
    elif request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        author = request.form["author"]
        content = request.form["content"]
        date = datetime.now()
        post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=date)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
