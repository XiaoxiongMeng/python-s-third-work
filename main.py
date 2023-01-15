from flask import Flask, request, jsonify
import pymysql
import time
app = Flask(__name__)

suser = input('请输入MySQL的用户名user:')
spassword = input('请输入MySQL用户"' + suser + '"的密码:')
db = pymysql.connect(host='localhost', user=suser, password=spassword, database='PYTHON')
c = db.cursor()
nums = c.execute("SELECT * FROM todolist")
print(nums)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/add", methods=['POST'])
def add():  # title, detail, isfinished, deadline
    nums = c.execute("SELECT * FROM todolist")
    infos = request.get_json()
    id = str(nums + 10001)
    try:
        title = infos.get('title')
        detail = infos.get('detail')
        isfns = infos.get('isfinished')
        ddl = infos.get('deadline')
        addtime = str(int(time.time()))
        if not all([title, detail, isfns, ddl]):
            return jsonify(msg="缺少参数", code=400)
        c.execute(
                "insert into python.todolist (title,detail,isfinished,deadline,addline,id) values('" + title + "','" + detail + "','" + isfns + "'," + ddl + "," + addtime+ "," + id + ");")
        db.commit()
        return jsonify(msg='success', code=200,
                       data={"事件标题": title, "事件内容": detail, '是否完成：': isfns, "截止日期：": ddl})
    except Exception as e:
        print(e)
        return jsonify(msg="意外的错误！:"+str(e), code=400)


@app.route("/change", methods=['POST'])
def change():
    infos = request.get_json()
    try:
        title = infos.get('title')
        detail = infos.get('detail')
        isfns = infos.get('isfinished')
        ddl = infos.get('deadline')
        id = infos.get('id')
        if not all([title, detail, isfns, ddl,id]):
            return jsonify(msg="缺少参数", code=400)
        c.execute(
                "UPDATE todolist\nSET title='"+title+"',detail='"+detail+"',isfinished='"+isfns+"',deadline='"+ddl+"'"+"\n"+"where id="+id+";")
        db.commit()
        return jsonify(msg='success', code=200,
                       data={"事件标题": title, "事件内容": detail, '是否完成：': isfns, "截止日期：": ddl})
    except Exception as e:
        return jsonify(msg="意外的错误！:"+str(e), code=400)


@app.route('/findall', methods=['GET'])
def findall():
    try:
        a = []
        c.execute("SELECT * FROM todolist")
        result = c.fetchall()
        length = len(result)
        for i in range(0,length):
            content = {"title":result[i][0],"detail":result[i][1],"isfinished":result[i][2],"deadline":result[i][3],"addline":result[i][4],"id":result[i][5]}
            a.append(content)
        return jsonify(msg="success",code=200,data=a)
    except Exception as e:
        return jsonify(msg="意外的错误！:"+str(e), code=400)


@app.route('/find', methods=['POST'])  # 查找关键字
def find():
    try:
        a = []
        infos = request.get_json()
        mains = infos.get('mains')
        c.execute("select * from todolist where title like '%"+mains+"%';")
        result = c.fetchall()
        length = len(result)
        for i in range(0, length):
            content = {"title": result[i][0], "detail": result[i][1], "isfinished": result[i][2], "deadline": result[i][3],
                   "addline": result[i][4], "id": result[i][5]}
            a.append(content)
        return jsonify(msg="success", code=200, data=a)
    except Exception as e:
        return jsonify(msg="意外的错误！:"+str(e), code=400)


@app.route('/findid', methods=['POST'])
def findid():
    try:
        infos = request.get_json()
        id = infos.get('id')
        c.execute("select * from todolist where id="+id+";")
        result = c.fetchall()
        content = {"title": result[0][0], "detail": result[0][1], "isfinished": result[0][2], "deadline": result[0][3],
                   "addline": result[0][4], "id": result[0][5]}
        return jsonify(msg="success", code=200, data=content)
    except Exception as e:
        return jsonify(msg="意外的错误！:"+str(e), code=400)


@app.route('/delete', methods=['POST'])
def delete(id):
    try:
        infos = request.get_json()
        id = infos.get('id')
        c.execute("delete from todolist where id=" + id + ";")
        db.commit()
        return jsonify(msg="success", code=200)
    except Exception as e:
        return jsonify(msg="意外的错误！:" + str(e), code=400)


@app.route('/deleteall', methods=['GET'])
def deleteall():
    try:
        c.execute("TRUNCATE TABLE python.todolist;")
        db.commit()
        return jsonify(msg="success", code=200)
    except Exception as e:
        return jsonify(msg="意外的错误！:"+str(e), code=400)


@app.route('/deletefns', methods=['GET'])
def deletefns():
    try:
        c.execute("delete from todolist where isfinished='true';")
        db.commit()
        return jsonify(msg="success", code=200)
    except Exception as e:
        return jsonify(msg="意外的错误！:" + str(e), code=400)


@app.route('/deletenfns', methods=['GET'])
def deletenfns():
    try:
        c.execute("delete from todolist where isfinished='false';")
        db.commit()
        return jsonify(msg="success", code=200)
    except Exception as e:
        return jsonify(msg="意外的错误！:" + str(e), code=400)


app.run(host="0.0.0.0")
