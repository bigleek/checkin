import requests, time, re, rsa, base64, hashlib,sys

tianyi_session = requests.Session()

username = ""
password = ""
cookie = sys.argv[1]

# Server酱报错推送提醒，需要填下下面的key，官网：https://sc.ftqq.com/3.version
SCKEY = ""

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVersion/1.0.6',
    "Host": "https://xn--gmqz83awjh.com",
    "Accept-Encoding": "gzip, deflate",
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'cache-control': 'no-cache',
    'content-length': '0',
    'cookie': f"{cookie}",
    'dnt': '1',
    'origin': 'https://xn--gmqz83awjh.com',
    'pragma': 'no-cache',
    'referer': 'https://xn--gmqz83awjh.com/user',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-requested-with': 'XMLHttpRequest'
}

def pushMessage(data):
    if SCKEY != "":
        return requests.post(f"https://sc.ftqq.com/{SCKEY}.send", data=data)
    else:
        return False



def main():
    # msg = login(username, password)
    # if msg != "error":
    checkin()



# 签到
def checkin():
    rand = str(round(time.time() * 1000))
    url = 'https://xn--gmqz83awjh.com/user/checkin'
    response = tianyi_session.get(url, headers=headers)
    res = response
 
    pushMessage({
            "text": res,
            "desp": str()
    })
    print(res)


# 抽奖
# def lottery(few):
#     url = ''
#     if few == 1: url = 'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN'
#     if few == 2: url = 'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN'
#     if url == '':
#         print('few只能为1或2')
#         return
#     response = tianyi_session.get(url, headers=headers)
#     if "errorCode" in response.text:
#         if response.json()['errorCode'] == "User_Not_Chance":
#             print(f"第{str(few)}次抽奖次数不足")
#         else:
#             if SCKEY != "":
#                 pushMessage({
#                     "text": f"第{str(few)}次抽奖出错",
#                     "desp": response.text
#                 })
#             print(f"第{str(few)}次抽奖出错")
#     else:
#         message = ''
#         if "prizeName" in response.json():
#             message = ",获得" + response.json()['prizeName']
#         print(f"第{str(few)}次抽奖完成{message}")
#
#
# BI_RM = list("0123456789abcdefghijklmnopqrstuvwxyz")


def int2char(a):
    return BI_RM[a]


def b64tohex(a):
    b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    d = ""
    e = 0
    c = 0
    for i in range(len(a)):
        if list(a)[i] != "=":
            v = b64map.index(list(a)[i])
            if 0 == e:
                e = 1
                d += int2char(v >> 2)
                c = 3 & v
            elif 1 == e:
                e = 2
                d += int2char(c << 2 | v >> 4)
                c = 15 & v
            elif 2 == e:
                e = 3
                d += int2char(c)
                d += int2char(v >> 2)
                c = 3 & v
            else:
                e = 0
                d += int2char(c << 2 | v >> 4)
                d += int2char(15 & v)
    if e == 1:
        d += int2char(c << 2)
    return d


def rsa_encode(j_rsakey, string):
    rsa_key = f"-----BEGIN PUBLIC KEY-----\n{j_rsakey}\n-----END PUBLIC KEY-----"
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
    result = b64tohex((base64.b64encode(rsa.encrypt(f'{string}'.encode(), pubkey))).decode())
    return result


def calculate_md5_sign(params):
    return hashlib.md5('&'.join(sorted(params.split('&'))).encode('utf-8')).hexdigest()


def login(username, password):
    url = "https://cloud.189.cn/udb/udb_login.jsp?pageId=1&redirectURL=/main.action"
    r = tianyi_session.get(url)
    captchaToken = re.findall(r"captchaToken' value='(.+?)'", r.text)[0]
    lt = re.findall(r'lt = "(.+?)"', r.text)[0]
    returnUrl = re.findall(r"returnUrl = '(.+?)'", r.text)[0]
    paramId = re.findall(r'paramId = "(.+?)"', r.text)[0]
    j_rsakey = re.findall(r'j_rsaKey" value="(\S+)"', r.text, re.M)[0]
    tianyi_session.headers.update({"lt": lt})

    username = rsa_encode(j_rsakey, username)
    password = rsa_encode(j_rsakey, password)
    url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
        'Referer': 'https://open.e.189.cn/',
    }
    data = {
        "appKey": "cloud",
        "accountType": '01',
        "userName": f"{{RSA}}{username}",
        "password": f"{{RSA}}{password}",
        "validateCode": "",
        "captchaToken": captchaToken,
        "returnUrl": returnUrl,
        "mailSuffix": "@189.cn",
        "paramId": paramId
    }
    try:
        r = tianyi_session.post(url, data=data, headers=headers, timeout=5)
        if r.json()['result'] == 0:
            print(r.json()['msg'])
        else:
            if SCKEY == "":
                print(r.json()['msg'])
            else:
                msg = r.json()['msg']
                print(msg)
                pushMessage({
                    "text": "登录出错",
                    "desp": "错误提示：{msg}"
                })
            return "error"
        redirect_url = r.json()['toUrl']
        r = tianyi_session.get(redirect_url)
        return tianyi_session
    except Exception as e:
        text = "登录账号出现异常!"
        pushMessage({
            "text": text,
            "desp": str(e)
        })
        print(text)


if __name__ == "__main__":
    main()
