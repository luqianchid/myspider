from multiprocessing import Pool
import time
import requests
from lxml import etree
# import pymysql

headers = {
    'cookie': '__cfduid=d8cb6a574001881eb90ae8eeaae3658981561645074; UM_distinctid=16b994cdd4cb2-0e3ede7b093eaa-6353160-144000-16b994cdd4d1cc; CNZZDATA1261736110=419637929-1561642102-https%253A%252F%252Fwww.baidu.com%252F%7C1561642102; Hm_lvt_5ee23c2731c7127c7ad800272fdd85ba=1561645081,1561645095,1561645122; Hm_lpvt_5ee23c2731c7127c7ad800272fdd85ba=1561645122; cscpvrich7919_fidx=2',
    'referer': 'https://www.qu.la/book/122471/',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
# words = {'一':1,    '二':2,    '三':3,    '四':4,    '五':5,    '六':6,    '七':7,    '八':8,    '九':9,   '十':10 }
# CONN = pymysql.connect('localhost','root','root','ceshi')
# CURSOR = CONN.cursor()
F = open('D:/pythonlearn/qinli.txt','a+',encoding="GBK")

# def chinese2dit(word):
#     wordlist = list(word)
#     if wordlist[1] == '十' and len(wordlist)==2:
#         return words[wordlist[0]]*10
#     elif wordlist[0] == '十' and len(wordlist) == 2:
#         return 10 + words[wordlist[1]]
#     elif wordlist[1] == '百' and len(wordlist) == 2:
#         return words[wordlist[0]]*100
#     elif len(wordlist) == 5:
#         return words[wordlist[0]]*100+words[wordlist[2]]*10+words[wordlist[4]]
#     elif len(wordlist) == 4:
#         return words[wordlist[0]]*100+words[wordlist[2]]*10
#     elif len(wordlist) == 3:
#         return words[wordlist[0]]*10+words[wordlist[2]]
#     elif len(wordlist) == 1:
#         return words[wordlist[0]]

# def insert_into_sql(para,title,cont,time):
#     sql = "insert into wiki_doc2(para,title,content,createtime)values('%s','%s','%s','%d')" % (para,title,cont,time)
#     try:
#         CURSOR.execute(sql)
#         CONN.commit()
#         print('插入%s条数据'% title)
#     except Exception as e:
#         raise e


def getcont(url):
    resp = requests.get(url,headers=headers).content
    html = etree.HTML(resp)
    title = html.xpath('//h1/text()')[0]
    # para = title.split(' ')[0].replace('第','').replace('章', '')
    # para = chinese2dit(para)
    cont = html.xpath('//div[@id="content"]/text()')
    text = ""
    for i in cont:
        text += i.replace("'",'').replace("\u3000",'').replace('\xa0','')
    # insert_into_sql(para,title,text,time.time())
    F.write('%s\n%s' % (title,text))
    print('%s写入成功'%title)

def parse_url():
    url = "https://www.qu.la/book/61524/"
    domain = "https://www.qu.la"
    pools = Pool(processes=20)
    resp = requests.get(url,headers=headers).content
    html = etree.HTML(resp)
    urls = html.xpath('//dd/a/@href')
    for i in urls[12:]:
        u = domain + i
        try:
            pools.apply_async(getcont,(u,))
        except Exception as e:
            raise e     
    pools.close()
    pools.join()

if __name__ == "__main__":
    start = time.time()
    parse_url()    
    # CONN.close()
    F.close()
    end = time.time()
    print('==============%s==========='% '下载完成')
    print('total:%.2fs'%(end-start))