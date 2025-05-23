#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',data=[{'name':'Yes'}, {'name':'No'}])

@app.route("/test" , methods=['GET', 'POST'])
def test():
    Q1 = request.form.get('Q1')
    Q2 = request.form.get('Q2')
    Q2a = request.form.get('Q2a')
    Q2b = request.form.get('Q2b')
    Q3 = request.form.get('Q3')

    # SCORES
    R = []

    # Q1
    if Q1=="Yes":
       L = [100,100,80,50] 
    else:
        L = [0,0,0,0] 
    R.append(L)

    # Q2
    if Q2=="Yes":
       L = [0,0,0,100] 
    else:
        L = [0,0,0,0] 
    R.append(L)
    
    # Q2a
    if Q2=="Yes":
       if Q2a=="No":
          L = [0,0,0,50] 
       else:
            L = [50,50,50,0] 
    else:        
        L = [0,0,0,0]
    R.append(L)

    # Q2b
    if Q2=="Yes":
       if Q2b=="No":
          L = [0,0,0,50] 
       else:
            L = [50,50,50,0] 
    else:        
        L = [0,0,0,0]
    R.append(L)

    # Q3
    if Q3=="Yes":
       L = [0,0,0,100] 
    else:
        L = [0,0,0,0] 
    R.append(L)

    # Number of questions
    no_Q = 2
    S = {'PBI':0,'Tableau':0,'TS':0,'Excel':0}
    i=-1
    for key in S:
        S[key]=0 
        i=i+1
        t = list(S).index(key)
        for j in range(no_Q):
            S[key]=S[key]+R[j][i]  
        print(key,"score",S[key])
    #return(str(select)) # just to see what select is
    return f"Hey there <h1>{Q1},{Q2},{S['PBI']}</h1>"

if __name__=='__main__':
    app.run(debug=True)