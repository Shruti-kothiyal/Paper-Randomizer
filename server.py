from flask import Flask, render_template, url_for, request,redirect
import re
from werkzeug.datastructures import ImmutableMultiDict
import json
import random

app = Flask(__name__)


storage = {}
data = {}


def getdata():
    global data
    data = {"1":["null"],"2":["null"],"3":["null"],"4":["null"],"5":["null"],"6":["null"]}
    for chapter,value in storage.items():
        for innerdata in storage[chapter]["Questions"]:
            data[storage[chapter]["Questions"][innerdata]["priority"]].append(storage[chapter]["Questions"][innerdata]["content"])
    return data 

def chooser(priority,iterations,output):
    global data
    if data[priority].count("null") > 0:
        data[priority].remove("null")
    for i in range(0,iterations):
        choice = random.choice(data[priority])
        output[priority].append(choice)
        data[priority].remove(choice)
        
    if output[priority].count("null") > 0:
        output[priority].remove("null")
    #print(output)
    return output

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', storage=storage)


@app.route("/generate" , methods=["GET", "POST"])
def process():
    global data
    getdata()
    if "easy" in request.form:
        setA = {"1":["null"],"2":["null"]}
        setA = chooser("1",10,setA)
        setA = chooser("2",10,setA)
        setB = {"2":["null"], "3":["null"]}
        setB = chooser("2",2,setB)
        setB = chooser("3",8,setB) 
        return render_template('easy.html',data=data, setA=setA, setB=setB, random=random)
    elif "medium" in request.form:
        setA = {"1":["null"],"2":["null"]}
        setA = chooser("1",6,setA)
        setA = chooser("2",6,setA)
        setB = {"4":["null"]}
        setB = chooser("4",8,setB)
        return render_template('medium.html' ,data=data, setA=setA, setB=setB, random=random)
    elif "hard" in request.form:
        setA = {"4":["null"],"3":["null"]}
        setA = chooser("4",4,setA)
        setA = chooser("3",4,setA)
        setB = {"4":["null"],"3":["null"]}
        setB = chooser("4",4,setB)
        setB = chooser("3",4,setB)
        return render_template('hard.html' ,setA=setA,setB=setB, random=random)
    else:
        return "404 Not Found"


@app.route("/test")
def fill():
    return storage



@app.route("/about")
def about():
    return render_template('about.html', title='About',chapters=5)

@app.route("/results", methods=["GET", "POST"])
def result():
    global storage
    if request.method == "POST":
        resp = ImmutableMultiDict(request.form)
        resp = resp.to_dict(flat=False)
        count = 1
        temp_count = 1 # keeping 1 since every time the question received from frontend would be 1
        print(resp)
        total_question_received = int(re.findall("\d.*",str(list(resp.keys())[-2]))[0])

        if "chapter "+resp["chapter"][0] not in storage:
            count = 1
        else:
            count = int(storage["chapter "+resp["chapter"][0]]["totalcount"])
            count+=1
        
        question_num = "question_no_{}".format(temp_count)
        for key in range(1,(len(list(resp.keys())))):
            if temp_count>total_question_received:
                print(count)
                return redirect("/home", code=302)
                return storage
            if "chapter "+resp["chapter"][0] not in storage:
                storage["chapter "+resp["chapter"][0]] = {"chaptername":resp["chaptername"][0],"totalcount":str(count),"Questions":{str(count):{"content":resp[question_num][0],"priority":resp["priority"][0]}}}
            else:
                question_num = "question_no_{}".format(temp_count)
                storage["chapter "+resp["chapter"][0]]["totalcount"] = str(count) 
                storage["chapter "+resp["chapter"][0]]["Questions"][str(count)] = {"content":resp[question_num][0],"priority":resp["priority"][0]}
            temp_count+=1
            count+=1
                


if __name__ == '__main__':
    app.run(debug=True,port=80,host="0.0.0.0")
