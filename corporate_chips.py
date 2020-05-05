import os
import time
import platform
import http.client

from urllib import request, error
from urllib.request import urlopen
from bs4 import BeautifulSoup


def downWeb(url):
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    while 1:
        try:
            req = request.Request(url, headers=headers)
            html_data = urlopen(url).read().decode()
        except error.HTTPError as e:
            print("get url Fail")
            print(e.reason, e.code, e.headers)
            return
        except error.URLError as e:
            print(e.reason)
            # resolve [Errno 111] Connection refused or Network is unreachable
            time.sleep(1)
        except http.client.HTTPException as e:
            print("HTTPException retry!!")
            time.sleep(1)
        else:
            # print('Request Successfully')
            soup = BeautifulSoup(html_data, 'html.parser')
            return soup


def clean_screen():
    sysstr = platform.system()
    if(sysstr == "Windows"):
        os.system('cls')
    elif(sysstr == "Linux"):
        os.system('clear')
    else:
        print("Other System tasks")
        os.system('clear')


while(1):
    # get optein data
    url = 'https://www.taifex.com.tw/cht/3/callsAndPutsDate'
    soup = downWeb(url)
    option_date = soup.select_one('#queryDate')
    call_value = soup.select_one(
        '#printhere > div:nth-child(4) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(6) > td:nth-child(13)').text.strip()
    put_value = soup.select_one(
        '#printhere > div:nth-child(4) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(9) > td:nth-child(13)').text.strip()
    option_net = 0

    try:
        option_net = format(int(call_value.replace(",", "")) -
                            int(put_value.replace(",", "")), ',')
    except:
        option_net = '-'

    # get future data
    url = 'https://www.taifex.com.tw/cht/3/futContractsDate'
    soup = downWeb(url)
    future_date = soup.select_one('#queryDate')
    net = soup.select_one(
        '#printhere > div:nth-child(4) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(6) > td:nth-child(13) > div:nth-child(1)').text.strip()

    clean_screen()

    # print msg
    msg = """\nOption:(%s)
    \t====================
    \tcall\t:%s
    \tput\t:%s
    \tnet\t:%s
    \nFutures:(%s)
    \t====================
    \tnet\t:%s
    \nExcel:\"%s\",\"%s\",\"%s\",\"%s\"
        """ % (option_date['value'], call_value, put_value, option_net, future_date['value'], net, net, option_net, call_value, put_value)
    print(msg)

    time.sleep(5)
