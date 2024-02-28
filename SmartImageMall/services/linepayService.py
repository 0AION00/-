from services import app
from services import sysConfig
from flask import request, make_response
from services.dbUtility import update, createConnection
from datetime import datetime
import requests
import random
import uuid
import json
import hashlib
import base64
import hmac

CID = sysConfig['LinePayData']['ChannelID']
CSkey = sysConfig['LinePayData']['ChannelSecretKey']    #linepay金鑰
linepayApiUrl = 'https://sandbox-api-pay.line.me/v3/payments/request' #linepay測試用API

#生成Authorization加密字串,給header使用
def getAuthCrypy(key, Url, order, nonce):
    text = key+Url+order+nonce
    return base64.b64encode(hmac.new(str.encode(key), str.encode(text), digestmod = hashlib.sha256).digest()).decode('utf8')    #用base64+hmac+sha256進行加密

@app.route('/api/v1/line/linepay', methods = ["GET"])
def linepaySystem(amount = 0, orderid = '', quantity = 0, productid = '', productname = '', lineText = False):
    if lineText:
        data = {
            'orderid': orderid,
            'productid': productid,
            'productname': productname,
            'amount': amount,
            'quantity': quantity,
            'totalamount': amount * quantity
        }
    else:
        data = {
            'orderid': request.args.get('oid'),
            'productid': request.args.get('pid'),
            'productname': request.args.get('pn'),
            'amount': int(request.args.get('a')),
            'quantity': int(request.args.get('q')),
            'totalamount': int(request.args.get('a')) * int(request.args.get('q'))
        }
    OrderData = {
        'amount': data["totalamount"],
        'currency': 'TWD',
        'orderId' : data["orderid"],
        "packages" :[
            {
                "id" : data["productid"],
                "amount" : data["amount"] * data["quantity"],
                "name" : data["productname"],
                "products": [
                    {
                        "name": data["productname"],
                        "quantity":data["quantity"],
                        "price":data["amount"]
                    }
                ]
            }
        ],
        "redirectUrls" :{
            "confirmUrl" : " https://66fe-59-127-190-15.ngrok-free.app/api/v1/linepay/complete",    #確認後回到的網頁位子
            "cancelUrl" : "https://www.sample.com"      #取消後回到的網頁位子
        }
    }
    nonce = str(uuid.uuid4())   #生成UUID4唯一識別碼
    requestURL = '/v3/payments/request' #加密字串用URL
    order = json.dumps(OrderData)     #將產品資訊轉為json物件
    myHeader = {"Content-Type": "application/json", "X-LINE-ChannelId" : CID, "X-LINE-Authorization-Nonce" : str(nonce), "X-LINE-Authorization" : getAuthCrypy(CSkey, requestURL, order, nonce)}
    response = requests.post(linepayApiUrl,data = json.dumps(OrderData), headers = myHeader)
    result = response.json()
    payUrl = result['info']['paymentUrl']['web']    #回傳linepay支付網址
    return payUrl

@app.route('/api/v1/linepay/complete', methods = ["GET"])
def completePay():
    orderid = request.args.get('orderId')
    time = str(datetime.now())
    conn = createConnection()
    update(conn, 'update Orders set state = 3, finishDate = %s where OrderID = %s', (time, orderid))
    response = make_response('', 204)
    return response