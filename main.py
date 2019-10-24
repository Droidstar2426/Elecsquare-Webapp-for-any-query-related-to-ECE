from flask import Flask,redirect,url_for,render_template,request,session
import pickle
import sqlite3
import re
app=Flask(__name__)
def func1(query):
    word=''
    xtest = [query]
    filename3 = 'ecewebmodel.pkl'
    m1 = pickle.load(open(filename3, 'rb'))
    filename2 = 'ecewebmodeltfidf.pkl'
    m2 = pickle.load(open(filename2, 'rb'))
    filename1 = 'ecewebmodelmlb.pkl'
    m3 = pickle.load(open(filename1, 'rb'))
    xtestfinal = m2.transform(xtest)
    print(xtestfinal)
    features = m1.predict(xtestfinal)
    y_value_pred = m3.inverse_transform(features)
    print(y_value_pred)
    if (y_value_pred != [()]):
        for i in y_value_pred:
            print(i[0])
            word=i[0]
    else:
        print("hi")
        word="Not Defined"
    return word

def func2(word):
    finalres="Sorry for the Inconvenience, Your Query is not Found!"
    image=''
    if(word!="Not Defined"):
        sql=sqlite3.connect("ecedb.db")
        cur=sql.cursor()
        cur.execute("SELECT about,image from Glossary where name=?",(word,))
        rows=cur.fetchall()
        for i in rows:
            finalres=i[0]
            image=i[1]
    return finalres,image

@app.route("/",methods=["GET","POST"])
def WelcomePage():
    findisp = 'Your Query will be displayed here'
    image = "https://i.ibb.co/z8XYGc0/quote.png"
    if request.method=="POST":
        query=request.form["Query"]
        # print(query)
        result=func1(query)
        findisp,image=func2(result)
        print(findisp)
    return render_template("WelcomePage.html",display=findisp,image=image)


if __name__=="__main__":
    app.run(debug=True)