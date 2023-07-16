from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import re




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://test_5cpl_user:ugNXvrq0UNGIFap2bAnxOe9STtnENlEp@dpg-ciprjmd9aq0dcpvqsg10-a.singapore-postgres.render.com/test_5cpl"
db = SQLAlchemy()
db.init_app(app)


class Link(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    link = db.Column(db.String(150), unique=True)
    conn = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()



@app.route('/')
def home():
    records = Link.query.order_by(Link.id.desc()).all()
    all_records = []
    for record in records:
        record_data = {
            'id': record.id,
            'link': record.link,
            'conn': record.conn
        }
        all_records.append(record_data)
    print(all_records)
    return render_template("home.html", data=all_records)

@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        links = request.form["link"]
        print(links)
        match_list = re.findall('https://www.linkedin.com/in/[a-z-0-9]*', links)
        # print(match_list)
        for i in match_list:
            if not Link.query.filter_by(link=i).first():
                add = Link(link=i)
                db.session.add(add)
                db.session.commit()
                print('not true')
        return redirect(url_for('home'))

    if request.method == "GET":
        return redirect(url_for('home'))



@app.route("/delete/<int:id>")
def delete(id):
    record = Link.query.get(id)
    if record:
        db.session.delete(record)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
