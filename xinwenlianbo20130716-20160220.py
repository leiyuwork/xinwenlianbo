import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Referer': 'http://tv.cctv.com/lm/xwlb/',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}


def href(date):
    """
    用于获取某天新闻联播各条新闻的链接
    :param date: 日期，形如20190101
    :return: href_list: 返回新闻链接的列表
    """
    href_list = []

    response = requests.get('http://cctv.cntv.cn/lm/xinwenlianbo/' + str(date) + '.shtml', headers=headers)
    bs_obj = BeautifulSoup(response.text, 'lxml')
    try:
        title = bs_obj.find("title").get_text()
        if "ERROR" in title:
            print(str(date) + " : this day is not accessible")
            log_date = open(
                r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20130716-20160220\xinwenlianbo20130716-20160220-log.txt",
                'a', encoding='utf-8')
            log_date.write(str(date) + " : this day is not accessible")
            log_date.write('\n')
            log_date.close()
    finally:
        lis = bs_obj.find_all('a')

        aaa = str(date)
        list1 = list(aaa)
        list1.insert(4,"/")
        list1.insert(7, "/")

        timeconfirm = "".join(list1)

        for each in lis:
            if timeconfirm in str(each):
                href_list.append(each.get('href'))
            elif str(date) in str(each):
                href_list.append(each.get('href'))

        return href_list
        #print(href_list)


def news(url):
    print(url)
    log_url = open(
        r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20130716-20160220\xinwenlianbo20130716-20160220-log.txt",
        'a', encoding='utf-8')
    log_url.write(url)
    log_url.write('\n')
    log_url.close()
    response = requests.get(url, headers=headers, )
    response.encoding = response.apparent_encoding
    bs_obj = BeautifulSoup(response.content, 'lxml')
    text = ""
    if 'news.cntv.cn' in url:
        url = url.replace('news.cntv.cn', 'tv.cctv.com')
        #print(url)
        response = requests.get(url, headers=headers, )
        response.encoding = response.apparent_encoding
        bs_obj = BeautifulSoup(response.content, 'lxml')
        if 'tv.cctv.com' in url:
            try:
                text = bs_obj.find('div', {'class': 'cnt_bd'}).text
            except AttributeError:
                text = ""
                print(url + " : this content is not accessible")
                log_con = open(
                    r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20130716-20160220\xinwenlianbo20130716-20160220-log.txt",
                    'a', encoding='utf-8')
                log_con.write(url + " : this content is not accessible")
                log_con.write('\n')
                log_con.close()

    return text
    #print(text)


def datelist(beginDate, endDate):
    # beginDate, endDate是形如‘20160601’的字符串或datetime格式
    date_l = [datetime.strftime(x, '%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l


def save_text(date):
    f = open(r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20130716-20160220\\" + str(date) + '.txt', 'a', encoding='utf-8')
    for each in href(date)[1:]:
        f.write(news(each))
        f.write('\n')
    f.close()


for date in datelist('20130716', '20160220'):
    try:
        save_text(date)
    except:
        print(date + " : unexpected error happened")
    time.sleep(5)
