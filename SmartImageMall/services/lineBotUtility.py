import requests
import json
from services import sysConfig
from services.dbUtility import createConnection, update, query

replyURL = 'https://api.line.me/v2/bot/message/reply' #lineBot回復端點

getContent = 'https://api-data.line.me/v2/bot/message/%s/content'
#lineBotAPI金鑰
lineBotKey = f'Bearer {sysConfig['LineBotKey']}'

def replyMsg(replyKey, message):
    msg = {
        "replyToken": replyKey,
        "messages":
        [
            {
                "type":"text",
                "text": message
            }
        ]
    }
    header = {"Content-Type" : "application/json", "Authorization" : lineBotKey}
    requests.post(url = replyURL, data = json.dumps(msg), headers = header)

def makeTemplate(altText, type, text):
    if type == 'confirm':
        template = {
            "type": "template",
            "altText": altText,
            "template": {
                "type": "confirm",
                "text": text,
                "actions":[
                    {
                        "type": "message",
                        "label": "是",
                        "text": "對我要買這個, "
                    },
                    {
                        "type": "message",
                        "label": "不是",
                        "text": "好像不是這個"
                    }                     
                ]
            }
        }
    elif type == 'buttons':
        template =  {
            "type": "template",
            "altText": altText,
            "template": {
                "type": "buttons",
                "thumbnailImageUrl": "https://cdn-icons-png.freepik.com/512/625/625599.png",
                "imageAspectRatio": "square",
                "imageSize": "cover",
                "imageBackgroundColor": "#FFFFFF",
                "title": "確認付款",
                "text": "👇點擊下面按鈕付款👇",
                "actions": [
                {
                    "type": "uri",
                    "label": "點我付款",
                    "uri": text
                }
                ]
            }
            }
    return template


def templateMsg(replyKey, type, message):
    msg = {
        "replyToken": replyKey,
        "messages":[makeTemplate(message, type, message)]
    }
    header = {"Content-Type" : "application/json", "Authorization" : lineBotKey}
    requests.post(url = replyURL, data = json.dumps(msg), headers = header)   

def readimage(imageid):
    contectUrl = getContent %imageid
    header = {"Authorization" : lineBotKey}
    response = requests.get(contectUrl, headers= header)
    if response.status_code == 200:
        result = response.content
        with open ('C:/image/temp.jpg', 'wb') as file:
            file.write(result)
    return result

def updateUser(id, displayName = '', language = '', imgurl = '', isfollow = False):
    conn = createConnection()
    result = query(conn, 'select UserID from LineUser Where UserID = %s', id)
    if result == None:
        sql = 'Insert Into LineUser(UserID, DisplayName, PictureURL, Language, IsAcive) values (%s, %s, %s, %s, %d)'
        update(conn, sql, (id, displayName, language, imgurl, isfollow))
    else:
        sql = 'update LineUser set IsAcive = %s where UserID = %s'
        update(conn, sql, (isfollow, id))