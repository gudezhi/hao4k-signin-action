import requests
import os
import re
import json

# hao4k 账户信息
username = os.environ["HAO4K_USERNAME"]
password = os.environ["HAO4K_PASSWORD"]
# 企微通知
corpid = os.environ["corpid"]
corpsecret = os.environ["corpsecret"]

# hao4k 签到 url
user_url = "https://www.hao4k.cn//member.php?mod=logging&action=login"
base_url = "https://www.hao4k.cn/"
signin_url = "https://www.hao4k.cn/plugin.php?id=k_misign:sign&operation=qiandao&formhash={formhash}&format=empty"
form_data = {
    'formhash': "",
    'referer': "https://www.hao4k.cn/",
    'username': username,
    'password': password,
    'questionid': "0",
    'answer': ""
}
inajax = '&inajax=1'

def run(form_data):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'})
    headers = {"Content-Type": "text/html", 'Connection': 'close'}
    user_resp = s.get(user_url,headers=headers)
    login_text = re.findall('action="(.*?)"', user_resp.text)
    for loginhash in login_text:
        if 'loginhash' in loginhash:
            login_url = base_url + loginhash + inajax
            login_url = login_url.replace("amp;", "")
            print(login_url)
    form_text = re.search('formhash=(.*?)\'', user_resp.text)
    print(form_text.group(1))
    form_data['formhash'] = form_text.group(1)
    print(form_data)

    login_resp = s.post(login_url, data=form_data)
    test_resp = s.get('https://www.hao4k.cn/k_misign-sign.html',headers=headers)
    if username in test_resp.text:
      print('login!')
    else:
      return 'login failed!'
    signin_text = re.search('formhash=(.*?)"', test_resp.text)
    signin_resp = s.get(signin_url.format(formhash=signin_text.group(1)))
    test_resp = s.get('https://www.hao4k.cn/k_misign-sign.html',headers=headers)
    if '您的签到排名' in test_resp.text:
      print('signin!')
    else:
      return 'signin failed!'


def sendMsg(data):
    token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+corpid+"&corpsecret="+corpsecret
    base_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
    s = requests.Session()
    s.headers.update(
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'})
    headers = {"Content-Type": "text/html", 'Connection': 'close'}
    user_resp = s.get(token_url, headers=headers)
    # print(user_resp.text)
    access_token = user_resp.json()['access_token']
    form_data = {
        "touser": "GuFeng",
        "msgtype": "text",
        "agentid": 1000002,
        "text": {
            "content": data
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    resp = s.post(base_url+access_token, headers=headers,
                  data=json.dumps(form_data))
    print(resp.json())

if __name__ == "__main__":
  signin_log = run(form_data)
  if signin_log is None:
    send_content = "hao4k 每日签到成功！"
    print('Sign in automatically!')
  else:
    send_content = signin_log
    print(signin_log)
  sendMsg("hao4k 每日签到结果通知：\n" + send_content)
  print('已通知 server 酱')
