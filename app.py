from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking, as it is not needed for SQLite
db = SQLAlchemy(app)

# Configure Sessions
app.config['SESSION_PERMANENT'] = False 
app.config['SESSION_TYPE'] = 'filesystem' 
session = Session()
session.init_app(app)

# Define a simple User model
class Registrant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    sport = db.Column(db.String(120), unique=True, nullable=False)


REGISTRANTS = {}

SPORTS = ["Baseball", "Basketball", "Hockey"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/greet', methods=["POST"])
def greet():
    # if "name" in request.args:
    #     name = request.args["name"]
    # else:
    #     name = "world"
        # how to plug the var in the url ?name=David
    
    # request.args.get("name", "world")
    # which retrieves values from query parameters (GET requests).
    name = request.form.get("name", "world")  # Access form data using request.form
    return render_template("greet.html", name = name)

@app.route('/register')
def register():
    return render_template('sport.html', sports = SPORTS)

@app.route('/success', methods=["GET", "POST"])
def success():
    #validate submission
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")
    # Remember registrants
    new_registrant = Registrant(name=name, sport=sport)
    db.session.add(new_registrant)
    db.session.commit()
    # db.execute("INSERT INTO registrants(name, sport) VALUES(?, ?)", name , sport)
    REGISTRANTS[name] = sport
    # return render_template("success.html")
    return redirect("/registrants")

@app.route('/registrants')
def registrants():
    return render_template("registrants.html", registrants=REGISTRANTS)

@app.route('/radio')
def radio():
    return render_template("radio.html", sports = SPORTS)

@app.route('/deregister')
def deregister():
    id = request.form.get('id')
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect('/registrants')
@app.route('/table')
def table():
    return render_template("deregister.html")
# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)