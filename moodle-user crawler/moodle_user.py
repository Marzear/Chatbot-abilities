import requests
import getpass
from lxml import html
from bs4 import BeautifulSoup

session = requests.Session()
USER = 'B10630040'
PASSWORD = getpass.getpass("請輸入密碼：")
LOGIN_URL = 'https://moodle.ntust.edu.tw/login/'

post_data = {'username': USER, 'password': PASSWORD}

html_post = session.post(LOGIN_URL, post_data)

class_id = str(input('請問您想查詢的課程代碼是：').upper())

soup = BeautifulSoup(html_post.text, 'html.parser')

for i in soup.find_all('a', href=True):
    if class_id in str(i.string):
        print("查詢課程：" , i.string)
        class_url = i['href']

try: 
    class_url = class_url.replace("course", "user")
    class_url = class_url.replace("view", "index")
    class_url += "&perpage=5000"

    new_request = session.post(class_url, post_data)
    soup = BeautifulSoup(new_request.text, 'html.parser')
    user_list = []
    for i in soup.find_all('a'):
        if '@ ' in str(i.string) and '老師' not in str(i.string):
            user_list.append(i.string.replace('@', ' '))
    user_list.sort()
    print(*user_list, sep = '\n')
except:
    print("您的輸入有誤，或是權限不足！！")