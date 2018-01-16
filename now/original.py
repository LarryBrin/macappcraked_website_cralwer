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
    from lxml.html import fromstring
    with open('html_file', 'r') as source:
        return fromstring(source.read())


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


def first_download_url(root):
    return root.xpath('//p/a[text()=" Sendit.cloud"]/@href')


def final_download_url(root):
    return root.xpath('//div/a/@href')


if __name__ == '__main__':
    start_url = 'https://nmac.to/download/aHR0cHM6Ly9zZW5kaXQuY2xvdWQ'
    'vbWJpN3RlNWZsNGRiL25tYWMudG9fcGNsaXAxNTgxLnppcA=='
    r = response(start_url)
    print(r.encoding)
    with open('../pages_sources/test_page.html', 'w+', encoding='UTF-8') as f:
        f.write(r.text)
