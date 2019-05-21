import time
from bs4 import BeautifulSoup
from selenium import webdriver 
from typing import List, Dict

def collect(users: List[str], limit: int) -> dict:
    """
    Collects analytics on an user' recent acvitvity

    :param users: list of usernames
    :param limit: upper limit on how many posts crawler collects defaults to 100 posts
    """
    post_analytics = {}
    for user in users:
        post_url = "https://reddit.com/user/{}/posts".format(user)
        post_analytics[user] = parse_posts(post_url, limit)
    return post_analytics

def parse_posts(url: str, limit: int) -> dict:
    """
    Collects user post history

    :param url: url to user posts
    :param limit: upper bound on how many posts to collect
    """
    posts_per_page = 17 
    page_html = process_page(url, limit//posts_per_page + 1)
    parsed = BeautifulSoup(page_html, 'html.parser')
    rs, c = {}, 0
    for _, link in enumerate(parsed.select('a')):
        if link.has_attr('data-click-id') and link['data-click-id'] == 'subreddit':
            r, c = link.text, c+1
            rs[r] = 1 if r not in rs else rs[r]+1
            if c >= limit:
                break
    rs["total"] = c
    return rs
    
def process_page(url: str, scrolls: int):
    """
    Process the page and returns source code

    :param url: page url
    :param scrolls: number of time to scroll to bottom (for infinite scroll pages) 
    """
    scroll_script = "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;return lenOfPage;"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    lenOfPage = 0
    match = False
    while(not match and scrolls > 0):
        lastCount = lenOfPage
        lenOfPage = browser.execute_script(scroll_script)
        match, srolls = lastCount == lenOfPage, scrolls-1
    return browser.page_source