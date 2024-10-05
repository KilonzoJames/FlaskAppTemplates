from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Sessions
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production

Session(app)


# Define a simple User model
class Registrant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    sport = db.Column(db.String(120), nullable=False)

# REGISTRANTS = {}

SPORTS = ["Baseball", "Basketball", "Hockey"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/greet', methods=["POST"])
def greet():
    # name = request.args.get("name", "world")
    # how to plug the var in the url ?name=David
    # request.args is only used when using get method and post method doesn't show details in the url
    # which retrieves values from query parameters (GET requests).
    name = request.form.get("name", "world")  # Access form data using request.form
    return render_template("greet.html", name = name)

@app.route('/both', methods = ["GET", "POST"])
def both():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        if "name" in request.form:
            name = request.form["name"]
        else:
            name = "world"
        return render_template("greet.html", name = name)

@app.route('/register')
def register():
    return render_template('sport.html', sports = SPORTS)

@app.route('/success', methods=["GET", "POST"])
def success():
    name = request.form.get("name")
    sport = request.form.get("sport")
    # Validate submission
    if not name or sport not in SPORTS or Registrant.query.filter_by(name=name).first():
        return render_template("failure.html")
    # Add registrant to the database
    new_registrant = Registrant(name=name, sport=sport)
    db.session.add(new_registrant)
    db.session.commit()
    return redirect("/deregister")

    # REGISTRANTS[name] = sport
    # return render_template("success.html")
    # db.execute("INSERT INTO registrants(name, sport) VALUES(?, ?)", name , sport)

@app.route('/registrants')
def registrant():
    registrants = Registrant.query.all()
    return render_template("registrants.html", registrants=registrants)

@app.route('/radio')
def radio():
    return render_template("radio.html", sports = SPORTS)

@app.route('/deregister', methods = ["GET", "POST"])
def deregister():
    if request.method == "GET":
        registrants = Registrant.query.all()
        return render_template("deregister.html", registrants=registrants)
    elif request.method == "POST":
        id = request.form.get('id')
        if id:
            # Remove registrant by id
            registrant_to_delete = Registrant.query.get(id)
            if registrant_to_delete:
                db.session.delete(registrant_to_delete)
                db.session.commit()
                flash(f"Registrant '{registrant_to_delete.name}' has been successfully deregistered.", "success")
            else:
                flash("Registrant not found.", "error")
        else:
            flash("Invalid ID provided.", "error")
        return redirect('/deregister')
        # db.execute("DELETE FROM registrants WHERE id = ?", id)

@app.route("/session")
def sessions():
    if not session.get("name"):
        return redirect("/login")
    return render_template("session.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Store the name in session after form submission
        session["name"] = request.form.get("name")
        return redirect("/session")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()  # This will clear all session data, including the session cookie
    return redirect("/login")


# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)