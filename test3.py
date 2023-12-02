import requests

url = "https://xkczb.xaiip.org.cn/applyservice/app/appointForm/add"

payload = "{\"identityType\":\"xaxqyjrc\",\"applyType\":\"transfer\",\"name\":\"谭晟\",\"phone\":\"13431908484\",\"idCard\":\"440402199103199233\",\"appointIdentity\":\"personal\",\"applyIdentity\":\"personal\",\"appointType\":\"transfer\",\"targetType\":\"NewEnergyIncremental\",\"businessType\":\"transfer\",\"workplace\":\"xiongan\",\"address\":\"xionganAddress\",\"newNum\":null,\"nonNewNum\":1,\"startTime\":\"09:30\",\"endTime\":\"09:30\",\"whatTime\":\"pm\",\"startDate\":\"2023-09-12\",\"code\":\"6a344c720493e3adc761371eafa18ee5\"}"
headers = {
  'Host': 'xkczb.xaiip.org.cn',
  'X-Access-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTM4ODA3MTEsInVzZXJuYW1lIjoiMTM0MzE5MDg0ODQifQ.d29BFaPQ9OteH1mAxOYT42z8uSzmR6H52nVe1Mrh8XY',
  'Content-Type': 'application/json;charset=UTF-8',
  'Accept': '*/*',
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
  # 'Referer': 'https://servicewechat.com/wx7edb03739857186f/12/page-frame.html'
}

response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'), verify=False)

print(response.text)
