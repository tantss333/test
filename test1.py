import time
from datetime import datetime

import requests, urllib3


urllib3.disable_warnings()


def get_time():
    url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/dbTime"

    headers = {
      'Host': 'jy.yectc.com:16952',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers,verify=False, timeout=10)

    a= datetime.fromtimestamp(int(response.text)/1000)

    time_gap = (limit_time-a).seconds

    print(time_gap)

if __name__ == '__main__':
    print(time.time())
    print(datetime.fromtimestamp(time.time()))
    limit_time_str = '2023-08-30 00:18'
    limit_time = datetime.strptime(limit_time_str,'%Y-%m-%d %H:%M')

    # while True:
    #     get_time()
        # time.sleep(5)
