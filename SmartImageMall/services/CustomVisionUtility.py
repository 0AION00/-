from services import sysConfig
import requests

url = sysConfig['cvData']['URL']
key = sysConfig['cvData']['Key']

def SharchPhoto(photo):
    CVheaders = {"Content-Type" : "application/octet-stream", "Prediction-Key" : key}
    CVAiResponse = requests.post(url, data = photo, headers = CVheaders)
    predata = CVAiResponse.json()
    predictions = predata['predictions']
    sortTop = sorted(predictions, key=lambda p:p['probability'], reverse = True)
    result = sortTop[0]
    score = result['probability']
    if score > 0.1:
        tagname = result['tagName']
        msg= tagname
    else:
        msg = 'None'
    return msg