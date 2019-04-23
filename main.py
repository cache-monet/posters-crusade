import time
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# Map of subreddits and number of posts

def user_analytics(user_name: str, limit: int = 100):
    """
    Collects analytics on an user' recent acvitvity
    """
    usr = "https://reddit.com/user/{}".format(user_name)

    # post analytics
    posts = parse_posts(usr + "/posts/", limit)
    total_posts = 0
    for r, p in posts.items():
        print("{} posts in in {}".format(p, r))
        total_posts += p
    print(sum)

    # comments analytics
    # comments = parse_comments(usr + "/comments/", limit)
    # total_comments = 0
    # for r, c in comments.items():
    #     print("{} comments in in {}".format(c, r))
    
def parse_comments(url: str, limit) -> dict:
    """
    Collects user comment history
    """

def parse_posts(url: str, limit: int) -> dict:
    """
    Collects user post history
    """
    scroll = "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;return lenOfPage;"

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    lenOfPage, posts = 0, 0
    match = False
    while(not match and posts < limit):
        lastCount = lenOfPage
        time.sleep(0.5)
        lenOfPage = browser.execute_script(scroll)
        match, posts = lastCount == lenOfPage, posts+15

    parsed = BeautifulSoup(browser.page_source, 'html.parser')
    rs, c = {}, 0
    for _, link in enumerate(parsed.select('a')):
        if link.has_attr('data-click-id') and link['data-click-id'] == 'subreddit':
            r, c = link.text, c+1
            rs[r] = 1 if r not in rs else rs[r]+1
            if c >= limit: return rs
    return rs
    
user_analytics('skiing2022')
