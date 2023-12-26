from flask import Flask, render_template, request

app = Flask(__name__)

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
    return render_template('sport.html')

@app.route('/success', methods=["GET", "POST"])
def success():
    return render_template("success.html")


if __name__ == '__main__':
    app.run(debug=True)