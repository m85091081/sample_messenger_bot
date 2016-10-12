from flask import Flask, request
import json, requests
###someconfig
app = Flask(__name__)
Auth = "粉絲專頁的 AuthToken"
Verify = "你自己設定的驗證 Token"

###posturl
post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%(Auth)



###answer_machine_method
def answer_machine(recipient_id,string):
    msg = string['message']['text']
    response_message = {'recipient':{'id': recipient_id},'message':{'text':msg}}
    requests.post(post_message_url, json=response_message)
    return 0


###logic_anser 
def logic_answer(recipient_id,string):
    getmsg = string['message']['text']
    if str(getmsg) == "msp":
        msg ="最棒了"
    else:
        msg = "看不懂"
    response_message = {'recipient':{'id': recipient_id},'message':{'text':msg}}
    requests.post(post_message_url, json=response_message)
    return 0


### button_select
def button_select(recipient_id,string):
    getmsg = string['message']['text']
    comment = 'msp真的很棒嗎？'
    title1 = '很棒'
    title2 = '超級棒'
    btnurl = 'https://www.facebook.com/MSPTaiwan/'
    if str(getmsg) == "msp":
        response_message = {'recipient':{'id': recipient_id},'message':{'attachment':{'type':'template','payload':{'template_type':'button','text':str(comment),,'buttons':[{'type':'web_url','url': str(btnurl) ,'title': str(title1)},{'type':'web_url','url': str(btnurl) ,'title': str(title2)}]}}}}
    else:
        msg = "看不懂"
        response_message = {'recipient':{'id': recipient_id},'message':{'text':msg}}
    requests.post(post_message_url, json=response_message)


@app.route("/hooks", methods=['GET', 'POST'])
def fbhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == str(Verify):
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'
        
    elif request.method == 'POST':
        output = json.loads(request.data.decode('utf8'))['entry']
        for event in output:
            messaging = event['messaging']
            for x in messaging:
                recipient_id = x['sender']['id']
                ### answer_machine
                answer_machine(recipient_id,x)
                ### logic_answer
                ## logic_answer(recipient_id,x)
                ### button_select
                ## button_select(recipient_id,x)
        return "Successful"

0
