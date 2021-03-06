import re
import datetime
import requests
from bs4 import BeautifulSoup


def generate_pages_list(total_pages, range, init_page_id):
    page_list = list()
    k = init_page_id

    while k + range - 1 <= total_pages:
        page_list.append((k, k + range -1))
        k += range

    if k + range - 1 < total_pages:
        page_list.append((k, total_pages))

    return page_list


def count_chn(string):
    '''Count Chinese numbers and calculate the frequency of Chinese occurrence.

    # Arguments:
        string: Each part of crawled website analyzed by BeautifulSoup.
    '''
    pattern = re.compile(u'[\u1100-\uFFFDh]+?')
    result = pattern.findall(string)
    chn_num = len(result)
    possible = chn_num / len(str(string))

    return chn_num, possible


def get_date_list_from_range(begin_date, end_date):
    '''Get date list from 'begin_date' to 'end_date' on the calendar.
    '''
    date_list = list()
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)

    return date_list


def gen_dates_list(date_list, date_range):
    date_list_latest = list()
    k = 0
    while k < len(date_list):
        if k + date_range >= len(date_list):
            break
        else:
            date_list_latest.append(date_list[k: k + date_range])
            k += date_range
    date_list_latest.append(date_list[k:])

    return date_list_latest


def search_max_pages_num(first_url, date):
    """
    主要针对金融界网站
    通过日期搜索新闻，比如2020年1月1日的新闻，下面链接
    http://stock.jrj.com.cn/xwk/202001/20200101_1.shtml
    为搜索返回的第一个网页，通过这个网页可以发现，数据库
    返回的最大页数是4，即2020年1月1日共有4页的新闻列表
    :param first_url: 搜索该日期返回的第一个网址，如'http://stock.jrj.com.cn/xwk/202001/20200101_1.shtml'
    :param date: 日期，如'2020-01-01'
    """
    respond = requests.get(first_url)
    respond.encoding = BeautifulSoup(respond.content, "lxml").original_encoding
    bs = BeautifulSoup(respond.text, "lxml")
    a_list = bs.find_all("a")
    max_pages_num = 1
    for a in a_list:
        if "href" in a.attrs and "target" in a.attrs:
            if a["href"].find(date.replace("-", "") + "_") != -1 \
                    and a.text.isdigit():
                max_pages_num += 1

    return max_pages_num


def html_parser(url):
    resp = requests.get(url)
    resp.encoding = BeautifulSoup(resp.content, "lxml").original_encoding
    bs = BeautifulSoup(resp.text, "lxml")

    return bs