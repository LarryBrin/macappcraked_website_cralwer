import math
import sqlite3
from urllib.parse import urljoin
from the_zero_page import get_item_details, main_page_items, generate_scv_file

BASE_URL = 'http://nmac.to/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/65.0.3311.3 Safari/537.36'}


def crawling(start_url, already_stored_items, page_number=None):
    """执行抓取进程"""
    new_crawled_item_number = 0  # 当前爬取的全部未爬取过的应用条目数量
    new_titles = []  # 本次爬取的新的需要存储的应用条目
    main_page_info = main_page_items(start_url)  # 调用 main_apge_tiems 函数.
    titles = main_page_info[0]
    home_page_items_number = len(titles)  # 抓页面条目数量，为确定后续抓取切入点作准备

    for title in titles:
        title_split = title.rsplit(sep=' ', maxsplit=1)
        app_name = title_split[0]
        app_version = float(itle_split[1].strip())
        if app_name not in already_stored_items:
            new_titles.append(title)
            new_crawled_item_number += 1
        elif app_name in already_stored_items and app_version > already_stored_items[app_name]:
            new_titles.append(title)
            new_crawled_item_number += 1
        elif app_name in already_stored_items and app_version < already_stored_items[app_name]:
            new_crawled_item_number += 1
        elif app_name in already_stored_items and app_version == already_stored_items[]:
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

    # 判断是连续爬取还是跳转爬取
    try:
        if jump_to_page_havent_been_crawled:
            previously_crawled_number = get_previously_crawled_number()
            have_been_crawed_items_number = new_crawled_item_number + previously_crawled_number
            page_number = math.floor(have_been_crawed_items_number / home_page_items_number)
            url = start_url(page_number)
            crawling(url)
    except NameError as e:
        for i in range(2, 700):
            crawling(start_url(i))


def start_url(page_number):
    return urljoin(base_url, 'page/' + str(page_number))


def get_already_stored_items_and_app_number():
    app_items = {}
    app_num = 0
    with open('./meta_info.csv', 'rt', encoding="UTF-8") as f:
        import re
        pattern = re.compile('(^.*?),')
        for line in f:
            item = pattern.findall(line)[0]
            item_split = item.rsplit(sep=' ', maxsplit=1)
            app_items[item_split[0]] = float(item_split[1].strip())
            app_num += 1
        return app_items, app_num


def storing_data_in_db(data):
    """创建数据库表格"""
    conn = sqlite3.connect(app_information.sqlite)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS App_info (title text, meta_info text,
                time text, viewed_numbers text, url text)''')
    for item in data:
        new_title, meta_info, viewed_number, time, url, content = item
        cur.execute("INSERT INTO App_info VALUES (?, ?, ?, ?, ?)",
                    (new_title, meta_info, viewed_number, time, url, content))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    already_stored_items_and_app_number = get_already_stored_items_and_app_number()
    already_stored_items = already_stored_items_and_app_number[0]
    previously_crawled_number = already_stored_items_and_app_number[1]


exit with code null, signal SIGABRT
