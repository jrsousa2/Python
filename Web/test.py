from flask import Flask, redirect, url_for, render_template

app = Flask(__name__,static_folder='D:\\Python\\Web\\static')

full_filename = "D:\\Python\\Web\\static\\Huey.jpg"

@app.route("/") # define how we can access this specific page
def home():
    return render_template("index_bak.html", user_image = full_filename)

if __name__ == "__main__":
    app.run(debug=True)