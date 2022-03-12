import urllib.parse
import requests
import os
import re
import json

# hao4k 账户信息
username = os.environ["HAO4K_USERNAME"]
saltkey = os.environ["HAO4K_SALTKEY"]
# 企微通知
corpid = os.environ["corpid"]
corpsecret = os.environ["corpsecret"]
pushkey = os.environ["pushkey"]

def sendMsg2Pushdeer(send_content):
    base_url = "https://api2.pushdeer.com/message/push?pushkey="+pushkey+"&text="+urllib.parse.quote(send_content)
    print(base_url)
    resp = requests.get(base_url)

# hao4k 签到 url
user_url = "https://www.hao4k.cn//member.php?mod=logging&action=login"
base_url = "https://www.hao4k.cn/"
signin_url = "https://www.hao4k.cn/plugin.php?id=k_misign:sign&operation=qiandao&formhash={formhash}&format=empty&inajax=1&ajaxtarget=JD_sign"


def run(form_data):
    s = requests.Session()
    headers = {
        'authority': 'www.hao4k.cn',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'dnt': '1',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.hao4k.cn/qiandao/',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'Hm_lvt_6c1cdfd1254d8b1be9c00f4cdfe0c69e=1637551360; HxHg_2132_noticeTitle=1; HxHg_2132_saltkey='+saltkey+'; HxHg_2132_lastvisit=1637547949; HxHg_2132_sendmail=1; HxHg_2132_isms_login_referer=https%3A%2F%2Fwww.hao4k.cn%2Fqiandao%2F; HxHg_2132_seccodeSsDzt=52539.737feacd1c14a59ad6; HxHg_2132_sid=g1CzF9; HxHg_2132_ulastactivity=54859%2BOB6ZR1CwlTdVde6YtmAqOOUoiQTgEio3%2FHmznxgzkR7xn5; HxHg_2132_auth=e01ea2Sj7h7Lqiu54MAdutyWVjV9tzW9ZqiZGzoeYYdNbOOqIc8%2BWZMJU4B2gj%2F%2FpLPoDFcPhwEYYFd%2BEJvkFlusfD4; HxHg_2132_lastcheckfeed=761023%7C1637551596; HxHg_2132_checkfollow=1; HxHg_2132_lip=58.33.129.194%2C1637551358; HxHg_2132_connect_is_bind=0; HxHg_2132_myrepeat_rr=R0; HxHg_2132_curcountl=0; HxHg_2132_checkpm=1; Hm_lpvt_6c1cdfd1254d8b1be9c00f4cdfe0c69e=1637551597; HxHg_2132_lastact=1637551596%09plugin.php%09',
    }

    test_resp = s.get('https://www.hao4k.cn/qiandao/',headers=headers)
    # print(test_resp.text)
    if username in test_resp.text:
      print('login!')
    else:
      return 'login failed!'
    signin_text = re.search('formhash=(.*?)"', test_resp.text)
    signin_resp = s.get(signin_url.format(formhash=signin_text.group(1)),headers=headers)
    print(signin_resp.text)
    test_resp = s.get('https://www.hao4k.cn/qiandao/',headers=headers)
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
  # signin_log = run(form_data)
  signin_log = run({})
  if signin_log is None:
    send_content = "hao4k 每日签到成功！"
    print('Sign in automatically!')
  else:
    send_content = signin_log
    print(signin_log)
  send_content = "每日签到 hao4k\n" + send_content
  sendMsg(send_content)
  print('已通知 server 酱')
  sendMsg2Pushdeer(send_content)
