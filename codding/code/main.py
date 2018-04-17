import csv
import os.path
from datetime import datetime
from time import sleep

from requests import Session

start_url = 'http://nmac.to'

response = response(start_url)
root = get_root_html(response)

# 保存网站主页面html文件
parsed_time = datetime.now()
html_file_name = str(parsed_time)
with open('../pages_sources/htmlfiles/main_pages' +
          html_file_name + '.html', 'w', encoding='UTF-8') as f:
    f.writelines(response.text)
del response


session = Session()
# 提取浏览量
viewed_numbers = get_viewed_numbers(root)

# 提取发布时间
times = []
posted_time = get_posted_time(root)
for item in posted_time:
    times.append(item.split(' ')[1])

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
newest_download_urls = newest_download_url(original_urls_to_be_deal)
# 抓取先前版本的下载地址
previous_link_urls = previous_link_urls(original_urls_to_be_deal)
previous_donwload_urls = previous_donwload_urls(previous_link_urls)
# 合并下载链接，最新版下载地址排前
urls = newest_download_urls.extend(previous_donwload_urls)

# 预处理存入csv的数据
csv_data = list(zip(titles, meta_infos, times, viewed_numbers,
                    urls))
if not os.path.exists('../pages_sources/csvfiles/meta_info.csv'):
    with open('../pages_sources/csvfiles/meta_info.csv', 'a',
              encoding='UTF-8') as fil:
        handler = csv.writer(fil)
        handler.writerow('title', 'meta_info', 'time',
                         'viewed_number', 'url')
        for data in csv_data:
            title = data[0]
            meta_info = data[1]
            time = data[2]
            viewed_number = data[3]
            url = data[4]
            handler.writerow(title, meta_info, time,
                             viewed_number, url)

else:
    with open('../pages_sources/csvfiles/meta_info.csv', 'a',
              encoding='UTF-8') as fil:
        handler = csv.writer(fil)
        for data in csv_data:
            title = data[0]
            meta_info = data[1]
            time = data[2]
            viewed_number = data[3]
            url = data[4]
            handler.writerow(title, meta_info, time,
                             viewed_number, url)
