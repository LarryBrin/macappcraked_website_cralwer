from lxml.html import fromstring
from requests import Session


def headersGenerator(headersFileName):
    with open(headersFileName, 'r') as fh:
        headers = {}
        for line in fh:
            line = line.strip().split(":")
            if line[0] == 'User-Agent':
                headers[line[0].strip()] = line[1].strip()
                return headers


def response(start_url):
    session = Session()
    headers = headersGenerator('headers.txt')
    response = session.get(start_url, headers=headers)
    return response


def creat_html_file(response):
    with open('../pages_sources/filename.html', 'w+', encoding='UTF-8') as f:
        f.write(response.text)


def get_root_html(html_file):
    with open('html_file', 'r') as source:
        return fromstring(source.read())


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
        posted_time.append(get_time[1])
    return posted_time


def get_titles(root):
    # 抓取应用标题，可以作为html文件名
    # 返回一个含有十个元素的list
    titles_item = []
    titles = root.xpath('//h2/a/text()')
    for title in titles:
        title_item = title.split('–')
        titles_item.append(title_item)
    return titles_item


def get_contents(root):
    # 返回具有十个应用的简介list
    contents = root.xpath('//div[@class="excerpt"]/text()')
    for content in contents:
        if not content.rstrip().endswith('[…]'):
            index = contents.index(content)
            contents[index] = contents[index] + contents[index + 1]
            contents.remove(contents[index + 1])
    return contents


def main_page_urls(root):
    # 抓取首页面，也就是列表页面的列表内各个软件的urls
    # creat_html_file
    # 返回具有十个元素的list
    return root.xpath('//h2/a/@href')


def download_urls(main_page_urls):
    download_urls = {'newest_download_urls': [], 'previous_links': []}
    for url in main_page_urls:
        app_main_page_response = response(url)
        # creat_html_file
        root = get_root_html(app_main_page_response)
        # 抓取软件最新版本的下载链接
        newest_download_url = root.xpath(
            '//p/a[text()=" Sendit.cloud"]/@href')[0]
        download_urls['newest'].append(newest_download_url)
        # 抓取软件先前版本的下载链接（如果有）
        previous_link_url = root.xpath(
            '//div/a[text()="Previous Versions"]/@href')
        if previous_link_url:
            from urllib.parse import urljoin
            previous_link_url = urljoin(
                'https://nmac.to/', previous_link_url[0])
            download_urls['previous_link'].append(previous_link_url)
        else:
            previous_link_urls.append(None)
    return download_urls


def newest_download_urls(download_urls):
    newest_urls = download_urls['newest_download_urls']
    return newest_urls


def previous_link_urls(download_urls):
    # 抓取应用主页面的先前版本链接地址
    # 注意，这里抓取的url是相对地址，而非绝对地址。
    # 返回含有10个链接的list,元素中可能包含None
    previous_link_urls = download_urls['previous_links']
    return previous_link_urls


def previous_donwload_urls(previous_link_urls):
    # 抓取各个先前版本的下载地址
    # 返回具有0个或多个元素的list，
    previous_donwload_urls = []
    for url in previous_link_urls:
        if not url:
            previous_donwload_urls.append(None)
        else:
            previous_donwload_response = response(url)
            root = get_root_html(previous_donwload_response)
            versions = root.xpath('//a[@class="accordion-toggle"]/text()')
            urls = root.xpath('//a[text()=" Sendit.cloud"]/@href')
            previous_donwload_urls.append(urls)
    return list(zip(versions, urls))


if __name__ == '__main__':
    pass
