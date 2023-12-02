import pprint
import threading
import time

import urllib3
import requests
import json
from datetime import datetime



urllib3.disable_warnings()

class Function:



    def __init__(self, window=None):

        self.s = requests.Session()

        self.headers = {
            'Host': 'jy.yectc.com:16952',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded;',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        self.window = window

        self.pause = False

        self.e = threading.Event()
        self.start = False


    def stop_check(self):
        self.pause = True
        self.start = False
        self.e.set()


    def login(self,user='YLBYNYKJ',passwd='147258369'):

        url = "https://jy.yectc.com:16952/frontService/customer/login/loginByPwd"

        payload = f"username={user}&password={passwd}&loginTerminal=1"

        try:
            response = self.s.post(url, headers=self.headers, data=payload, verify=False, timeout=5)
        except:
            self.window.write_event_value('message1','登录超时，请重试')
            return

        resp = json.loads(response.text)

        if 'code' in resp.keys():

            try:
                self.window.write_event_value('message1',resp['msg'])
            except:
                pass

        else:
            self.userId = resp['userId']
            self.token = resp['token']

            self.headers['UserID'] = self.userId
            self.headers['Token'] = self.token
            try:
                self.window.write_event_value('message','登陆成功')
            except:
                pass

            with open('./user.json', 'w', encoding='utf-8') as file:
                json.dump({'user':user, 'passwd':passwd}, file,ensure_ascii=False)
                file.close()

            self.check_scedule()


    def check_bid(self, plateId, tradeModeID,tradeTimeId):

        self.tradeModeId = tradeModeID
        self.tradeTimeId = tradeTimeId

        url = f"https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/plate/matter/list?plateId={plateId}"

        try:
            response = self.s.get(url, headers=self.headers,verify=False, timeout=10)
        except:
            return

        resp = json.loads(response.text)

        # resp = {'plateVo': {'plateId': 95, 'plateName': '公开竞价（润邦矿业）', 'status': 2, 'startTime': '08:30:00', 'startTimeProcess': '2023-08-31 08:30:00', 'endTime': '2023-09-01 00:39:30', 'tradeModeId': 1, 'companyId': None, 'companyName': '润邦矿业', 'buyOrSell': 1, 'isShareMargin': 1, 'eachMargin': None, 'startWay': None, 'maxMatterCount': None, 'filterNumber': 0, 'maxCount': 1, 'createTime': None, 'modifyTime': None, 'tradeStyle': '2', 'sectionId': 1, 'sortProcessID': 0, 'breedNameType': 0}, 'matterGroupList': [{'matterGroupNo': 'DMGN', 'tradeModeId': 1, 'matterList': [{'matterId': 51009, 'matterCode': 'RB23080059', 'matterGroupNo': 'RB23080059', 'tradeModeId': 1, 'plateId': None, 'plateName': None, 'status': 1, 'breedId': None, 'quantityPrecision': 2, 'pricePrecision': 2, 'breedName': '块煤', 'commodityId': 20882, 'name': '中块', 'companyName': None, 'quantity': 2000.0, 'bestPrice': 0.0, 'bestQuantity': 2000.0, 'unit': '吨', 'buyOrSell': None, 'isQuantityShowApprox': 1, 'breedTradeWay': None, 'beginPrice': 740.0, 'alertPrice': 1500.0, 'curPrice': 0.0, 'cureShares': None, 'curSection': None, 'totalSecion': None, 'factor': None, 'allQuantity': None, 'hadFilterCount': 0, 'deliveryUnit': None, 'stationRoadId': '67', 'orderQuantity': 0.0, 'tradeTimeId': None, 'sectionId': 1, 'minOrderQuantity': None, 'minMoveQuantity': None, 'startTime': '08:30', 'planStartTime': None, 'deliveryStartDate': '2023-08-31', 'createTime': None, 'reportedQuantity': 0.0, 'enableFactor': 0, 'myFlag': False}]}], 'matterList': [{'matterId': 51009, 'matterCode': 'RB23080059', 'matterGroupNo': 'RB23080059', 'tradeModeId': 1, 'plateId': None, 'plateName': None, 'status': 1, 'breedId': None, 'quantityPrecision': 2, 'pricePrecision': 2, 'breedName': '块煤', 'commodityId': 20882, 'name': '中块', 'companyName': None, 'quantity': 2000.0, 'bestPrice': 0.0, 'bestQuantity': 2000.0, 'unit': '吨', 'buyOrSell': None, 'isQuantityShowApprox': 1, 'breedTradeWay': None, 'beginPrice': 740.0, 'alertPrice': 1500.0, 'curPrice': 0.0, 'cureShares': None, 'curSection': None, 'totalSecion': None, 'factor': None, 'allQuantity': None, 'hadFilterCount': 0, 'deliveryUnit': None, 'stationRoadId': '67', 'orderQuantity': 0.0, 'tradeTimeId': None, 'sectionId': 1, 'minOrderQuantity': None, 'minMoveQuantity': None, 'startTime': '08:30', 'planStartTime': None, 'deliveryStartDate': '2023-08-31', 'createTime': None, 'reportedQuantity': 0.0, 'enableFactor': 0, 'myFlag': False}], 'drawShowOrderQty': True}
        """{
	"plateVo": {
		"plateId": 95,
		"plateName": "公开竞价（润邦矿业）",
		"status": 3,
		"startTime": "08:24:00",
		"startTimeProcess": "2023-12-02 08:24:00",
		"endTime": "2023-12-02 08:26:00",
		"tradeModeId": 1,
		"companyId": null,
		"companyName": "润邦矿业",
		"buyOrSell": 1,
		"isShareMargin": 1,
		"eachMargin": null,
		"startWay": null,
		"maxMatterCount": null,
		"filterNumber": 0,
		"maxCount": 25,
		"createTime": null,
		"modifyTime": null,
		"tradeStyle": "2",
		"sectionId": 8,
		"sortProcessID": 0,
		"breedNameType": 0
	},
	"matterGroupList": [{
		"matterGroupNo": "DMGN",
		"tradeModeId": 1,
		"matterList": [{
			"matterId": 62683,
			"matterCode": "RB23120036",
			"matterGroupNo": "RB23120036",
			"tradeModeId": 1,
			"plateId": null,
			"plateName": null,
			"status": 1,
			"breedId": null,
			"quantityPrecision": 2,
			"pricePrecision": 2,
			"breedName": "块煤",
			"commodityId": 25200,
			"name": "中块",
			"companyName": null,
			"quantity": 1000.0,
			"bestPrice": 0.0,
			"bestQuantity": 1000.0,
			"unit": "吨",
			"buyOrSell": null,
			"isQuantityShowApprox": 1,
			"breedTradeWay": null,
			"beginPrice": 750.0,
			"alertPrice": 2220.0,
			"curPrice": 0.0,
			"cureShares": null,
			"curSection": null,
			"totalSecion": null,
			"factor": null,
			"allQuantity": null,
			"hadFilterCount": 0,
			"deliveryUnit": null,
			"stationRoadId": "67",
			"orderQuantity": 0.0,
			"tradeTimeId": null,
			"sectionId": 9,
			"minOrderQuantity": null,
			"minMoveQuantity": null,
			"startTime": "08:24",
			"planStartTime": null,
			"deliveryStartDate": "2023-12-02",
			"createTime": null,
			"reportedQuantity": 0.0,
			"enableFactor": 0,
			"myFlag": false
		}]
	}],
	"matterList": [{
		"matterId": 62683,
		"matterCode": "RB23120036",
		"matterGroupNo": "RB23120036",
		"tradeModeId": 1,
		"plateId": null,
		"plateName": null,
		"status": 1,
		"breedId": null,
		"quantityPrecision": 2,
		"pricePrecision": 2,
		"breedName": "块煤",
		"commodityId": 25200,
		"name": "中块",
		"companyName": null,
		"quantity": 1000.0,
		"bestPrice": 0.0,
		"bestQuantity": 1000.0,
		"unit": "吨",
		"buyOrSell": null,
		"isQuantityShowApprox": 1,
		"breedTradeWay": null,
		"beginPrice": 750.0,
		"alertPrice": 2220.0,
		"curPrice": 0.0,
		"cureShares": null,
		"curSection": null,
		"totalSecion": null,
		"factor": null,
		"allQuantity": null,
		"hadFilterCount": 0,
		"deliveryUnit": null,
		"stationRoadId": "67",
		"orderQuantity": 0.0,
		"tradeTimeId": null,
		"sectionId": 9,
		"minOrderQuantity": null,
		"minMoveQuantity": null,
		"startTime": "08:24",
		"planStartTime": null,
		"deliveryStartDate": "2023-12-02",
		"createTime": null,
		"reportedQuantity": 0.0,
		"enableFactor": 0,
		"myFlag": false
	}],
	"drawShowOrderQty": true
}"""
        if resp['matterList'] is None:
            self.window.write_event_value('message','未有场次公布')
        else:

            matterId = resp['matterList'][0]['matterId']
            matterCode = resp['matterList'][0]['matterCode']
            tradeModeId = resp['matterList'][0]['tradeModeId']
            current_price = resp['matterList'][0]['curPrice']
            quantity = int(resp['matterList'][0]['quantity'])

            name = resp['matterList'][0]['name']
            beginPrice = resp['matterList'][0]['beginPrice']

            endTime = resp['plateVo']['endTime']
            startTime = resp['plateVo']['startTimeProcess']
            status = resp['plateVo']['status']

            self.window.write_event_value('return-info',(matterCode, name, quantity, startTime, endTime, status, beginPrice, current_price))

            if self.originalMatter != matterId:
                self.originalMatter = matterId

                self.window.write_event_value('reset-status','')
                self.start = False

            if status == 1:
                self.window.write_event_value('message', '场次%s 等待开始......'%matterCode)
                self.message += 1
            else:
                if self.get_time(endTime) == 'start' and self.start:

                    if self.limitPrice is None:

                        if current_price == 0.0:
                            bid_price = beginPrice
                        else:
                            bid_price = current_price + 1

                    else:

                        if current_price == 0.0:
                            bid_price = beginPrice

                        else:
                            if current_price < self.limitPrice:
                                bid_price = current_price + 1

                            else:
                                bid_price = None

                    if bid_price is not None:
                        self.bid(bid_price, matterId, quantity, tradeModeId)
                        # self.e.wait(3)
                        # self.get_bid_result()


    def start_bid(self, limitPrice):

        if not limitPrice.isdigit():

            self.limitPrice = None
        else:
            self.limitPrice = float(limitPrice)

        self.start = True

    def stop_bid(self):

        self.start = False


    def check_scedule(self):

        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/home/tradingPlate/list"

        try:
            response = self.s.get(url, headers=self.headers, verify=False, timeout=10)
        except:
            return

        resp = json.loads(response.text)

        if type(resp) is list:
            resp = [{'plateId': 95, 'plateName': '公开竞价（润邦矿业）', 'status': 1, 'startTime': '08:30:00',
                     'startTimeProcess': '2023-08-31 08:30:00', 'endTime': '2023-08-31 08:56:00', 'tradeModeId': 1,
                     'companyId': 66, 'companyName': '神木润邦矿业专场', 'buyOrSell': 1, 'isShareMargin': 1, 'eachMargin': None,
                     'startWay': None, 'maxMatterCount': None, 'filterNumber': 0, 'maxCount': None, 'createTime': None,
                     'modifyTime': None, 'tradeStyle': None, 'sectionId': None, 'sortProcessID': 1693441800000,
                     'breedNameType': 0, 'breedList': [{'breedId': 1020, 'breedName': '块煤', 'sortNo': 0}],
                     'matterCount': 9, 'startTimeSpecial': '2023-08-31 08:30:00', 'tradeTimeId': 6641,
                     'noTradeFlag': False}]
            if resp == []:
                try:
                    self.window.write_event_value('message','当日交易模块暂无交易计划')
                except:
                    pass
                return
            else:

                plate_dict = {}
                for i in resp:
                    plate_dict[i['plateName']] = {'plateId':i['plateId'],'tradeModeId':i['tradeModeId'],'tradeTimeId':i['tradeTimeId']}

                try:
                    self.window.write_event_value('return-plate',plate_dict)
                except:
                    pass

        else:
            if 'code' in resp.keys():
                try:
                    self.window.write_event_value('message1',resp['msg'])
                except:
                    pass
            return

    def get_time(self,limit_time):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/dbTime"

        headers = {
            'Host': 'jy.yectc.com:16952',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        b = datetime.strptime(limit_time, '%Y-%m-%d %H:%M:%S').timestamp()

        a_ = time.time()

        try:
            response = requests.get(url, headers=headers, verify=False, timeout=0.5)

            if response.status_code == 200:
                a = float(response.text)/1000
            else:
                a = a_
                self.window.write_event_value('message', '获取平台时间遭遇状态：%s,启用本地时间'%response.status_code)
                self.message += 1
        except:
            self.window.write_event_value('message', '获取平台时间超时,启用本地时间')
            self.message += 1
            a = a_

        time_gap = round((b - a),2)

        del b,a,a_
        self.window.write_event_value('return-gap', time_gap)

        if time_gap <= 1 and time_gap >=0:
            return 'start'
        else:
            return


    def bid(self, price, matterId, quantity, tradeId):

        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/open/order/single"

        payload = f"matterId={matterId}&tradeModeId={tradeId}&price={price}&quantity={quantity}"

        try:
            response = self.s.post(url, headers=self.headers, data=payload, verify=False, timeout=5)
        except:
            try:
                self.window.write_event_value('message','投标超时')
            except:
                pass
            return

        resp = json.loads(response.text)

        if 'code' in resp.keys():

            try:
                self.window.write_event_value('message1', resp['msg'])
            except:
                pass

        else:
            try:
                self.window.write_event_value('message', resp)
            except:
                pass


    def get_bid_result(self):

        url = f"https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/match/order?tradeModeId={self.tradeModeId}&tradeTimeId={self.tradeTimeId}"

        # url = 'https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/match/order?tradeModeId=1&tradeTimeId=6723'

        while True:
            if self.pause:
                break
            try:
                response = self.s.get(url, headers=self.headers, verify=False, timeout=5)
            except:
                try:
                    self.window.write_event_value('message1', '获取中标结果超时，自动重试')
                except:
                    pass
                self.message += 1
                continue

            resp = json.loads(response.text)

            if resp == []:
                pass
            else:

                table_value = []
                for x in resp:

                    orderNo = x['orderNo']
                    matterCode = x['matterCode']
                    name = x['name']
                    orderQuantity = x['orderQuantity']
                    price = x['price']
                    status = '中标' if x['orderStatus'] == 3 else '未中标'

                    table_value.append([status, orderNo, matterCode, name, orderQuantity, price])

                self.window.write_event_value('return-table', table_value)

            self.e.wait(5)

    def run(self, plateId,tradeModeId,tradeTimeId):

        self.e.clear()
        self.pause = False
        self.start = False
        self.message = 0

        self.originalMatter = ''
        while True:
            if self.pause:
                break

            if self.message >= 30:
                self.window.write_event_value('clear-message','')
                self.message = 0

            self.check_bid(plateId,tradeModeId,tradeTimeId)
            self.e.wait(0.4)


# if __name__ == '__main__':
#     f= Function()
#     f.login(user='SMCYGS',passwd='09128463')
#     f.get_bid_result()

