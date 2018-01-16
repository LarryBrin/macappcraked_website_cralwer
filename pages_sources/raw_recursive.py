
import csv
# import json
import os.path

# from datetime import datetime

# from lxml.html import fromstring


def get_root_html(html_file):
    from lxml.html import fromstring
    with open(html_file, 'r', encoding='UTF-8') as source:
        return fromstring(source.read())


def get_urls(root):
    urls = root.xpath('//h2/a/@href')
    return urls


def get_viewed_numbers(root):
    numbers = root.xpath('//span[@class="numcount"]/text()')
    for number in numbers:
        if int(number) < 20:
            numbers.remove(number)
    return numbers


def get_titles(root):
    titles = root.xpath('//h2/a/text()')
    return titles


def get_contents(root):
    contents = root.xpath('//div[@class="excerpt"]/text()')
    for content in contents:
        if not content.rstrip().endswith('[…]'):
            index = contents.index(content)
            contents[index] = contents[index] + contents[index + 1]
            contents.remove(contents[index + 1])
    return contents


if __name__ == "__main__":
    with open('test.csv', 'w+', newline='') as csv_test:
        # html_page = '{}_page.html'.format(datetime.now())  # 更替html文件
        html_page_path = './first_page.html'
        if os.path.exists(html_page_path):
            root = get_root_html(html_page_path)
            titles = get_titles(root)
            urls = get_urls(root)
            contents = get_contents(root)
            viewed_numbers = get_viewed_numbers(root)
            raw_writein = list(zip(titles, contents, viewed_numbers, urls))
            writer = csv.writer(csv_test)
            writer.writerow(raw_writein)
        else:
            pass
