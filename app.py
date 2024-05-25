from flask import Flask, render_template, request, Markup
import google.generativeai as palm
import replicate
import os
import sqlite3
import datetime


flag = 1
name = ""
makersuite_api = os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=makersuite_api)


model = {"model" : "models/chat-bison-001"}
app = Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods = ["GET","POST"])
def main():
    global flag, name
    if flag == 1:
        name = request.form.get("q")
        current_time = datetime.datetime.now()
        conn = sqlite3.connect('log.db')
        c = conn.cursor()
        c.execute('INSERT INTO user (name,timestamp) VALUES (?,?)',(name,current_time))
        conn.commit()
        c.close()
        conn.close()
        flag = 0
    return(render_template("main.html",r=name))

@app.route("/prediction",methods = ["GET","POST"])
def prediction():
    return(render_template("prediction.html"))

@app.route("/dbs_price",methods = ["GET","POST"])
def dbs_price():
    q = float(request.form.get("q"))
    return(render_template("dbs_price.html",r=(q*-50.6)+90.2))

@app.route("/generate_text",methods = ["GET","POST"])
def generate_text():
    return(render_template("generate_text.html"))

@app.route("/text_result_makersuite",methods = ["GET","POST"])
def text_result_makersuite():
    q = request.form.get("q")
    r = palm.chat(**model, messages=q)
    return(render_template("text_result_makersuite.html",r=r.last))

@app.route("/generate_image",methods = ["GET","POST"])
def generate_image():
    return(render_template("generate_image.html"))

@app.route("/image_result",methods = ["GET","POST"])
def image_result():
    q = request.form.get("q")
    r = replicate.run("stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
      input = {"prompt":q}
    )
    return(render_template("image_result.html",r=r[0]))

@app.route("/log",methods = ["GET","POST"])
def log():
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    c.execute('SELECT * FROM user')
    r=""
    for row in c:
      r+=str(row) + "<br>"
    r = Markup(r)
    c.close()
    conn.close()
    return(render_template("log.html", r=r))

@app.route("/delete",methods = ["GET","POST"])
def delete():
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    c.execute('DELETE FROM user')
    conn.commit()
    c.close()
    conn.close()
    return(render_template("delete.html"))

@app.route("/end",methods = ["GET","POST"])
def end():
    global flag
    flag = 1
    return(render_template("index.html"))


if __name__ == "__main__":
    app.run()
