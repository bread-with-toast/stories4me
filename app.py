from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stories.db"

db = SQLAlchemy(app)
    
class Stories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    story = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return self.id

@app.route("/")
def index():
    return render_template("index.html", stories=Stories.query)

@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        db.session.add(Stories(title=request.form["title"], story=request.form["story"]))
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("create.html")

@app.route("/delete/<int:id>")
def delete(id):
    db.session.delete(Stories.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    if request.method == "POST":
        Stories.query.get_or_404(id).title = request.form["title"]
        Stories.query.get_or_404(id).story = request.form["story"]

        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("update.html", stories=Stories.query)
    

if __name__ == "__main__":
    app.run(debug=True)