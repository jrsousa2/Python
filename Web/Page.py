from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

full_filename = "Huey.jpg"

@app.route("/") # define how we can access this specific page
def home():
    return render_template("index.html", content=['SP','RJ','NY'], user_image = full_filename)

#@app.route("/<name>")
#def user(name):    
    #return f"Hello {name}!"

#@app.route("/admin")
#def admin():
#    return redirect(url_for("user",name="Admin!"))

if __name__ == "__main__":
    app.run(debug=True)