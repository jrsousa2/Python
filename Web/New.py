from flask import Flask, render_template, render_template_string, request

app = Flask(__name__) 

@app.route('/selectusername')
def selectusername_page():

    userlist = [['James'], ['Adam'], ['Mark']]

    return render_template("test2.html", userlist=userlist)

@app.route('/showusername', methods=['POST', 'GET'])
def showusername_page():
    print('args:', request.args)
    print('form:', request.form)

    #currentuser = request.args.get("currentuser")
    currentuser = request.form.get("currentuser")

    return render_template_string('''<h1>Hello {{ currentuser }}</h1>''', currentuser=currentuser)

if __name__ == '__main__':
    app.run(debug=True)