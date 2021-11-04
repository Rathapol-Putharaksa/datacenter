from flask import Flask, request
from linebot.models import *
from linebot import *
import requests
import json
FIREBASE_HOST ="datacenter-3975d-default-rtdb.asia-southeast1.firebasedatabase.app"
FIREBASE_AUTH= "7sWhgxLOBU37yOo3swUAIGWvuEhcbRzp1kvm7TwC"
SI = {"Temperature":"°C",
    "Humidity":"%"}


channel_secret = "84c3c6325ea9c1f823ac9168fbd529af"
channel_access_token = "srpbG1MswCsie3vDV/vl80pMHaxEQum7RgNFl3dLP56czsREbDPy0BKmNAvOWRu6I20UNJ4ceubNUTuCOLMIWzWqPtV9E3/2B5ziqa/po3hpdkZ+gmUQnDTpuDjWhWYtj9oWYVl56a57SBcBehHfQQdB04t89/1O/w1cDnyilFU="

def callAPI():
    link = "https://{}/.json?auth={}".format(FIREBASE_HOST,FIREBASE_AUTH)
    response = requests.get(link)
    return response.json()

def getValue(location,province,option,response):   
    try:
        
        value = "{} {}".format(response[location][province][option],SI[option] )
       
    except:
        value = "ไม่พบข้อมูล"
    return value

"""
rangsit_123 = "27 C"
rangsit_456 = "25 C"
data = {"ลำปาง":{
    "Temperature":{"123":"22 C","456":"23 C"}
},
 "รังสิต":{
    "Temperature":{"123":"27 C","456":"25 C"} 
 },
  "ท่าพระจันทร์":{
    "Temperature":{"123":"22 C","456":"25 C"} 
 },
 "พัทยา":{
    "Temperature":{"123":"28 C","456":"25 C"} 
 }

}
location_name = ["ลำปาง","รังสิต","ท่าพระจันทร์","พัทยา"]

"""
app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    print(body)
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name
    if (intent == "locationAndOption"):
        response = callAPI()
        msg = ""
        location = req["queryResult"]['parameters']["location"]
        option = req["queryResult"]['parameters']["option"]
        province = req["queryResult"]['parameters']["province"]
    
        for p in province:
            msgL = "{} \n\n".format(p)
            for l in location:
                msgL +="{} \n".format(l)
                for o in option:
                    msgL+="{} = {} \n".format(o ,getValue(l,p,o,response))
            msg+= msgL+"\n"
                
        
    


        reply(intent,text,reply_token,id,disname,msg)
    elif intent == "optionSecond":
        location = req["queryResult"]['outputContexts'][0]['parameters']["location"]
        option = req["queryResult"]['outputContexts'][0]['parameters']["option"]
        reply_cloud(intent,text,reply_token,id,disname,location,option)
    elif intent == "locationSecond":
        location = req["queryResult"]['outputContexts'][0]['parameters']["location"]
        option = req["queryResult"]['outputContexts'][0]['parameters']["option"]
        reply_cloud(intent,text,reply_token,id,disname,location,option)
    


    
    else:
        try:
            location = req["queryResult"]['outputContexts'][0]['parameters']["location"]
            option = req["queryResult"]['outputContexts'][0]['parameters']["option"]
        except:
            location = ""
            option = ""
            room = ""
    print(body)
    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)
    print('location = '+location)
    #print('option = '+option)

    


def reply(intent,text,reply_token,id,disname,msg):
    text_message = TextSendMessage(text=msg)
    line_bot_api.reply_message(reply_token,text_message)

def reply_en(intent,text,reply_token,id,disname,location,room):
    text_message = TextSendMessage(text=data[location][option])
    line_bot_api.reply_message(reply_token,text_message)

def reply_cloud(intent,text,reply_token,id,disname,location,option):
    text_message = TextSendMessage(text=callAPI(location,option))
    line_bot_api.reply_message(reply_token,text_message)




    
    


if __name__ == "__main__":
    app.run()