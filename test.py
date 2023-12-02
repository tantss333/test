import requests

url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/match/order?tradeModeId=1&tradeTimeId=6641"

payload = {}
headers = {
  'Host': 'jy.yectc.com:16952',
  'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
  'Accept': 'application/json, text/plain, */*',
  'UserID': 'YLBYNYKJ',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
  'Token': '4c00e473-49c2-4878-933f-ebef28dff4bd',
  'sec-ch-ua-platform': '"macOS"',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://jy.yectc.com:16952/',
  'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,de;q=0.6,de-DE;q=0.5',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
