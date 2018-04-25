# # -*- coding: UTF-8 -*-
import csv
import math
import os
import os.path
import re
import sqlite3
from collections import OrderedDict
from datetime import datetime
from time import sleep
from urllib.parse import urljoin

from lxml.html import fromstring
from requests import Session

user = os.environ['USER']

MAIN_PAGE_PATH = '/Users/{}/Public/git/macappcraked_website_cralwer/codding/corpus/htmlfiles/main_pages/'.format(user)
APP_ITEM_PAGE_PATH = '/Users/{}/Public/git/macappcraked_website_cralwer/codding/corpus/htmlfiles/app_item_pages/'.format(user)
CSV_PATH = '/Users/{}/Public/git/macappcraked_website_cralwer/codding/corpus/csvfiles/'.format(user)
BASE_URL = 'http://nmac.to/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/65.0.3311.3 Safari/537.36'}


def response(start_url):
    # global HEADERS
    session = Session()
    resp = session.get(start_url, headers=HEADERS)
    return resp.text


def get_root_html(response):
    # with open('response', 'r') as source:
    root = fromstring(response)
    return root


def get_viewed_numbers(root):
    # 抓取被浏览的次数
    # 返回一个含有十个元素的list
    numbers = root.xpath('//span[@class="numcount"]/text()')
    if len(numbers) <= 10:   #  把==改为了<=
        return numbers
    else:
        for _ in range(len(numbers) - 10):
            numbers.remove(min(numbers))
        return numbers


def get_posted_time(root):
    # 抓取发布的时间
    # 返回一个含有十个元素的list
    posted_time = []
    posted_time_strings = root.xpath('//span[@class="meta-info"]/text()')
    for time_string in posted_time_strings:
        get_time = time_string.split()
        posted_time.append(get_time[1].strip())
    return posted_time


def get_title_infos(root):
    # 抓取应用标题，可以作为html文件名
    # 返回一个含有十个元素的list
    app_infos = OrderedDict()
    title_list = root.xpath('//h2/a/text()')
    for title in title_list:
        title_items = title.rsplit(sep='–', maxsplit=1)
        # get app_name and version
        name_mix_version = title_items[0].strip()
        # judge whether the last char is num.
        if len(name_mix_version.split()) > 1:
            if re.findall('[0-9]{1,}$', name_mix_version):
                mix_split = name_mix_version.rsplit(sep=' ', maxsplit=1)
                index = name_mix_version.rfind('–') + 1
            else:
                mix_split_raw = name_mix_version.rsplit(sep='+',
                                                        maxsplit=1)[0].strip()
                mix_split = mix_split_raw.rsplit(sep=' ', maxsplit=1)
                index = name_mix_version.rfind('+') + 1
            version_raw = mix_split[1].strip()
            app_name = mix_split[0].strip()
            app_decription = title[index:].strip()
            # get app_version
            dot_splited_version = version_raw.split('.')
            try:
                version_list = [int(item) for item in dot_splited_version]
            except ValueError:
                version_list = []
                for item in dot_splited_version:
                    try:
                        item = int(item)
                        version_list.append(item)
                    except ValueError:
                        if item.startswith('v'):
                            item = item[1:]
                        raw = re.findall(
                            '([a-z]{1,})|([0-9]{1,})', item)  # 分析raw的成分
                        for item in raw:
                            item1, item2 = item
                            if item1 == '':
                                version_list.append(int(item2))
                            if item2 == '':
                                version_list.append(item1)
        else:
            for char in name_mix_version:
                if char.isdigit():
                    index = name_mix_version.index(char)
                    app_name = name_mix_version[:index]
                    version_list = [app_name]
                    app_decription = title_items[1].strip()
        app_infos[app_name] = (version_list, app_decription)

    return app_infos


def get_contents(root):
    # 返回具有十个应用的简介list
    contents = root.xpath('//div[@class="excerpt"]/text()')
    if len(contents) <= 10:
        return contents
    else:
        for content in contents:
            if str(content).startswith(' '):
                index = (contents).index(content)
                contents[index] = contents[index] + contents[index + 1]
                contents.remove(contents[index + 1])
        return contents


def get_app_urls(root):
    # 抓取首页面，也就是列表页面的列表内各个软件的urls
    # creat_html_file
    # 返回具有十个元素的list
    return root.xpath('//h2/a/@href')


def download_urls(get_app_urls, titles):
    # 抓取最新版本软件的下载地址以及先前版本下载地址的导向链接，同时保存response生成各软件
    # 的主页面html文件
    global APP_ITEM_PAGE_PATH
    urls = {'newest_download_urls': [], 'previous_links': []}
    i = 0  # 用于索引titles中的各个title，以对html文件进行命名
    for url in get_app_urls:
        print('-------------------Sleep 0.8s--------------------')
        sleep(0.8)
        app_main_page_response = response(url)
        html = app_main_page_response
        root = get_root_html(app_main_page_response)
        # creat_html_file
        title = titles[i]  # 作为html文件名的头部
        if '/' in title:
            raw_title = title.split('/')
            title = ' '.join(raw_title)
        time_string = str(datetime.now()).split(' ')[0]  # 作为html文件名的副部
        with open(APP_ITEM_PAGE_PATH + title + '-' + time_string + '.html', 'w',
                  encoding='UTF-8') as f:
            f.writelines(html)

        # 抓取软件最新版本的下载链接
        if root.xpath('//td/a[text()=" Download"]/@href'):
            newest_download_url = root.xpath(
                '//td/a[text()=" Download"]/@href')[0]
        elif root.xpath('//div//a[text()=" Torrent"]/@href'):
            newest_download_url = root.xpath(
                '//div//a[text()=" Torrent"]/@href')[0]
        elif root.xpath('//p/a[text()=" Sendit.cloud"]/@href'):
            newest_download_url = root.xpath(
                '//p/a[text()=" Sendit.cloud"]/@href')[0]
        elif root.xpath('//p/a[text()=" Userscloud"]/@href'):
            newest_download_url = root.xpath(
                '//p/a[text()=" Userscloud"]/@href')[0]
        else:
            newest_download_url = 'None'
        urls['newest_download_urls'].append(newest_download_url)
        # 抓取软件先前版本的下载链接（如果有）
        previous_link_url = root.xpath(
            '//div/a[text()="Previous Versions"]/@href')
        if previous_link_url:
            previous_link_url = urljoin(
                'https://nmac.to/', previous_link_url[0])
            urls['previous_links'].append(previous_link_url)
        else:
            previous_link_url = 'This is an old game.'
            urls['previous_links'].append(['None'])
        # print('previous_link_url:', previous_link_url)
        print("Finish", i + 1, 'newest and previous links')
        i += 1
    return urls


def newest_download_urls(download_urls):
    newest_urls = download_urls['newest_download_urls']
    return newest_urls


def previous_link_urls(download_urls):
    # 抓取应用主页面的先前版本链接地址
    # 注意，这里抓取的url是相对地址，而非绝对地址。
    # 返回含有10个链接的list,元素中可能包含None
    pre_urls = download_urls['previous_links']
    return pre_urls


def previous_donwload_urls(pre_link_urls):
    # 抓取各个先前版本的下载地址
    # 返回具有0个或多个元素的list，
    urls = []
    i = 0
    for url in pre_link_urls:
        if url == ['None']:
            urls.append(['\nNone'])

            print('previous url is None')
        else:
            try:
                previous_donwload_response = response(url)
                root = get_root_html(previous_donwload_response)
                version = root.xpath('//a[@class="accordion-toggle"]/text()')
                urls_list = root.xpath('//a[text()=" Sendit.cloud"]/@href')
                if urls_list:
                    pairs = list(zip(version, urls_list))
                    urls.append(pairs)
                else:
                    urls_list = ['None']
                    pairs = list(zip(version, urls_list))
                    urls.append(pairs)
                print('-------------------Sleep 0.8s-------------------')
                sleep(0.8)
            except Exception:
                print("The uncrawled url: %s" % url)
                continue
        i += 1
        print('Finish', i, 'previous_donwload_url')
    return urls


def main_page_items(start_url):
    # 抓取主页各个应用的条目信息
    global MAIN_PAGE_PATH
    resp = response(start_url)
    root = get_root_html(resp)
    # 保存网站主页面html文件
    parsed_time = datetime.now()
    html_file_name = str(parsed_time).split('.')[0]
    with open(MAIN_PAGE_PATH + html_file_name + '.html', 'w',
              encoding='UTF-8') as f:
        f.writelines(resp)
    # 提取应用标题和应用的元信息
    app_infos = [(title, info)
                 for title, info in get_title_infos(root).items()]
    # 提取浏览量
    viewed_numbers = get_viewed_numbers(root)
    # 提取发布时间
    posted_times = get_posted_time(root)
    # 提取应用简介
    contents = get_contents(root)
    # 提取应用主页面的主应用链接
    app_urls = get_app_urls(root)
    return app_infos, viewed_numbers, posted_times, contents, app_urls


def get_item_details(app_urls, titles):
    # 爬取主页面纵向信息供后续处理，同时本地存储对应html文件
    original_urls_to_be_deal = download_urls(app_urls, titles)
    # 抓取最新版本的下载地址
    newest_urls = newest_download_urls(original_urls_to_be_deal)
    # 抓取先前版本的下载地址
    previous_urls = previous_link_urls(original_urls_to_be_deal)
    previous_urls = previous_donwload_urls(previous_urls)
    # 合并下载链接，最新版下载地址排前
    urls = list(zip(newest_urls, previous_urls))
    return urls


def generate_scv_file(csv_data):
    # 生成csv文件
    global CSV_PATH
    with open(CSV_PATH + 'meta_info.csv', 'a', encoding='UTF-8') as fil:
        handler = csv.writer(fil)
        handler.writerows(csv_data)


def start_url(page_number):
    # 生成下一个需要爬取的主页面地址
    global BASE_URL
    return urljoin(BASE_URL, 'page/' + str(page_number))


def crawling(already_stored_items, previously_crawled_number, url=None,
             page_number=1, new_crawled_item_number=0):
    # 执行抓取进程
    print('\ncrawler circling.....page%s\n' % page_number)
    app_names = []
    app_versions = []
    app_usages = []
    # need_to_stored_app_infos = []
    need_stored_item = 0  # 本次爬取的新的需要存储的应用条目
    main_page_info = main_page_items(url)  # 调用 main_apge_tiems 函数.
    app_infos = main_page_info[0]
    home_page_items_number = len(app_infos)  # 抓页面条目数量，为确定后续抓取切入点作准备
    # from_this_crawling_time_theory_crawled_number = page_number * home_page_items_number
    for item in app_infos:
        app_name = item[0]
        version = item[1][0]
        usage = item[1][1]
        if app_name not in already_stored_items or (app_name in already_stored_items and version > already_stored_items[app_name]):
            need_stored_item += 1
            new_crawled_item_number += 1
            app_names.append(app_name)
            app_versions.append('.'.join((str(item) for item in version)))
            app_usages.append(usage)
        elif app_name in already_stored_items and version < already_stored_items[app_name]:
            new_crawled_item_number += 1
        elif app_name in already_stored_items and version == already_stored_items[app_name]:
            jump_to_page_havent_been_crawled = True
    # 根据上述判断开始爬取未爬取的应用条目
    if need_stored_item > 0:
        print('need_stored_item: %d' % need_stored_item)
        app_urls = main_page_info[-1][:need_stored_item]
        urls = get_item_details(app_urls, app_names)
        viewed_numbers = main_page_info[1][:need_stored_item]
        posted_times = main_page_info[2][:need_stored_item]
        contents = main_page_info[3][:need_stored_item]
        current_app_num = previously_crawled_number + new_crawled_item_number
        data = list(zip(app_names, app_versions, app_usages, viewed_numbers,
                        posted_times, contents, urls))
        # 存储本地数据
        storing_data_in_db(data, current_app_num)
    # 判断是连续爬取还是跳转爬取
    try:
        if jump_to_page_havent_been_crawled:
            jump_to_page_havent_been_crawled = False
            current_app_num = previously_crawled_number + new_crawled_item_number
            page_number = math.floor(
                current_app_num / home_page_items_number)
    except NameError:
        pass
    page_number += 1
    # print('page_number: %d' % page_number)
    url = start_url(page_number)
    # print('url: %s' % url)
    crawling(already_stored_items, previously_crawled_number,
             page_number=page_number,
             url=url,
             new_crawled_item_number=new_crawled_item_number)


def get_stored_app_infos():
    db_path = os.path.join(os.getcwd(), 'csvfiles/app_information.sqlite')
    if os.path.exists(db_path):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('SELECT MAX(total_number) FROM App_info')
            previously_crawled_number = cur.fetchone()[0]
            cur.execute('SELECT app_name, app_version FROM App_info')
            names_and_versions = cur.fetchall()
        return previously_crawled_number, names_and_versions
    else:
        return (0,), {}


def storing_data_in_db(data, current_app_num):
    """创建数据库表格"""
    db_path = os.path.join(os.getcwd(), 'csvfiles/app_information.sqlite')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS App_info (
                app_name TEXT, app_version TEXT, app_usage TEXT,
                viewed_number INTEGER, posted_time text, content TEXT,
                url TEXT, total_number INTEGER)''')
    for item in data:
        # print('item: ', item)
        app_name, app_version, app_usage, viewed_number, posted_time, content, url = item
        cur.execute("INSERT INTO App_info VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (app_name, str(app_version), app_usage, int(viewed_number),
                     str(posted_time), str(content), str(url), current_app_num))
    conn.commit()
    print('commited finished!!!')


if __name__ == '__main__':
    already_stored_items = {}
    stored_app_infos = get_stored_app_infos()
    previously_crawled_number = stored_app_infos[0]
    print(previously_crawled_number)
    app_names_and_versions = stored_app_infos[1]
    # print(app_names_and_versions)
    try:
        for app_name, version_str in app_names_and_versions:
            app_version = []
            for item in version_str.split('.'):
                try:
                    app_version.append(int(item))
                except ValueError:
                    app_version.append(item)
            already_stored_items[app_name] = app_version
    except ValueError:
        already_stored_items = {}
    url = BASE_URL
    crawling(already_stored_items, previously_crawled_number, url=url)
