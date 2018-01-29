# -*- coding: utf-8 -*-
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
from src.screct.mykey import *
from subprocess import call
import uuid, time


#Mac OS提示功能
def mac_notify( message, title = "ZB实时交易通知" ):
    cmd = 'display notification \" ' + message  + '\" with title \"' +title +'\"'
    call(["osascript", "-e", cmd])





# 阿里云短息推送功能
def send_sms(business_id, phone_number, sign_name, template_code, template_param=None):
    '''
    #短信模板:
        行情通知: ${market} 价格(RMB)${updown}超过${lastprice}元。
    :param business_id:
    :param phone_number:
    :param sign_name:
    :param template_code:
    :param template_param:
    :return:
    '''
    # ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
    acs_client = AcsClient(SMS_ACCESS_KEY_ID, SMS_ACCESS_KEY_SECRET, "cn-hangzhou")

    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)
    # 短信模板变量参数,友情提示:如果JSON中需要带换行符,请参照标准的JSON协议对换行符的要求,比如短信内容中包含\r\n的情况在JSON中需要表示成\\r\\n,否则会导致JSON在服务端解析失败
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)
    # 短信签名
    smsRequest.set_SignName(sign_name);
    # 短信发送的号码，必填。支持以逗号分隔的形式进行批量调用，批量上限为1000个手机号码,批量调用相对于单条调用及时性稍有延迟,验证码类型的短信推荐使用单条调用的方式
    smsRequest.set_PhoneNumbers(phone_number)
    # 发送请求
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    return smsResponse

    #例子:
    #params = "{\"username\":\"老丁\"}"
    #print send_sms(__business_id, "18680369080", "丁福海", "SMS_102375068", params)
    #print send_sms(__business_id, "18680369080", "丁福海", "SMS_102345067", params)
    #print send_sms(__business_id, "18680369080", "丁福海", "SMS_102375068", params)


if __name__ == '__main__':

    mac_notify("行情开始大涨,请注意")

    #print send_sms(uuid.uuid1(), "18680369080", "丁福海", "SMS_123797121", params)

    market="EOS"
    updown="下跌"
    lastprice=90.0

    msg="zb用户,"+market+updown+"超过"+str(lastprice)

    print "提醒:尊敬的"+msg+"，这是一条测试短信，请忽略。"
    print send_sms(uuid.uuid1(), "18680369080", "丁福海", "SMS_123797121", '{"name":"'+ msg+'"}')