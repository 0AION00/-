from services import app
from flask import render_template, request, make_response
from services.dbUtility import update, createConnection
import json

@app.route('/menberregister')
def register():
    reg = render_template('menberregister.html')
    return reg

@app.route('/api/v1/menber/add', methods = ['POST'])
def registerAdd():
    member = request.get_json()
    print(member)
    response = make_response()
    if member['access'] != '' and member['password'] != '' and member['nickname'] != '' and member['email'] != '':
        try:
            conn = createConnection()
            sql = 'Insert Into Customer(account, password, customerName, email) values (%s, %s, %s, %s)'
            result = update(conn, sql, (member['access'], member['password'], member['nickname'], member['email']))
            print(result)
            msg = {'code' : 200, 'msg' : '註冊成功'}
            response.status_code = 200
        except Exception as ex:
            print(ex)
            msg = {'code' : 400, 'msg' : '註冊失敗'}
            response.status_code = 400
    else:
        msg = {'code' : 400, 'msg' : '有資料沒輸入喔'}
        response.status_code = 400
    response.content_type = 'application/json'
    response.set_data(json.dumps(msg))
    return response
