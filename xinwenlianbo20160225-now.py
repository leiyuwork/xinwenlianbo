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

    response = requests.get('http://tv.cctv.com/lm/xwlb/day/' + str(date) + '.shtml', headers=headers)
    bs_obj = BeautifulSoup(response.text, 'lxml')
    try:
        title = bs_obj.find("title").get_text()
        if "ERROR" in title:
            print(str(date) + " : this day is not accessible")
            log_date = open(
                r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20160225-\xinwenlianbo20160225-log.txt",
                'a', encoding='utf-8')
            log_date.write(str(date) + " : this day is not accessible")
            log_date.write('\n')
            log_date.close()
    finally:
        lis = bs_obj.find_all('li')
        for each in lis:
            href_list.append(each.find('a')['href'])
        return href_list


def news(url):
    print(url)
    log_url = open(
        r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20160225-\xinwenlianbo20160225-log.txt",
        'a', encoding='utf-8')
    log_url.write(url)
    log_url.write('\n')
    log_url.close()
    response = requests.get(url, headers=headers, )
    response.encoding = response.apparent_encoding
    bs_obj = BeautifulSoup(response.content, 'lxml')
    text = ""
    if 'news.cctv.com' in url:
        try:
            text = bs_obj.find('div', {'id': 'content_body'}).text

        except AttributeError:
            text = ""
            print(url + " : this content is not accessible")
            log_con = open(
                r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20160225-\xinwenlianbo20160225-log.txt",
                'a', encoding='utf-8')
            log_con.write(url + " : this content is not accessible")
            log_con.write('\n')
            log_con.close()
    else:
        try:
            text = bs_obj.find('div', {'class': 'cnt_bd'}).text
        except AttributeError:
            text = ""
            print(url + " : this content is not accessible")
            log_con = open(
                r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20160225-\xinwenlianbo20160225-log.txt",
                'a', encoding='utf-8')
            log_con.write(url + " : this content is not accessible")
            log_con.write('\n')
            log_con.close()
    return text

    # print(text)


def datelist(beginDate, endDate):
    # beginDate, endDate是形如‘20160601’的字符串或datetime格式
    date_l = [datetime.strftime(x, '%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l


def save_text(date):
    f = open(r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20160225-\\" + str(date) + '.txt', 'a', encoding='utf-8')
    for each in href(date)[1:]:
        f.write(news(each))
        f.write('\n')
    f.close()


for date in datelist('20160225', '20200929'):
    try:
        save_text(date)
    except:
        print(date + " : unexpected error happened")
        log_date = open(
            r"C:\Users\ray\OneDrive\Research\PHD\Research\data\context analysis\xinwenlianbo20160225-\xinwenlianbo20160225-log.txt",
            'a', encoding='utf-8')
        log_date.write(date + " : unexpected error happened")
        log_date.write('\n')
        log_date.close()
    time.sleep(5)

