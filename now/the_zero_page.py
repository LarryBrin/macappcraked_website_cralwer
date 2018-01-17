import csv
import os.path
from datetime import datetime
from time import sleep

from requests import Session

from lxml.html import fromstring

# def headersGenerator(headersFileName):
#     with open(headersFileName, 'r') as fh:
#         headers = {}
#         for line in fh:
#             line = line.strip().split(":")
#             if line[0] == 'User-Agent':
#                 headers[line[0].strip()] = line[1].strip()
#                 return headers


def response(start_url):
    session = Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/65.0.3311.3 Safari/537.36'}
    resp = session.get(start_url, headers=headers)
    return resp.text


# def creat_html_file(response):
#     with open('../pages_sources/filename.html', 'w+', encoding='UTF-8') as f:
#         f.write(response.text)


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


# response = response('https://nmac.to/')
# root = get_root_html(response)
# get_app_urls = get_app_urls(root)
# for url in get_app_urls:
#     print(url)
# print(get_app_urls)


def download_urls(get_app_urls, titles):
    # 抓取最新版本软件的下载地址以及先前版本下载地址的导向链接，同时保存response生成各软件
    # 的主页面html文件
    sleep(1.0)
    urls = {'newest_download_urls': [], 'previous_links': []}
    i = 0  # 用于索引titles中的各个title，以对html文件进行命名
    for url in get_app_urls:
        print('-------Sleep time' * 5)
        print('Sleep 1.0s')
        print('-------Sleep over' * 5)
        app_main_page_response = response(url)
        html = app_main_page_response
        root = get_root_html(app_main_page_response)
        # creat_html_file
        title = titles[i]
        time_string = str(datetime.now())
        with open('../pages_sources/htmlfiles/app_item_pages/' + title
                  + time_string + '.html', 'w', encoding='UTF-8') as f:
            f.writelines(html)
        # 抓取软件最新版本的下载链接
        newest_download_url = root.xpath(
            '//p/a[text()=" Sendit.cloud"]/@href')[0]
        urls['newest_download_urls'].append(newest_download_url)
        # 抓取软件先前版本的下载链接（如果有）
        previous_link_url = root.xpath(
            '//div/a[text()="Previous Versions"]/@href')
        print('')
        print('previous_link_url:', previous_link_url)
        print('')
        if previous_link_url:
            from urllib.parse import urljoin
            previous_link_url = urljoin(
                'https://nmac.to/', previous_link_url[0])
            urls['previous_links'].append(previous_link_url)
        else:
            previous_link_url.append('None')
        print("Finish", i + 1, 'newest and previous links')
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
    pre_link_urls = download_urls['previous_links']
    return pre_link_urls


def previous_donwload_urls(pre_link_urls):
    # 抓取各个先前版本的下载地址
    # 返回具有0个或多个元素的list，
    urls = []
    i = 0
    for url in pre_link_urls:
        print('-------Sleep time' * 5)
        sleep(1.5)
        print('-------Sleep over' * 5)
        if url == 'None':
            urls.append('None')
            print('previous url is None')
        else:
            previous_donwload_response = response(url)
            root = get_root_html(previous_donwload_response)
            # versions = root.xpath('//a[@class="accordion-toggle"]/text()')
            urls_list = root.xpath('//a[text()=" Sendit.cloud"]/@href')
            if urls_list:
                urls.append(urls_list)
            else:
                urls.append('None')
        print('Finish', i + 1, 'app previous links')
        i += 1
        # print('Finish',i, 'previous_donwload_url')
    print('')
    print("previous urls:", urls)
    print(len(urls))
    return urls


if __name__ == '__main__':
    start_url = 'http://nmac.to'
    resp = response(start_url)
    root = get_root_html(resp)
    print(root)

    # 保存网站主页面html文件
    parsed_time = datetime.now()
    html_file_name = str(parsed_time)
    with open('../pages_sources/htmlfiles/main_pages/' +
              html_file_name + '.html', 'w', encoding='UTF-8') as f:
        f.writelines(resp)
    # del response

    # 提取浏览量
    viewed_numbers = get_viewed_numbers(root)

    # 提取发布时间
    times = get_posted_time(root)

    # 提取应用标题和应用的元信息
    titles_and_meta_infos = get_titles_and_meta_infos(root)
    titles = titles_and_meta_infos[0]
    meta_infos = titles_and_meta_infos[1]

    # 提取应用简介
    contents = get_contents(root)

    # 提取应用主页面的主应用链接
    app_urls = get_app_urls(root)
    # 爬取主页面纵向信息供后续处理，同时本地存储对应html文件
    original_urls_to_be_deal = download_urls(app_urls, titles)
    # 抓取最新版本的下载地址
    newest_urls = newest_download_urls(original_urls_to_be_deal)
    # 抓取先前版本的下载地址
    previous_link_urls = previous_link_urls(original_urls_to_be_deal)
    previous_donwload_urls = previous_donwload_urls(previous_link_urls)
    # 合并下载链接，最新版下载地址排前
    # urls = newest_download_urls.extend(previous_donwload_urls)
    urls = newest_urls
    # i = 0
    # for newest in newest_urls:
    #     urls.append([newest])
    #     urls[i].append(previous_donwload_urls[i])
    #     i += 1
    # print(urls)

    # 预处理存入csv的数据
    csv_data = list(zip(titles, meta_infos, times, viewed_numbers,
                        urls))

    # 生成csv文件
    if not os.path.exists('../pages_sources/csvfiles/meta_info.csv'):
        with open('../pages_sources/csvfiles/meta_info.csv', 'a',
                  encoding='UTF-8') as fil:
            handler = csv.writer(fil)
            handler.writerow(('title', 'meta_info', 'time',
                              'viewed_number', 'url'))
            # for data in csv_data:
            #     title = data[0]
            #     meta_info = data[1]
            #     time = data[2]
            #     viewed_number = data[3]
            #     url = data[4]
            handler.writerows(csv_data)

    else:
        with open('../pages_sources/csvfiles/meta_info.csv', 'a',
                  encoding='UTF-8') as fil:
            handler = csv.writer(fil)
            # for data in csv_data:
            #     title = data[0]
            #     meta_info = data[1]
            #     time = data[2]
            #     viewed_number = data[3]
            #     url = data[4]
            handler.writerows(csv_data)
