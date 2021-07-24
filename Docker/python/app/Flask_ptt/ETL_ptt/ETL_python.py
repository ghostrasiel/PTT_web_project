import requests
from bs4 import BeautifulSoup
import re
import jieba
import time
import os
import random
import pymysql
import sys

file = os.path.dirname(os.path.realpath(__file__)) #mac解決當前路徑問題
print(file)
notword_list = []
conninfo = {'host':'localhost' , 'port':3306,'user':'eric' , 'passwd':'123456',
'db':'pttdb','charset':'utf8mb4'}
while True: #連線機制
    try:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        break
    except:
        pass

with open(f'{file}/notword.txt' , 'r' , encoding="utf-8") as f:
    notword = f.readlines()
    for n in notword:
        notword_list.append(n.strip('\n'))

def jieba_parsing(content): #詞句分析
    jieba.load_userdict(f'{file}/mydict.txt')
    tags = jieba.cut(content)
    tag = []
    for t in list(tags):
        if len(t) > 1 and len(t)<=6:
            if re.search('([a-z]|[A-z]|[0-9]|-)', t) == None:
                if t not in notword_list:
                    tag.append(t)
    return list(set(tag))

def resget(url): #requsets and soup
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    cookies = {'over18':'1'}
    res = requests.get(url=url ,headers=headers , cookies=cookies )
    soup = BeautifulSoup(res.text , 'html.parser')
    return soup

def mysql(db,tp): #導入資料
    sql_insert = f"""
    Insert INTO ptt_{db} (id , date , post_tag , post_title , post_author ,tag , push , good , bad ,url)
    Values (%s , %s ,%s , %s , %s ,%s , %s,%s,%s,%s);
    """
    cursor.executemany(sql_insert , tp)
    print('OK')
    conn.commit()


try:
    PTT = ['Stock' , 'Gossiping']
    # PTT = ['Stock']
    for P in PTT :
        page_url = f'https://www.ptt.cc/bbs/{P}/index.html'
        select_maxid = f'select max(id) from ptt_{P};' #查詢id編碼到哪
        cursor.execute(select_maxid)
        maxid = cursor.fetchall()
        post_id = maxid[0][0]
        if post_id == None:
            post_id = 0

        SQL_list = []
        for i in range(3): #-----------------爬取頁數------------------------
            print(i)
            soup = resget(page_url)
            posts =soup.select('div.r-list-container div.r-ent')
            for post in posts :
                try:
                    post_title = post.select('a')[0].text
                    post_url = 'https://www.ptt.cc'+ post.select('a')[0]['href']
                    post_tag = re.search('\[.+\]', post_title).group()

                    post_title = re.sub('\[.+\]\s+', '', post_title)
                    select_title = f"select post_title from ptt_{P} where post_title = '{post_title}';"
                    cursor.execute(select_title)
                    sql_title = cursor.fetchone()
                    if sql_title != None:    #查詢有無重複文章
                        break 
                    post_soup = resget(post_url)
                    post_author = post_soup.select('span.article-meta-value')[0].text
                    post_time = post_soup.select('span.article-meta-value')[3].text
                    post_time = time.strftime('%Y-%m-%d',time.strptime(post_time ,"%a %b  %d  %H:%M:%S %Y"))
                    post_conant = post_soup.select('div#main-content')[0].text
                    post_conant = re.split('20[0-9][0-9]', post_conant)[1].split('※ 發信站')[0]
                    conant_tag = jieba_parsing(post_conant)
                    conant_tag_list = []
                    for a in range(3):
                        r = random.randint(0, len(conant_tag))
                        conant_tag_list.append('#'+conant_tag[r])
                        conant_tag.pop(r)
                    conant_tag_list = ' '.join(conant_tag_list)
                    post_pushs = post_soup.select('div.push')
                    
                    good =0 ;bad = 0 ;push = 0
                    for post_push in post_pushs:
                        push += 1
                        if  '推' in post_push.select('span')[0].text:
                            good += 1
                        elif '噓' in post_push.select('span')[0].text:
                            bad +=1
                    post_id +=1
                    SQL_turple=(post_id , post_time , post_tag,post_title , post_author , conant_tag_list , push , good , bad ,post_url)
                    SQL_list.append(SQL_turple)
                    # print('id:',post_id)
                    # print('時間:',post_time)
                    # print('文章標籤:',post_tag)
                    # print('文章標題:',post_title)
                    # print('作者:',post_author)
                    # print('文章標記:',conant_tag_list)
                    # print('回文數:',push)
                    # print('推:',good , ' 噓:',bad)
                    # print('url:',post_url)
                    print(SQL_turple)
                    print('---------')
                    time.sleep(random.randint(0, 2 ))
                except IndexError :
                    print('水桶文章')
                    time.sleep(random.randint(0, 2 ))
                except AttributeError :
                    print('刪除文章')
                    time.sleep(random.randint(0, 2 ))
            page_url = 'https://www.ptt.cc'+soup.select('a.btn.wide')[1]['href']
        mysql(P, SQL_list)
except :
    print(sys.exc_info())
    pass
finally:
    cursor.close()
    conn.close()
    print('OK! good')