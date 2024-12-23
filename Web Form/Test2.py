from flask import Flask, render_template
import os

#PEOPLE_FOLDER = os.path.join('static')

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
#full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Huey.jpg')

@app.route('/')
@app.route('/index')
def show_index():
    
    return render_template("index2.html")

if __name__ == "__main__":
    app.run(debug=True)    