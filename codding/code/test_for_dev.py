from urllib.parse import urljoin

from the_zero_page import main

import math

BASE_URL = 'http://nmac.to/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/65.0.3311.3 Safari/537.36'}


def crawling(start_url, titles, already_stored_items, page_number=None):
    """执行抓取进程"""
    new_crawled_item_number = 0  # 当前爬取的全部未爬取过的应用条目数量
    new_titles = []  # 本次爬取的新的需要存储的应用条目
    main_page_info = main_page_items(start_url)  # 调用 main_apge_tiems 函数.
    titles = main_page_info[0]
    home_page_items_number = len(titles)  # 抓页面条目数量，为确定后续抓取切入点作准备

    for title in titles:
        title_split = title.rsplit(sep=' ', maxsplit=1)
        app_name = title_split[0]
        app_version = title_split[1]
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
    csv_data = list(zip(new_titles, meta_infos, viewed_numbers,
                        times, urls, contents))

    # 存储本地数据
    generate_scv_file(csv_data)

    # 判断是连续爬取还是跳转爬取
    if not jump_to_page_havent_been_crawled:
        for i in range(2, 700):
                crawling(start_url(i))
    else:
        previously_crawled_number = get_previously_crawled_number()
        have_been_crawed_items_number = new_crawled_item_number + previously_crawled_number
        page_number = math.floor(have_been_crawed_items_number / home_page_items_number)
        url = start_url(page_number)
        crawling(url)


def start_url(page_number):
    return urljoin(base_url, 'page/' + str(page_number))


def get_already_stored_items():
    app_items = {}
    with open('./meta_info.csv', 'rt', encoding="UTF-8") as f:
        import re
        pattern = re.compile('(^.*?),')
        for line in f:
            item = pattern.findall(line)[0]
            item_split = item.rsplit(sep=' ', maxsplit=1)
            app_items[item_split[0]] = item_split[1]
        return app_items


def get_previously_crawled_number():



if __name__ == '__main__':
    already_stored_items = get_already_stored_items()
    previously_crawled_number = get_previously_crawled_number()
