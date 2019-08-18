import urllib.request
import urllib
import json
import logging
logger = logging.getLogger('account')


# 手机验证码接口
def send_sms(mobile,captcha):
    # flag用于标记短信是否发送成功
    flag = True
    # 短信的API地址
    url = 'https://open.ucpaas.com/ol/sms/sendsms'
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    values = {
         "sid":"6c32b1ab0df397d14b18b4f599671730",
         "token":"245679ca256fd3af201df51c3eed8d7c",
         "appid":"473e1cb2d207447b802ac5345a4c5a7d",
         "templateid":"489851",
         "param":f"{str(captcha)},5",
         "mobile":mobile,
    }

    try:
        # 将字典格式化成bytes格式
        data = json.dumps(values).encode('utf-8')
        logger.info(f"即将发送短信: {data}")
        # 创建一个request,放入我们的地址、数据、头
        request = urllib.request.Request(url, data, headers)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        # html = '{"code":"000000","count":"1","create_date":"2018-07-23 13:34:06","mobile":"15811564298","msg":"OK","smsid":"852579cbb829c08c917f162b267efce6","uid":""}'
        code = json.loads(html)["code"]
        logger.info(f"结果是：{html}")
        if code == "000000":
            logger.info(f"短信发送成功：{html}")
            flag = True
        else:
            logger.info(f"短信发送失败：{html}")
            flag = False
    except Exception as ex:
        logger.info(f"出错了,错误原因：{ex}")
        flag = False
    return flag