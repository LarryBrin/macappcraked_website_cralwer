from urllib.parse import urljoin

from the_zero_page import main

import math

base_url = 'http://nmac.to/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/65.0.3311.3 Safari/537.36'}


def start_url(page_number):
    return urljoin(base_url, 'page/' + str(page_number))


def judge_page_whether_crawledd(home_page):
    if all_crawled:
        # compulate_the_start_page
    if partly_crawled:
        # crawl_the_items_which_have_not_been_crawled
        # compulate_the_start_page
    if all_uncrawled:
        # crawl_the_whole_home_page
        # judge_page_whether_crawledd(next_page)


def all_crawled(*args):
    # all items' title_is_identical and version_is_identical

def partly_crawled(*args):
    # partly items' title_is_identical or `version_is_identical`
    if title_is_identical and version_is_bigger:
        # crawl
    if title_is_fifferent:
        # crawl

def all_uncrawled(*args):
    if last_item_title_fifferent or last_item_version_bigger:
        # crawl

def compulate_the_start_page(*args):
    # home_page_items_number
    # have_been_crawed_items_number
    page_number = math.ceil(have_been_crawed_items_number /
                            home_page_items_number)
