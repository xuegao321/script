from flask import Flask
from flask import request
import json
import requests
import sys
import pickle
from dateutil import parser


app = Flask(__name__)

@app.route('/', methods=['POST'])
def alarm():
    data = json.loads(request.data.decode())
#    print(data)
    msg_str = data['message']
    msg = json.loads(msg_str)
    sms = msg['sms_content']
    get_token_url_template = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={ID}&corpsecret={SECRECT}'
    get_token_url = get_token_url_template.format(
                                 ID='ww73***********',
                                 SECRECT='SFqabPQ_DvZJ***********************')
    r_token = requests.get(url=get_token_url)
    token_dic = r_token.json()
    token = token_dic.get('access_token')
    data_body = {
        "toparty" : "2",               # userid 也就是网页上显示的账户对应的值
        "msgtype" : "text",                 # 消息类型为 纯文本
        "agentid" : 1000011,                # 消息类型为 纯文本
        "text" : {
        "content" : sms        #具体消息放在这里
         },
        "safe":0                            # 是否加密传输： 0 不加密  1 加密
    }
    send_msg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'
    r = requests.post(
              url=send_msg_url.format(token),  # 把获取到的 token 格式化进来
              json=data_body                   # 发送的消息体
                  )
#    print(r.status_code)                           # 返回的状态码
#    print(r.text)                                  # 返回的内容
    return '200'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
