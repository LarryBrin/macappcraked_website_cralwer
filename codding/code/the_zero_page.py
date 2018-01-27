import csv
import sqlite3
import os.path
from datetime import datetime
from time import sleep
from urllib.parse import urljoin

from requests import Session

from lxml.html import fromstring

MAIN_PAGE_PATH = '/Users/larrybrin/Public/git/macappcraked_website_cralwer/codding/corpus/htmlfiles/main_pages/'
APP_ITEM_PAGE_PATH = '/Users/larrybrin/Public/git/macappcraked_website_cralwer/codding/corpus/htmlfiles/app_item_pages/'
CSV_PATH = '/Users/larrybrin/Public/git/macappcraked_website_cralwer/codding/corpus/csvfiles/'
BASE_URL = 'http://nmac.to/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/65.0.3311.3 Safari/537.36'}


def response(start_url):
    global HEADERS
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
    for number in numbers:
        if int(number) < 50:  # 过滤掉liked_numbers
            numbers.remove(number)
    return numbers


def get_posted_time(root):
    # 抓取发布的事件
    # 返回一个含有十个元素的list
    posted_time = []
    posted_time_strings = root.xpath('//span[@class="meta-info"]/text()')
    for time_string in posted_time_strings:
        get_time = time_string.split()
        posted_time.append(get_time[1].strip())
    return posted_time


def get_titles_and_meta_infos(root):
    # 抓取应用标题，可以作为html文件名
    # 返回一个含有十个元素的list
    titles = []
    meta_infos = []
    title_list = root.xpath('//h2/a/text()')
    for title in title_list:
        title_item = title.split('–')
        titles.append(title_item[0].strip())
        meta_infos.append(title_item[1].strip())
    return titles, meta_infos


def get_contents(root):
    # 返回具有十个应用的简介list
    contents = root.xpath('//div[@class="excerpt"]/text()')
    for content in contents:
        if not content.rstrip().endswith('[…]'):
            index = contents.index(content)
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
        print('\n-------------------Sleep 1.0s--------------------\n')
        sleep(1.0)
        app_main_page_response = response(url)
        html = app_main_page_response
        root = get_root_html(app_main_page_response)
        # creat_html_file
        title = titles[i]  # 作为html文件名的头部
        time_string = str(datetime.now()).split(' ')[0]  # 作为html文件名的副部
        with open(APP_ITEM_PAGE_PATH + time_string + title + '.html', 'w',
                  encoding='UTF-8') as f:
            f.writelines(html)
        # 抓取软件最新版本的下载链接
        newest_download_url = root.xpath(
            '//p/a[text()=" Sendit.cloud"]/@href')[0]
        urls['newest_download_urls'].append(newest_download_url)
        # 抓取软件先前版本的下载链接（如果有）
        previous_link_url = root.xpath(
            '//div/a[text()="Previous Versions"]/@href')
        if previous_link_url:
            previous_link_url = urljoin(
                'https://nmac.to/', previous_link_url[0])
            urls['previous_links'].append(previous_link_url)
        else:
            previous_link_url = 'None'
            urls['previous_links'].append(['None'])
        print('\nprevious_link_url:', previous_link_url)
        print("\nFinish", i + 1, 'newest and previous links')
        i += 1
        # sleep(0.6)
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
        print('\n-------------------Sleep 1.5s-------------------\n')
        sleep(1.5)
        if url == ['None']:
            urls.append(['\nNone'])

            print('previous url is None')
        else:
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
        print('Finish', i + 1, 'app previous links')
        i += 1
        print('Finish', i, 'previous_donwload_url')
    print('')
    print("previous urls:", urls)
    print(len(urls))
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
    titles_and_meta_infos = get_titles_and_meta_infos(root)
    titles = titles_and_meta_infos[0]
    meta_infos = titles_and_meta_infos[1]

    # 提取浏览量
    viewed_numbers = get_viewed_numbers(root)

    # 提取发布时间
    times = get_posted_time(root)

    # 提取应用简介
    contents = get_contents(root)

    # 提取应用主页面的主应用链接
    app_urls = get_app_urls(root)
    return titles, meta_infos, viewed_numbers, times, contents, app_urls


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
    if not os.path.exists(CSV_PATH + 'meta_info.csv'):
        with open(CSV_PATH + 'meta_info.csv', 'a', encoding='UTF-8') as fil:
            handler = csv.writer(fil)
            handler.writerow(('title', 'meta_info', 'time',
                              'viewed_number', 'url', 'content'))
            handler.writerows(csv_data)

    else:
        with open(CSV_PATH + 'meta_info.csv', 'a', encoding='UTF-8') as fil:
            handler = csv.writer(fil)
            handler.writerows(csv_data)


def crawling(url, already_stored_items, previously_crawled_number,
             start_num=2, page_number=None, new_crawled_item_number=0):
    # 执行抓取进程
    new_titles = []  # 本次爬取的新的需要存储的应用条目
    main_page_info = main_page_items(url)  # 调用 main_apge_tiems 函数.
    titles = main_page_info[0]
    home_page_items_number = len(titles)  # 抓页面条目数量，为确定后续抓取切入点作准备

    for title in titles:
        title_split = title.rsplit(sep=' ', maxsplit=1)
        app_name = title_split[0]
        app_version_str = title_split[1].strip().split('.')
        item_num = len(app_version_str)
        app_version_set = {int(item) for item in app_version_str}
        if app_name not in already_stored_items:
            new_titles.append(title)
            new_crawled_item_number += 1
        elif app_name in already_stored_items and app_version_set > already_stored_items[app_name]:
            new_titles.append(title)
            new_crawled_item_number += 1
        elif app_name in already_stored_items and app_version_set < already_stored_items[app_name]:
            new_crawled_item_number += 1
        elif app_name in already_stored_items and app_version_set == already_stored_items[app_name]:
            jump_to_page_havent_been_crawled = True

    # 根据上述判断开始爬取未爬取的应用条目
    should_be_crawled_items_number = len(new_titles)
    app_urls = main_page_info[-1][:should_be_crawled_items_number]
    urls = get_item_details(app_urls, new_titles)
    meta_infos = main_page_info[1]
    times = main_page_info[2]
    viewed_numbers = main_page_info[3]
    contents = main_page_info[-2]
    data = list(zip(new_titles, meta_infos, viewed_numbers,
                    times, urls, contents))

    # 存储本地数据
    generate_scv_file(data)
    storing_data_in_db(data)

    # 判断是连续爬取还是跳转爬取
    try:
        if jump_to_page_havent_been_crawled:  # 跳转爬取
            url = start_url(page_number)
    except NameError as e:
            url = start_url(start_num)
            have_been_crawed_items_number = previously_crawled_number + new_crawled_item_number
            page_number = math.floor(have_been_crawed_items_number / home_page_items_number)
    else:
        print('There is some fatal error, Check it!')
        # break
    finally:
        crawling(url, already_stored_items, previously_crawled_number,page_number=page_number)
        start_num += 1
        page_number += 1


def start_url(page_number):
    # 生成下一个需要爬取的主页面地址
    return urljoin(base_url, 'page/' + str(page_number))


def get_already_stored_items_and_app_number():
    global CSV_PATH
    app_items = {}
    app_num = 0
    try:
        with open(CSV_PATH + 'meta_info.csv', 'rt', encoding="UTF-8") as f:
            import re
            pattern = re.compile('(^.*?),')
            for line in f:
                item = pattern.findall(line)[0]
                item_split = item.rsplit(sep=' ', maxsplit=1)
                version_str = item_split[1]
                dot_split = version_str.split('.')
                version_set = {int(item) for item in dot_split}
                app_items[item_split[0]] = version_set
                app_num += 1
            return app_items, app_num
    except FileNotFoundError as e:
        return {}, 0


def storing_data_in_db(data):
    """创建数据库表格"""
    conn = sqlite3.connect(CSV_PATH + 'app_information.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS App_info (title text, meta_info text,
                viewed_number text, posted_time text, url text, content text)''')
    for item in data:
        new_title, meta_info, viewed_number, posted_time, url, content = item
        cur.execute("INSERT INTO App_info VALUES (?, ?, ?, ?, ?, ?)",
                    (str(new_title), str(meta_info), str(viewed_number),
                     str(posted_time), str(url), str(content)))
    conn.commit()
    # conn.close()

if __name__ == '__main__':
    already_stored_items_and_app_number = get_already_stored_items_and_app_number()
    already_stored_items = already_stored_items_and_app_number[0]
    previously_crawled_number = already_stored_items_and_app_number[1]
    url = BASE_URL
    crawling(url, already_stored_items, previously_crawled_number)
