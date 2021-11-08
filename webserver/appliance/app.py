from flask import Flask, jsonify
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:QQQ111www222@db.shishko.info:5432/literature"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Literature(db.Model):
    __tablename__ = 'magazines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"{self.name}"

class Literature1(db.Model):
    __tablename__ = 'article_types'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String())

    def __init__(self, id, type):
       self.id = id
       self.type = type

    def __repr__(self):
        return f"{self.type}"

class Literature2(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String())

    def __init__(self, author):
        self.id = id
        self.author = author

    def __repr__(self):
        return f"{self.author}"

class Articles(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    magazines_id = db.Column(db.Integer(), db.ForeignKey('magazines.id'))
    article_type_id = db.Column(db.Integer(), db.ForeignKey('article_types.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('author.id'))

    def __init__(self, magazines_id):
        self.magazines_id = magazines_id

    def __repr__(self):
        return f"{self.magazines_id}"

@app.route("/")
def home():
    liters = Literature.query.all()
    liters1 = Literature1.query.all()
    liters2 = Literature2.query.all()
    return render_template("home.html", liters=liters, liters1=liters1, liters2=liters2)

@app.route("/magazinesadd", methods=['POST'])
def magazinesadd():
    name = request.form["name"]
    entry = Literature(name)
    db.session.add(entry)
    db.session.commit()
    return redirect("/")

@app.route("/articleadd", methods=['POST'])
def articleadd():
    type = request.form["type"]
    entry = Literature1(type)
    db.session.add(entry)
    db.session.commit()
    return redirect("/")

@app.route("/authoradd", methods=['POST'])
def authoradd():
    author = request.form["author"]
    entry = Literature2(author)
    db.session.add(entry)
    db.session.commit()
    return redirect("/")

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    liter = Literature.query.filter_by(name=oldtitle).first()
    liter.name = newtitle
    db.session.commit()
    return redirect("/")

@app.route("/updatearticle", methods=["POST"])
def updatearticle():
    newtitle1 = request.form.get("newtitle1")
    oldtitle1 = request.form.get("oldtitle1")
    liter1 = Literature1.query.filter_by(type=oldtitle1).first()
    liter1.type = newtitle1
    db.session.commit()
    return redirect("/")

@app.route("/updateauthor", methods=["POST"])
def updateauthor():
    newtitle2 = request.form.get("newtitle2")
    oldtitle2 = request.form.get("oldtitle2")
    liter2 = Literature2.query.filter_by(author=oldtitle2).first()
    liter2.author = newtitle2
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    liter = Literature.query.filter_by(name=name).first()
    db.session.delete(liter)
    db.session.commit()
    return redirect("/")

@app.route("/deletearticle", methods=["POST"])
def deletearticle():
    type = request.form.get("type")
    liter1 = Literature1.query.filter_by(type=type).first()
    db.session.delete(liter1)
    db.session.commit()
    return redirect("/")

@app.route("/deleteauthor", methods=["POST"])
def deleteauthor():
    author = request.form.get("author")
    liter2 = Literature2.query.filter_by(author=author).first()
    db.session.delete(liter2)
    db.session.commit()
    return redirect("/")

@app.route("/generated")
def generated():
    return render_template("index.html")

@app.route("/helloworld")
def helloworld():
    return "<p>Hello, World!</p>"

@app.route("/join")
def join():
    jointables = db.session.query(Literature, Articles).join(Articles, Literature.id == Articles.magazines_id).all()
    jointables1 = db.session.query(Literature1, Articles).join(Articles, Literature1.id == Articles.article_type_id).all()
    jointables2 = db.session.query(Literature2, Articles).join(Articles, Literature2.id == Articles.author_id).all()
    data = zip(jointables, jointables1, jointables2)
    return render_template("join.html", data=data, jointables=jointables)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
