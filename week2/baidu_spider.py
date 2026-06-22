import requests
from bs4 import BeautifulSoup
from db_helper import MySQLHelper

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
resp = requests.get('https://top.baidu.com/board?tab=realtime', headers=headers)
resp.encoding = 'utf-8'
soup = BeautifulSoup(resp.text, 'html.parser')

hot_list = []
for div in soup.find_all('div', class_=lambda c: c and 'category-wrap' in c):
    title_tag = div.find('div', class_=lambda c: c and 'ellipsis' in c)
    score_tag = div.find('div', class_=lambda c: c and ('hot' in c.lower() or 'index' in c.lower()))
    if title_tag:
        title = title_tag.get_text(strip=True)
        score = score_tag.get_text(strip=True) if score_tag else '未知'
        hot_list.append((title, score))
    if len(hot_list) >= 10:
        break

print(f'抓到 {len(hot_list)} 条热搜')

if hot_list:
    db = MySQLHelper()
    db.execute('''CREATE TABLE IF NOT EXISTS baidu_hot (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(200),
        hot_score VARCHAR(50),
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    db.execute('TRUNCATE TABLE baidu_hot')   # <--- 新增这一行
    for title, score in hot_list:
        db.execute('INSERT INTO baidu_hot (title, hot_score) VALUES (%s, %s)', (title, score))
    db.close()
    print('百度热搜入库成功')