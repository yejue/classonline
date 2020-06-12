from utils.yuntongxun.CCPRestSDK import REST
import configparser

accountSid = '8aaf0708721773ab0172232c014101f1'
# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。

accountToken = '136ef91ca8a240ce8d47468291d62550'
# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。

appId = '8aaf0708721773ab0172232c01a401f7'
# 请使用管理控制台中已创建应用的APPID。

serverIP = 'app.cloopen.com'
# 说明：请求地址，生产环境配置成app.cloopen.com。

serverPort = '8883'
# 说明：请求端口 ，生产环境为8883.

softVersion = '2013-12-26'  # 说明：REST API版本号保持不变。


def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.items():
        if k == 'templateSMS':
            for k, s in v.item():
                print('{}:{}'.format(k, s))
        else:
            print('%s:%s' % (k, v))

sendTemplateSMS(15807561440, ['1234', 5], 1)