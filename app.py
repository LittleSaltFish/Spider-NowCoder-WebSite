from flask import Flask, render_template, request, g
import sys
import sqlite3 as sql

app = Flask(__name__)


DATABASE = "./static/Data.db"


def connect_db():
    return sql.connect(DATABASE)


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [
        dict((cur.description[idx][0], value) for idx, value in enumerate(row))
        for row in cur.fetchall()
    ]
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, "db"):
        g.db.close()


@app.route("/")
def home():
    ret = []
    for data in query_db("select * from `NowCoder-Data` ORDER BY RANDOM() limit 20"):
        data.pop('JobRequest')
        data.pop('Introduction') 
        ret.append(data)
    print(ret)
    return render_template("home.html", data=ret)


@app.route("/Analyse")
def student():
    return render_template("DataAnalyse.html")


@app.route("/Result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        flag=False
        result=[]
        print("=========================")
        print(f"input={request.form.get('InputText')}")
        input = request.form.get("InputText")
        for data in query_db(f"select * from `NowCoder-Data` where Company like '%{input}%' ORDER BY RANDOM() limit 50"):
            data.pop('JobRequest')
            data.pop('Introduction') 
            result.append(data)
        for data in query_db(f"select * from `NowCoder-Data` where JobName like '%{input}%' ORDER BY RANDOM() limit 50"):
            data.pop('JobRequest')
            data.pop('Introduction')
            result.append(data)
        print(result)
        if len(result)!=0:
            flag=True
        return render_template("SearchResult.html", Result=result,Flag=flag)
    else:
        print(request.method)
        print(f"input={request.form.get('InputText')}")
        return render_template(
            "result.html",
            result={
                "InputText": "网页出现错误，请联系邮箱：saltfish@whut.edu.cn",
                "result": "ERROR",
            },
        )


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5001,debug=True)
