from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)
#app.debug = True


@app.route("/", methods=['POST','GET'])
def login():
    if request.method =="POST":
        user = request.form.get["nm"]
        # var2 = request.form["score"]
        return redirect(url_for("user",usr=user))
    else:    
        colours = ['Yes', 'No']
        return render_template('test.html', colours=colours)

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)