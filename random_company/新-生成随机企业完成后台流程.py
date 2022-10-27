# coding:utf-8
import base64
import requests
import json
import datetime
import time
import  logging
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import pymysql
from faker import Faker

# 依赖
# pip3 install pymysql
# pip3 install faker
def current_time():
    """当前日期时间"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def log_time():
    return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

def generate_company_name():
    """
    随机产生一个企业名称
    :return:
    """
    f = Faker(locale='zh_cn')
    fack_name = f.city() + f.company()
    return  fack_name
def generate_mobile():
#     """
#     随机产生一个手机号
#     :return:
#     """
    f = Faker(locale='zh_cn')
    fack_mobile = f.phone_number()
    return  fack_mobile
class BackManager(object):
    """日志配置"""
    logging.basicConfig(level=logging.INFO,
                        filename='./log%s.text' % (log_time()),
                        filemode='w',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d]- %(levelname)s: %(message)s')
    # 根据参数生成对应环境的初始数据
    def __init__(self, username, password,env_code,company_name,phone):
        # 公共请求头
        self.common_header = {
            'content-type': 'application/json;charset=UTF-8',
            'authorization': None,
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        self.username = username
        self.password = password
        self.company_name = company_name
        self.phone = phone
        self.company_code = company_code
        # 环境判断：1-test环境，2-UAT环境，3-PRE环境
        if env_code == 1 :
            self.host_api_ustax = 'https://api.test.ustax.tech'
            self.host_api = 'https://api.localtest.zlbzb.cn'
            self.host_zlb_manage = 'http://manage.localtest.zlbzb.cn'
            #后台的用户id，判断数据权限
            # self.common_header["user-id"] = '1519140003799224321'

            self.common_header["user-id"] = '1460811657615958018'

            #场景为信息技术服务/互联网技术服务"
            # self.tradeId = 23
            # self.tax_item_id = 26

            # #发布API任务时税目为：6-9-11-13的一级税目/二级-6%的税目
            # self.tradeId = 52
            # self.tax_item_id = 46
            # self.parkId = 395098863620325376
            # self.parkName = '开封园区'
            # self.tax_item = '信息技术服务/互联网技术服务'
            # self.tax_item = '经纪代理服务>其他经纪代理服务'
            self.tradeId = 188918816263110656
            self.tax_item_id = 188918289076846592
            self.parkId = 188915292234055680
            self.parkName = '体验园区'
            self.tax_item = '体验税目/试用体验税目'
            self.fk_creat_payload ="{\"company_name\":\"%s\",\"industry\":\"零售业\",\"communicate_at\":\"%s\",\"main_business\":\"测试数据\",\"customer_name\":\"测试数据\",\"website\":\"\",\"customer_identity\":\"测试数据\",\"taxpayer_type\":1,\"customer_mobile\":\"%s\",\"monthly_turnover\":\"13.00\",\"customer_email\":\"535163263623@qq.com\",\"door_header_comment\": \"\",\"has_door_header\":1,\"invoice_type\":2,\"associated_company\":\"\",\"voice_attachment\":[\"1510089287835684866\"],\"other_attachment\":[],\"rv_credit_rating_id\":\"1475752063345500160\",\"rv_tax_credit_rating_id\":\"1475752341276860416\",\"has_dispute_history\":0,\"voiceAttachment\":[],\"otherAttachment\":[],\"year_turnover\":\"156.00\",\"company_code\":\"%s\",\"organization_id\":\"1331113825351561217\",\"company_id\":\"1517347856669556738\",\"trade_info\":[{\"trade_id\":\"%s\",\"tax_item_id\":\"%s\",\"trade_remark\":\"测试数据测试数据测试数据测试数据\",\"email_delivery\":\"测试数据\",\"use_reason_one\":\"偶发性业务，不配置相关正式员工\",\"worker_from\":[\"自主寻找\"],\"last_tax_plan_one\":\"个人去税局代开发票\",\"matter_risk\":\"无\",\"work_at_one\":\"个人自行安排\",\"work_address_one\":\"个人自行安排\",\"work_tool_one\":\"个人自带\",\"is_follow_rule_one\":\"是\",\"contract_form_one\":\"劳动合同\",\"is_social_insurance\":1,\"need_people_monthly\":\"10人以下\",\"salary_form_one\":\"按件\",\"salary_form_remark\":\"测试数据测试数据测试数据测试数据测试数据\",\"person_monthly_salary\":\"小于1万\",\"total_monthly_salary\":\"0-10万\",\"canDelete\":true,\"verify_remark\":\"该场景在工作时间、地点上较为灵活，灵活用工人员按件计算方式获取相应酬劳，可自主决定是否为企业提供服务，且这批人员与客户企业不存在劳动合同关系，较符合灵活用工适用场景，建议引进\",\"matter_risk_remark\":\"\",\"new_delivery_info\":[{\"name\":\"1\",\"is_surpass_limit\":0,\"num\":1,\"remark\":\"\",\"star\":1}],\"delivery_info\":[],\"value_added_rate\":\"6\",\"lessData\":[],\"surpassData\":[],\"is_surpass_limit\":0,\"verify_status\":1,\"use_reason\":\"偶发性业务，不配置相关正式员工\",\"work_at\":\"个人自行安排\",\"work_address\":\"个人自行安排\",\"work_tool\":\"个人自带\",\"is_follow_rule\":\"是\",\"contract_form\":\"劳动合同\",\"salary_form\":\"按件\",\"last_tax_plan\":\"个人去税局代开发票\"}],\"notice_info\":[{\"content\":\"收款人必须为实际承接任务人员，不能出现代收款情况\",\"can_delete\":0},{\"content\":\"自由职业者单人单月酬劳发放不超过10万元\",\"can_delete\":0},{\"content\":\"客户公司的正式员工、法人、股东、董事监事及关联企业的正式员工不能作为客户企业的灵活用工人员，同时若有分支机构/关联企业也有灵活用工的需求，需要其以自己的名义重新在我们平台注册、认证、发布任务\",\"can_delete\":0},{\"content\":\"公职人员、军人不能作为灵活用工人员入驻众乐邦平台\",\"can_delete\":0},{\"content\":\"众乐邦平台会在灵活用工人员交付成果后，就业务真实性与服务商电话核实任务完成情况\",\"can_delete\":0}]}" % (company_name, current_time(), phone,self.company_code,self.tradeId,self.tax_item_id)
            print("当前为test环境")

        elif env_code == 2 :
            self.host_api_ustax = 'https://api.uat.ustax.com.cn'
            self.host_api = 'https://api.uat.zlbzb.cn'
            self.host_zlb_manage = 'http://manage.uat.zlbzb.cn'
            self.common_header["user-id"] = '1460429985512660994'
            self.tradeId = 188918816263110656
            self.tax_item_id = 188918289076846592
            self.parkId = 188915292234055680
            self.parkName = '体验园区'
            self.tax_item = '体验税目/试用体验税目'
            self.fk_creat_payload = "{\"company_name\":\"%s\",\"industry\":\"零售业\",\"communicate_at\":\"%s\",\"main_business\":\"测试数据\",\"customer_name\":\"测试数据\",\"website\":\"\",\"customer_identity\":\"测试数据\",\"taxpayer_type\":1,\"customer_mobile\":\"%s\",\"has_door_header\":1,\"invoice_type\":2,\"monthly_turnover\":\"13.00\",\"customer_email\":\"535163263623@qq.com\",\"associated_company\":\"\",\"voice_attachment\":[\"1510089287835684866\"],\"other_attachment\":[],\"rv_credit_rating_id\":\"1475752063345500160\",\"rv_tax_credit_rating_id\":\"1475752341276860416\",\"has_dispute_history\":0,\"voiceAttachment\":[],\"otherAttachment\":[],\"year_turnover\":\"156.00\",\"company_code\":\"91500000MA5U5MLK89\",\"organization_id\":\"1331113825351561217\",\"company_id\":\"1510088780800106497\",\"trade_info\":[{\"trade_id\":\"%s\",\"tax_item_id\":\"%s\",\"trade_remark\":\"测试数据测试数据测试数据测试数据\",\"email_delivery\":\"测试数据\",\"use_reason_one\":\"偶发性业务，不配置相关正式员工\",\"worker_from\":[\"自主寻找\"],\"last_tax_plan_one\":\"个人去税局代开发票\",\"matter_risk\":\"无\",\"work_at_one\":\"个人自行安排\",\"work_address_one\":\"个人自行安排\",\"work_tool_one\":\"个人自带\",\"is_follow_rule_one\":\"是\",\"contract_form_one\":\"劳动合同\",\"is_social_insurance\":1,\"need_people_monthly\":\"10人以下\",\"salary_form_one\":\"按件\",\"salary_form_remark\":\"测试数据测试数据测试数据测试数据测试数据\",\"person_monthly_salary\":\"小于1万\",\"total_monthly_salary\":\"0-10万\",\"canDelete\":true,\"verify_remark\":\"该场景在工作时间、地点上较为灵活，灵活用工人员按件计算方式获取相应酬劳，可自主决定是否为企业提供服务，且这批人员与客户企业不存在劳动合同关系，较符合灵活用工适用场景，建议引进\",\"matter_risk_remark\":\"\",\"new_delivery_info\":[{\"name\":\"1\",\"is_surpass_limit\":0,\"num\":1,\"remark\":\"\",\"star\":1}],\"delivery_info\":[],\"value_added_rate\":\"6\",\"lessData\":[],\"surpassData\":[],\"is_surpass_limit\":0,\"verify_status\":1,\"use_reason\":\"偶发性业务，不配置相关正式员工\",\"work_at\":\"个人自行安排\",\"work_address\":\"个人自行安排\",\"work_tool\":\"个人自带\",\"is_follow_rule\":\"是\",\"contract_form\":\"劳动合同\",\"salary_form\":\"按件\",\"last_tax_plan\":\"个人去税局代开发票\"}],\"notice_info\":[{\"content\":\"收款人必须为实际承接任务人员，不能出现代收款情况\",\"can_delete\":0},{\"content\":\"自由职业者单人单月酬劳发放不超过10万元\",\"can_delete\":0},{\"content\":\"客户公司的正式员工、法人、股东、董事监事及关联企业的正式员工不能作为客户企业的灵活用工人员，同时若有分支机构/关联企业也有灵活用工的需求，需要其以自己的名义重新在我们平台注册、认证、发布任务\",\"can_delete\":0},{\"content\":\"公职人员、军人不能作为灵活用工人员入驻众乐邦平台\",\"can_delete\":0},{\"content\":\"众乐邦平台会在灵活用工人员交付成果后，就业务真实性与服务商电话核实任务完成情况\",\"can_delete\":0}]}" % (company_name, current_time(), phone,self.tradeId,self.tax_item_id)
            print("当前为UAT环境")

        elif env_code == 3 :
            self.host_api_ustax = 'https://api.uat.ustax.com.cn'
            self.host_zlb_manage = 'http://manage.pre.zlbzb.cn'
            print("当前为PRE环境")
        else:
            print('输入环境参数有误，请按以下关系输入：1-test,2-UAT,3-PRE')
        self.session_bm = requests.session()


    def login(self):
        """
        登录
        :return:
        """
        url = self.host_api_ustax + "/auth/login"
        pwd_encoded = hashlib.md5(self.password.encode(encoding='utf-8')).hexdigest()
        payload = "{\"loginType\":1,\"platformNo\":1,\"clientId\":\"resico\",\"clientSecret\":\"resico888\",\"username\":\"%s\",\"password\":\"%s\"}" % (
            self.username, pwd_encoded)
        resp_raw = self.session_bm.post(url, data=payload)
        resp = json.loads(resp_raw.text)
        # 设置请求头
        self.common_header["authorization"] = "Bearer"+resp["data"]["accessToken"]
        print('登录结果：', (resp.get("succeed") is True))

    def send_code(self):
        """
        发送验证码
        :return:
        """
        url = self.host_api +  "/fe/validate/sendCode?phone=%s&type=1"%(self.phone)
        resp_raw = self.session_bm.get(url)
        resp = json.loads(resp_raw.text)
        print('发送验证码结果：', (resp.get("succeed") is True))

    def register(self):
        """
        注册账号
        :return:
        """
        url = self.host_api +  "/fe/user/register"
        payload = "{\"type\":2,\"password\":123456,\"mobile\":\"%s\",\"invitationCode\":\"\",\"verificationCode\":\"999999\",\"isChild\":false,\"thirdPartyAccountId\":\"\"}" % (
            self.phone)
        payload_json = json.loads(payload)
        resp_raw = self.session_bm.post(url,headers=self.common_header,data=payload)
        resp = json.loads(resp_raw.text)
        print(resp)
        print(payload)
        print(self.common_header)
        print('注册结果：', (resp.get("succeed") is True))

    def create_coorparate(self):
        """
        创建合作客户
        :return:
        """
        url = self.host_api_ustax + "/marketing/crm/cooperated/save"
        payload = "{\"province\":\"110000\",\"city\":\"110100\",\"area\":\"110101\",\"contacts\":[],\"customerId\":null,\"customerName\":\"%s\",\"phones\":[{\"phone\":\"%s\",\"source\":2}],\"type\":1,\"industryCode\":\"INS2020090300022\",\"district\":[\"110000\",\"110100\",\"110101\"],\"address\":\"输入框-详细地址\",\"source\":5,\"enterpriseType\":\"\",\"legalPerson\":\"\",\"website\":\"\",\"registeredDate\":\"\",\"registeredCapital\":\"\",\"contributedCapital\":\"\",\"staffSize\":\"\",\"remark\":\"\"}" % (
            self.company_name, self.phone)
        # headers = self.create_headers({
        #     'authorization': bg_token,
        # })
        resp = json.loads(self.session_bm.post(url, headers=self.common_header, data=payload.encode("utf-8")).text)
        print("创建合作客户：")
        logging.info("创建合作客户参数:" + payload)
        if resp.get("code") == 10000 and not resp.get("data"):
            return True
        else:
            return False

    def fkdy_bm(self):
        """
        后台发起风控调研
        large_to_15:是否大于15万
        :return:
        """
        url = self.host_zlb_manage + "/api/zlb/riskControl/create"

        payload = self.fk_creat_payload


        resp = json.loads(self.session_bm.post(url, headers=self.common_header, data=payload.encode("utf-8")).text)
        logging.info("发起风控调研参数:" + payload)
        print("发起风控调研结果：", resp.get('msg'))

    def __get_verify_list(self):
        """
        通过企业名称获取企业审核id
        :param compny_name:
        :return:
        """
        url = self.host_zlb_manage + "/api/zlb/riskControl/verifyList"

        payload = "{\"keywords\":\"%s\",\"current\":1,\"size\":20}" % self.company_name
        print(payload)
        resp_raw = self.session_bm.post(url, headers=self.common_header, data=payload.encode("utf-8"))
        resp = json.loads(resp_raw.text)
        print(resp)
        return resp.get("data").get("records")[0].get("id")

    def fkdy_first_confirm(self):
        """
        风控调研审批
        :return:
        """
        # 初审
        self.verify_id =self.__get_verify_list()
        url = self.host_zlb_manage + "/api/zlb/riskControl/verify"
        payload = ("{\"company_name\":\"%s\","
                   "\"industry\":\"零售业\","
                   "\"communicate_at\":\"%s\","
                   "\"main_business\":\"零售业\","
                   "\"customer_name\":\"小邦邦\","
                   "\"website\":null,"
                   "\"customer_identity\":\"总经理\","
                   "\"has_door_header\":1,"
                   "\"taxpayer_type\":1,"
                   "\"customer_mobile\":\"13666666670\","
                   "\"monthly_turnover\":10,"
                   "\"customer_email\":\"123@qq.com\","
                   "\"invoice_type\":2,"
                   "\"associated_company\":\"\","
                   "\"voice_attachment\":[\"1559734127964123137\"],"
                   "\"other_attachment\":[],"
                   "\"rv_credit_rating_id\":\"1468493923205914624\","
                   "\"rv_tax_credit_rating_id\":\"1470934708497031168\","
                   "\"has_dispute_history\":0,"
                   "\"otherAttachment\":[],"
                   " \"id\":\"%s\","
                   "\"company_code\":\"91500000MA5U5MLK89\","
                   "\"industry_code_list\":null,"
                   "\"organization_id\":\"1331113825351561217\","
                   "\"status\":{\"label\":\"待初审\","
                   "\"value\":1},"
                   "\"current_audit_id\":{\"label\":\"初审\","
                   "\"value\":\"33\"},"
                   "\"created_at\":\"%s\","
                   "\"updated_at\":\"%s\","
                   "\"created_by\":{\"label\":\"销售二号\","
                   "\"value\":\"1414422761330896897\"},"
                   "\"refuse_reason\":null,"
                   "\"re_communicate_at\":null,"
                   "\"source\":{\"label\":\"APP\","
                   "\"value\":1},"
                   " \"company_id\":\"%s\","
                   "\"year_turnover\":120,"
                   "\"rv_credit_rating\":\"A\","
                   "\"rv_tax_credit_rating\":\"A\","
                   "\"have_temporary\":false,"
                   "\"sendEmailType\":1,"
                   "\"company_risk_tag\":null,"
                   "\"trade_info\":[{\"trade_id\":\"%s\","
                   "\"tax_item_id\":\"%s\","
                   "\"trade_remark\":\"分角色分手快乐成魔喜喜\","
                   "\"email_delivery\":\"感受感受\","
                   "\"use_reason_one\":\"季节性业务，忙时需灵活人员协助\","
                   "\"worker_from\":[\"招聘\"],"
                   "\"is_need_credentials\":0,"
                   "\"last_tax_plan_one\":\"个人去税局代开发票\","
                   "\"matter_risk\":\"无\","
                   "\"work_at_one\":\"个人自行安排\","
                   "\"work_address_one\":\"个人自行安排\","
                   "\"work_tool_one\":\"个人自带\","
                   "\"is_follow_rule_one\":\"是\","
                   "\"contract_form_one\":\"无合同\","
                   "\"is_social_insurance\":1,"
                   "\"need_people_monthly\":\"10人以下\","
                   "\"salary_form_one\":\"按件\","
                   "\"salary_form_remark\":\"咯来咯哦哦谢谢Hhhhhhhbb\","
                   "\"person_monthly_salary\":\"小于1万\","
                   "\"total_monthly_salary\":\"0-10万\","
                   "\"remark\":null,"
                   "\"risk_trade_id\":\"188918816263110656\","
                   "\"use_reason\":\"季节性业务，忙时需灵活人员协助\","
                   "\"delivery_info\":\"测试6\","
                   "\"work_at\":\"个人自行安排\","
                   "\"work_address\":\"个人自行安排\","
                   "\"work_tool\":\"个人自带\","
                   "\"is_follow_rule\":\"是\","
                   "\"contract_form\":\"无合同\","
                   "\"salary_form\":\"按件\","
                   "\"last_tax_plan\":\"个人去税局代开发票\","
                   "\"verify_status\":1,"
                   "\"verify_remark\":\"该场景在工作时间、地点上较为灵活，灵活用工人员按件计算方式获取相应酬劳，可自主决定是否为企业提供服务，且这批人员与客户企业不存在劳动合同关系，较符合灵活用工适用场景，建议引进\", "
                   "\"created_at\":\"%s\","
                   "\"updated_at\":\"%s\","
                   "\"park_name\":null,"
                   "\"value_added_rate\":\"6\","
                   "\"is_surpass_limit\":0,"
                   "\"new_delivery_info\":[{\"name\":\"测试6\","
                   "\"is_surpass_limit\":0,"
                   "\"num\":1,"
                   "\"remark\":\"\","
                   "\"star\":5}],"
                   "\"surpassData\":[],"
                   "\"lessData\":[{\"delivery\":[\"测试6\"],"
                   "\"remark\":\"\"}],"
                   "\"matter_risk_remark\":\"\"}],"
                   "\"notice_info\":[{\"content\": \"自知则知之做做做做做做做做做做做做做做做做做做做做做做做做做做做\",\"can_delete\": 1}]}"
                   %(self.company_name,current_time(),self.verify_id,current_time(),current_time(),self.verify_id,self.tradeId,self.tax_item_id,current_time(),current_time()) )
        resp = json.loads(self.session_bm.post(url, headers=self.common_header, data=payload.encode("utf-8")).text)
        print("风控初审结果:", resp.get('msg'))
        logging.info("风控调研初审参数:" + payload)
    def fkdy_last_confirm(self):
        """
        风控调研审批
        :return:
        """
        # 复审
        url = self.host_zlb_manage + "/api/zlb/riskControl/verify"
        payload =("{\"company_name\":\"%s\","
                   "\"industry\":\"零售业\","
                   "\"communicate_at\":\"%s\","
                   "\"main_business\":\"零售业\","
                   "\"customer_name\":\"小邦邦\","
                   "\"website\":null,"
                   "\"customer_identity\":\"总经理\","
                   "\"has_door_header\":1,"
                   "\"taxpayer_type\":1,"
                   "\"customer_mobile\":\"13666666670\","
                   "\"monthly_turnover\":10,"
                   "\"customer_email\":\"123@qq.com\","
                   "\"invoice_type\":2,"
                   "\"associated_company\":\"\","
                   "\"voice_attachment\":[\"1559734127964123137\"],"
                   "\"other_attachment\":[],"
                   "\"rv_credit_rating_id\":\"1468493923205914624\","
                   "\"rv_tax_credit_rating_id\":\"1470934708497031168\","
                   "\"has_dispute_history\":0,"
                   "\"otherAttachment\":[],"
                   " \"id\":\"%s\","
                   "\"company_code\":\"91500000MA5U5MLK89\","
                   "\"industry_code_list\":null,"
                   "\"organization_id\":\"1331113825351561217\","
                   "\"status\":{\"label\":\"待复审\","
                   "\"value\":3},"
                   "\"current_audit_id\":{\"label\":\"复审\","
                   "\"value\":\"34\"},"
                   "\"created_at\":\"%s\","
                   "\"updated_at\":\"%s\","
                   "\"created_by\":{\"label\":\"销售二号\","
                   "\"value\":\"1414422761330896897\"},"
                   "\"refuse_reason\":null,"
                   "\"re_communicate_at\":null,"
                   "\"source\":{\"label\":\"APP\","
                   "\"value\":1},"
                   " \"company_id\":\"%s\","
                   "\"year_turnover\":120,"
                   "\"rv_credit_rating\":\"A\","
                   "\"rv_tax_credit_rating\":\"A\","
                   "\"have_temporary\":false,"
                   "\"sendEmailType\":1,"
                   "\"company_risk_tag\":null,"
                   "\"trade_info\":[{\"trade_id\":\"%s\","
                   "\"tax_item_id\":\"%s\","
                   "\"park_id\":\"%s\","
                   "\"trade_remark\":\"分角色分手快乐成魔喜喜\","
                   "\"email_delivery\":\"感受感受\","
                   "\"use_reason_one\":\"季节性业务，忙时需灵活人员协助\","
                   "\"worker_from\":[\"招聘\"],"
                   "\"is_need_credentials\":0,"
                   "\"last_tax_plan_one\":\"个人去税局代开发票\","
                   "\"matter_risk\":\"无\","
                   "\"work_at_one\":\"个人自行安排\","
                   "\"work_address_one\":\"个人自行安排\","
                   "\"work_tool_one\":\"个人自带\","
                   "\"is_follow_rule_one\":\"是\","
                   "\"contract_form_one\":\"无合同\","
                   "\"is_social_insurance\":1,"
                   "\"need_people_monthly\":\"10人以下\","
                   "\"salary_form_one\":\"按件\","
                   "\"salary_form_remark\":\"咯来咯哦哦谢谢Hhhhhhhbb\","
                   "\"person_monthly_salary\":\"小于1万\","
                   "\"total_monthly_salary\":\"0-10万\","
                   "\"remark\":null,"
                   "\"risk_trade_id\":\"188918816263110656\","
                   "\"use_reason\":\"季节性业务，忙时需灵活人员协助\","
                   "\"delivery_info\":\"测试6\","
                   "\"work_at\":\"个人自行安排\","
                   "\"work_address\":\"个人自行安排\","
                   "\"work_tool\":\"个人自带\","
                   "\"is_follow_rule\":\"是\","
                   "\"contract_form\":\"无合同\","
                   "\"salary_form\":\"按件\","
                   "\"last_tax_plan\":\"个人去税局代开发票\","
                   "\"verify_status\":1,"
                   "\"verify_remark\":\"该场景在工作时间、地点上较为灵活，灵活用工人员按件计算方式获取相应酬劳，可自主决定是否为企业提供服务，且这批人员与客户企业不存在劳动合同关系，较符合灵活用工适用场景，建议引进\", "
                   "\"created_at\":\"%s\","
                   "\"updated_at\":\"%s\","
                   "\"park_name\":null,"
                   "\"value_added_rate\":\"6\","
                   "\"is_surpass_limit\":0,"
                   "\"new_delivery_info\":[{\"name\":\"测试6\","
                   "\"is_surpass_limit\":0,"
                   "\"num\":1,"
                   "\"remark\":\"\","
                   "\"star\":5}],"
                   "\"surpassData\":[],"
                   "\"lessData\":[{\"delivery\":[\"测试6\"],"
                   "\"remark\":\"\"}],"
                   "\"matter_risk_remark\":\"\"}],"
                   "\"notice_info\":[{\"content\": \"自知则知之做做做做做做做做做做做做做做做做做做做做做做做做做做做\",\"can_delete\": 1}]}"
        %(self.company_name,current_time(),self.verify_id,current_time(),current_time(),self.verify_id,self.tradeId,self.tax_item_id,self.parkId,current_time(),current_time()))
        resp = json.loads(self.session_bm.post(url, headers=self.common_header, data=payload.encode("utf-8")).text)
        print("复审结果:", resp.get('msg'))
        logging.info("风控调研复审参数:" + payload)

    def addPersonVerifyConfig(self):
        '''
        配置认证方式
        :return:
        '''
        url = self.host_zlb_manage + "/api/zlb/riskControl/addPersonVerifyConfig"

        payload = ("{\"id\":\"%s\","
                   "\"electronSign\":true,"
                   "\"nonElectronSign\":false,"
                   "\"livingBody\":true,"
                   "\"operatorThreeElement\":true,"
                   "\"bankFourElement\":true,"
                   "\"cardTwoElement\":false,"
                   "\"cardPhoto\":true,"
                   "\"riskSettings\":[\"1435844277656756224\",\"1438067993908224000\",\"1438075815647649792\",\"1443044518181085184\",\"1468505757392707584\",\"1437291948791701504\",\"1468495858558443520\",\"1468521276401393664\",\"1468885944273870848\",\"1471429032573804544\",\"1472762861737615360\",\"1474003475267461120\",\"1474206805000331264\",\"1437601274366402560\",\"1468521483834892288\",\"1468521736365547520\",\"1437691114143490048\",\"1470347357181845504\",\"1471669408060547072\",\"1437691114143490049\",\"1474283640656633856\",\"1474288163919896576\","
                   "\"1437604212287610880\"]}")%(self.verify_id)

        resp = json.loads(self.session_bm.post(url, headers=self.common_header, data=payload.encode("utf-8")).text)
        logging.info("配置认证方式参数:" + payload)
        print("配置认证方式结果：", resp.get('msg'))

    def official_deal(self):
        '''
        线下处理风控邮件
        :return:
        '''
        url = self.host_zlb_manage + "/api/zlb/riskControl/offlineDeal"

        payload = "{\"id\": \"%s\"}"%(self.verify_id)

        resp = json.loads(self.session_bm.post(url, headers=self.common_header, data=payload.encode("utf-8")).text)
        logging.info("线下处理风控邮件参数:" + payload)
        print("线下处理风控邮件结果：", resp.get('msg'))
    def zlb_cooperate(self):
        '''
        完成众乐邦合作流程
        :param company_name:
        :return:
        '''
        url =  self.host_zlb_manage + "/api/app/riskControl/encrypt"
        payload = json.dumps({
            "data": {
                "companyName": self.company_name,
                "turnover": "5",
                "createdBy": "1460429985512660994",
                "createdByName": "zlb_robot",
                "details": [
                    {
                        "tradeId": "%s"%(self.tradeId),
                        "taxRate": 6,
                        "personScale": "0.00",
                        "companyScale": "10.00",
                        "gtPersonScale": "0.00",
                        "gtCompanyScale": "20.00"
                    }
                ]
            }
        })
        request_raw = self.session_bm.post(url, headers=self.common_header, data=payload.encode("utf-8")).text
        url =  self.host_zlb_manage + "/api/zlb/contract/newContractNotice"
        payload = json.dumps({ "data": request_raw})
        resp_raw = self.session_bm.post(url, headers=self.common_header, data=payload.encode("utf-8")).text
        resp = json.loads(resp_raw)
        print("众乐邦合作流程结果：", resp.get('msg'))
    def teardown(self):
        self.session_bm.close()

class Db_oprate(object):
    def __init__(self,env_code,phone,company_name):

        # 数据库配置
        if env_code == 1:
            self.config = {
                "host": '192.168.100.43',
                "user": "root",
                "password": 'Resico@2020#dev',
                "database": 'zlb'
                }
            # 场景为6-9-11-13的一级场景->6%不超15万场景
            self.tradeId = 33
            # 发布API任务时税目为：6-9-11-13的一级税目/二级-6%的税目
            self.tax_item_id = 31
            self.parkId = 4
            self.parkName = '永州园区'
            self.tax_item = '纳税申报代理/纳税申报代理'
            print("当前数据库为test环境")
        elif env_code == 2:
            self.config = {
                "host": 'rm-8vb749uw21dl46h8n7o.mysql.zhangbei.rds.aliyuncs.com',
                "user": "zlb_uat",
                "password": 'Zlb@uat2022',
                "database": 'zlb_uat'
            }
            self.tradeId = 188918816263110656
            self.tax_item_id = 188918289076846592
            self.parkId = 188915292234055680
            self.parkName = '体验园区'
            self.tax_item = '体验税目/试用体验税目'
            print("当前数据库为UAT环境")
        elif env_code == 3:
            self.config = {
                "host": 'rm-8vb749uw21dl46h8n.mysql.zhangbei.rds.aliyuncs.com',
                "user": "zlb_pre",
                "password": 'Zlb@pre2022',
                "database": 'zlb_pre'
            }
            print("当前数据库为PRE环境")
        else:
            print('输入环境参数有误，请按以下关系输入：1-test,2-UAT,3-PRE')
        self.phone = phone
        self.company_name = company_name
        self.__init_db()

    def __init_db(self):
        """
        初始化数据库连接
        :return:
        """
        self.db = pymysql.connect(**self.config)
        self.cursor = self.db.cursor()

    def release_db(self):
        """
        释放数据库连接
        :return:
        """
        self.cursor.close()
        self.db.close()

    def update_data(self):
        """
        插入企业数据
        :param company_name:
        :return:
        """
        self.__init_db()
        #根据手机号查询uid
        query_sql = "select id from zlb_users where mobile ='{}';".format(self.phone)
        self.cursor.execute(query_sql)
        self.uid = self.cursor.fetchone()[0]
        #生成一个company_id
        query_sql = "select id from zlb_company order by id desc limit 1"
        self.cursor.execute(query_sql)
        self.company_id = self.cursor.fetchone()[0]
        self.company_id = self.company_id + 1

        #插入company表数据
        insert_sql = "INSERT INTO `zlb_company`(`id`,`uid`, `pay_mode`, `company_name`, `company_origin_name`, `company_code`, `business_license`, `province`, `city`, `area`, `address`, `status`, `reason`, `verify_step`, `remark`, `is_show_task`, `auth_at`, `confirm_at`, `created_at`, `updated_at`, `created_by`, `updated_by`, `delete_flag`, `version`, `is_show_api_task`, `api_can_from_platform`, `isOpenPlatformUser`, `can_view_info`, `person_pay_way`, `person_verify_config`, `early_warning`, `balance_msg_switch`, `warn_balance`, `send_msg_num`, `warn_mobiles`, `check_bank_name`, `limit_min_age`, `limit_max_age`, `is_send_msg_for_balance_not_enough`, `is_send_msg_for_platform_pay_success`, `quality_check_at`, `industry`) VALUES ({},{}, 0, '{}', '{}', '91440300192317458F', 1528906723485650946, NULL, NULL, NULL, NULL, 1, '', 1, NULL, 0, '{}', NULL, '{}', '2022-09-22 09:42:02', NULL, NULL, 0, NULL, 0, 0, 1, 0, 4, 118, NULL, 0, 0.00, 0, NULL, 0, 16, 0, 1, 1, '2022-09-22 01:00:44', '电气机械和器材制造业');".format(self.company_id,self.uid,self.company_name,self.company_name,current_time(),current_time())
        self.cursor.execute(insert_sql)

        #插入company_detail表
        insert_sql = "INSERT INTO `zlb_company_detail`(`uid`, `company_id`, `admin_name`, `admin_card_number`, `admin_mobile`, `legal_name`, `legal_card_number`, `bank_name`, `bank_card_number`, `bank_detail_name`, `card_front_img`, `card_back_img`, `validation_img`, `created_at`, `created_by`, `updated_at`, `updated_by`, `version`, `delete_flag`) VALUES ({}, {}, '陈熠', '500231199610232058', '18711111111', '陈熠', '500231199610232058', NULL, NULL, NULL, 1528906725788323841, 1528906728665616385, 1528906730506915842, '{}', NULL, '{}', NULL, NULL, 0);".format(self.uid,self.company_id,current_time(),current_time())
        self.cursor.execute(insert_sql)

        # 生成一个company_task_relation_id
        query_sql = "select id from zlb_company_task_relation order by id desc limit 1"
        self.cursor.execute(query_sql)
        self.company_task_relation_id = self.cursor.fetchone()[0]
        self.company_task_relation_id = self.company_task_relation_id + 1

        #插入company_task_relation数据
        insert_sql = "INSERT INTO `zlb_company_task_relation`(`id`,`uid`, `trade_id`, `park_id`, `enable_large_tax_rate`, `is_enable`, `tax_item_id`, `value_added_rate`, `created_at`, `updated_at`, `created_by`, `updated_by`, `delete_flag`, `version`, `is_user_control`) VALUES ({},{}, {}, {}, 1, 1, 188918289076846592, 6, '2022-09-22 09:42:02', '2022-09-22 09:42:02', NULL, NULL, 0, NULL, 1);".format(self.company_task_relation_id,self.uid,self.tradeId,self.parkId)
        self.cursor.execute(insert_sql)


        #插入protocol数据
        insert_sql = "INSERT INTO `zlb_protocol_company`(`no`, `protocol_template_id`, `name`, `uid`, `main_entity`, `first_party`, `second_party`, `status`, `contract_id`, `trans_id`, `contract_url`, `contract_down_url`, `jump_url`, `contract_file_id`, `remark`, `sign_at`, `created_at`, `created_by`, `updated_at`, `updated_by`, `delete_flag`, `version`) VALUES ('CL0000642', 22, '众乐邦承揽协议', {}, '海南众乐邦网络科技有限公司', '{}', '{}', 2, 'f01838fc24e769d0b6f3ceccee466446', '1147d984495c69284210a46ffd533b1d', 'https://testapi.fadada.com:8443/api/viewContract.action?app_id=403472&v=2.0&timestamp=20220524091738&contract_id=f01838fc24e769d0b6f3ceccee466446&msg_digest=OTU4OTA1NzgyRTYzNUMzMkMwOEZGQkY5NDYxRkI5NTQ0QTAzQjZFNQ==', 'https://testapi.fadada.com:8443/api/downLoadContract.action?app_id=403472&v=2.0&timestamp=20220524091738&contract_id=f01838fc24e769d0b6f3ceccee466446&msg_digest=OTU4OTA1NzgyRTYzNUMzMkMwOEZGQkY5NDYxRkI5NTQ0QTAzQjZFNQ==', 'https://testapi25.fadada.com/api/extsign.api?app_id=403472&v=2.0&timestamp=20220524091739&transaction_id=1147d984495c69284210a46ffd533b1d&customer_id=C9B749535E0454DAEB1E9CCA8D836291&contract_id=f01838fc24e769d0b6f3ceccee466446&doc_title=%E7%94%A8%E5%B7%A5%E4%BC%81%E4%B8%9A%E6%9C%8D%E5%8A%A1%E5%8D%8F%E8%AE%AE&keyword_strategy=0&return_url=https%3A%2F%2Fpc.uat.zlbzb.cn%2F%23%2Fself%2FtaskManage%2Fpublish&notify_url=http%3A%2F%2Fapi.uat.zlbzb.cn%2Ffe%2Ffdd_callback%2Fcontract&msg_digest=OERCQUNGRjZFQjk0NUNBNjhCRTM3RjVFNTVDNjNDNkFCRUQ1RjlCQw==', NULL, NULL, '2022-05-24 09:17:59', '2022-05-24 09:17:39', 1528904965950640129, '2022-05-24 09:17:39', 1528904965950640129, 0, NULL);".format(self.uid,self.company_name,self.company_name)
        self.cursor.execute(insert_sql)
        # 查询protocol_company_id
        query_sql = "select id from zlb_protocol_company where uid ='{}';".format(self.uid)
        self.cursor.execute(query_sql)
        self.protocol_company_id = self.cursor.fetchone()[0]

        #查询一个可以用的平安银行账号
        query_sql = "SELECT bank_account_no FROM `zlb_bank_account` WHERE `park_id` = '{}' AND `status` = '0' limit 1;".format(self.parkId)
        self.cursor.execute(query_sql)
        self.bank_account_no = self.cursor.fetchone()[0]
        #将卡号更新为已使用
        update_sql = "UPDATE zlb_bank_account SET status=1 WHERE bank_account_no = '{}';".format(self.bank_account_no)
        self.cursor.execute(update_sql)
        #插入company_bank_account数据
        insert_sql = "INSERT INTO `zlb_company_bank_account`(`uid`, `no`, `union_no`, `account_no`, `account_name`, `account_deposit`, `account_type`, `park_id`, `balance`, `occupied_balance`, `frozen_balance`, `sort`, `warn_time`, `balance_msg_switch`, `warn_mobiles`, `warn_balance`, `warn_amt`, `created_at`, `updated_at`, `created_by`, `updated_by`, `delete_flag`, `version`, `subsidy_amt`, `status`) VALUES ({}, 1, NULL, '{}', '体验园区有限公司', '平安银行重庆两江支行', 1, {}, 1000000000.0000, 0.0000, 0.0000, 1, NULL, 0, NULL, NULL, NULL, '2022-09-21 10:57:55', '2022-09-21 10:57:55', 1319636526790897912, 1319636526790897912, 0, NULL, 0.0000, 1);".format(self.uid,self.bank_account_no,self.parkId)
        self.cursor.execute(insert_sql)

        # 生成一个zlb_company_task_relation_delivery_id
        query_sql = "select id from zlb_company_task_relation_delivery order by id desc limit 1"
        self.cursor.execute(query_sql)
        self.zlb_company_task_relation_delivery_id = self.cursor.fetchone()[0]
        self.zlb_company_task_relation_delivery_id = self.company_task_relation_id + 1


        #插入company_task_relation_delivery数据
        insert_sql = "INSERT INTO `zlb_company_task_relation_delivery`(`id`,`company_task_relation_id`, `delivery_name`, `star`, `is_surpass_limit`, `num`, `remark`, `created_at`, `updated_at`, `delete_flag`, `version`) VALUES ({},{}, '保洁服务', 3, 0, 33, NULL, NULL, NULL, 0, NULL);".format(self.zlb_company_task_relation_delivery_id, self.company_task_relation_id)
        self.cursor.execute(insert_sql)

        #插入protocol_company_supply数据
        insert_sql = "INSERT INTO `zlb_protocol_company_supply`(`protocol_company_id`, `no`, `name`, `uid`, `main_entity`, `first_party`, `second_party`, `status`, `effective_status`, `remark`, `source`, `reject_reason`, `failure_reason`, `turnover`, `content`, `sign_at`, `created_at`, `created_by`, `created_name`, `updated_at`, `updated_by`, `delete_flag`, `version`) VALUES ({}, 'BC0000355', '补充协议', {}, '海南众乐邦网络科技有限公司', '{}', '海南众乐邦网络科技有限公司', 4, 2, NULL, 2, NULL, NULL, 11111000000.0000, '<html><head></html>', '2022-05-24 09:18:07', '2022-05-24 09:17:22', 1528547743227428866, '陈熠', '2022-05-24 09:18:07', 0, 0, NULL);".format(self.protocol_company_id,self.uid,self.company_name)
        self.cursor.execute(insert_sql)
        #获取protocol_company_supply_id
        query_sql = "select id from zlb_protocol_company_supply where protocol_company_id ='{}';".format(self.protocol_company_id)
        self.cursor.execute(query_sql)
        self.protocol_company_supply_id = self.cursor.fetchone()[0]

        #插入zlb_protocol_custom_tax数据
        insert_sql = "INSERT INTO `zlb_uat`.`zlb_protocol_custom_tax`(`protocol_company_supply_id`, `item_tax_rate`, `first_limit_amt`, `first_limit_type`, `company_tax_rate`, `person_tax_rate`, `delete_flag`, `created_by`, `created_at`, `updated_by`, `updated_at`, `version`) VALUES ( {}, 6.0000, 15000000.0000, 0, 10.0000, 0.0000, 0, 1460429985512660994, '2022-09-07 13:42:06', 1460429985512660994, '2022-09-07 13:42:06', NULL);".format(self.protocol_company_supply_id)
        self.cursor.execute(insert_sql)
        insert_sql = "INSERT INTO `zlb_uat`.`zlb_protocol_custom_tax`(`protocol_company_supply_id`, `item_tax_rate`, `first_limit_amt`, `first_limit_type`, `company_tax_rate`, `person_tax_rate`, `delete_flag`, `created_by`, `created_at`, `updated_by`, `updated_at`, `version`) VALUES ({}, 6.0000, 15000000.0000, 1, 12.0000, 0.0000, 0, 1460429985512660994, '2022-09-07 13:42:06', 1460429985512660994, '2022-09-07 13:42:06', NULL);".format(self.protocol_company_supply_id)
        self.cursor.execute(insert_sql)


        #更新users表认证状态和时间
        update_sql = "UPDATE `zlb_users` set `isverify`=1 WHERE `id` ={}".format(self.uid)
        self.cursor.execute(update_sql)
        update_sql = "UPDATE `zlb_users` set `verify_at`= '{}' WHERE `id` ={}".format(current_time(), self.uid)
        self.cursor.execute(update_sql)

        #插入associate_users数据
        insert_sql = "INSERT INTO `zlb_associated_users`(`uid`, `associated_uid`, `created_at`, `updated_at`, `created_by`, `updated_by`, `version`, `delete_flag`, `company_name`) VALUES ({}, {}, '{}', '{}', 1572144332780720129, 1572144332780720129, NULL, 0, '{}');;".format(
            self.uid, self.uid, current_time(), current_time(),self.company_name)
        self.cursor.execute(insert_sql)

        # 插入发票管理信息
        insert_sql = "INSERT INTO `zlb_invoice_recipient_info`(`uid`, `real_name`, `tel_phone`, `invoice_send_type`, `province`, `city`, `area`, `address`, `com_email_address`, `note`, `created_at`, `updated_at`, `created_by`, `updated_by`, `delete_flag`, `version`) VALUES ( '{}', '马三', '18752648924', 1, '上海', '上海市', '徐汇区', '观音桥步行街融恒时代广场', '115039852@qq.com', null, '{}', '{}', 1759, 1759, 0, null );".format(self.uid,current_time(),current_time())
        self.cursor.execute(insert_sql)
        #插入发票抬头信息
        insert_sql = "INSERT INTO `zlb_invoice_title_info`(`uid`, `type`, `company_name`, `company_code`, `com_address`, `com_telphone`, `com_bank_name`, `com_bank_card`, `com_email_address`, `invoice_cate`, `invoice_content`, `created_at`, `updated_at`, `created_by`, `updated_by`, `delete_flag`, `version`) VALUES ({}, '1', '{}', '91500112MA60C7LG76', '重庆市渝北区啦啦啦啦啦啦', '9898989', '18220020000', '18220020001', 'ztx619944895@126.com', '体验税目', '试用体验税目', '{}', '{}', 1765, 1765, 0, NULL);".format(self.uid,self.company_name,current_time(),current_time())
        self.cursor.execute(insert_sql)




        self.cursor.connection.commit()
if __name__ == '__main__':
    # 税务销售顾问(众乐邦后台账号)
    # username = '18502338744'
    # password = "zlb123456"

    username = '18502338722'
    password = "cy123456"

    # 合作客户及手机号码,对接方提供
    # 社会信用代码法大大测试环境只校验存在的，暂时写死
    phone = generate_mobile()
    # phone = 18757108898
    # company_name ='婷婷市华成育卓网络有限公司'
    company_name = generate_company_name()
    company_code = '923501222550247843'
    # 环境配置：1 - test, 2 - UAT, 3 - PRE
    env_code = 1
    # # ==========================================================
    bm = BackManager(username, password,env_code,company_name,phone)
    # 1、生成合作客户
    # 1.1 环境配置：1-test,2-UAT,3-PRE
    # 1.2 后台登录获取auth

    # bm.send_code()
    # bm.register()


    bm.login()

    # 1.3 创建一个合作客户
    create_coorparate_result = bm.create_coorparate()
    logging.info("生成企业信息:"+company_name)
    # 2、风控调研
    # 2.1 风控调研发起
    bm.fkdy_bm()
    # 2.2 风控调研初审(后台发起的风控调研仅需要复审)
    # 暂时写死的数据：
    # 场景：体验场景>试用体验场景
    # 场景id：188918816263110656
    # 税目：体验税目>试用体验税目
    # 税率：6%

    bm.fkdy_first_confirm()
    bm.fkdy_last_confirm()
    bm.addPersonVerifyConfig()
    bm.official_deal()


    # 3、众乐邦合作
    bm.zlb_cooperate()

    bm.teardown()

    #4、初始化企业数据
    # db = Db_oprate(env_code,phone,company_name)
    # 数据库环境配置：1-test,2-UAT,3-PRE
    # db.update_data()
    # db.release_db()

    print('==' * 10)
    print("生成API企业成功:{},回复对接方信息内容：".format(phone))
    print("company_name: '%s'，""企业认证的时候营业执照图片可以随便传，测试环境不校验。企业名称手动修改为'%s',""社会信用代码:'%s',""法人姓名输入实名认证的法人姓名，发布API任务场景id:%s,发布任务税目：%s"%(company_name,company_name,company_code,bm.tradeId,bm.tax_item))
    print('==' * 10)


