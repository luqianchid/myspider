import requests
from lxml import etree
import time
from pypinyin import lazy_pinyin
import pymysql
from multiprocessing import Pool

headers = {
  'Cookie': 'identity_id=5011365580505284; UM_distinctid=16b73fbd4211d-07f37883d979f5-39395704-1fa400-16b73fbd422463; hd_uid=3894285811561019012; _ga=GA1.2.239434776.1561019013; __gads=ID=05cae50d9a01f9fa:T=1561100830:S=ALNI_MbTw8W37QFNxNfWsdacMAJXwS8Lqw; CNZZDATA1260070928=882088203-1561017692-null%7C1561426152; __ft_57e9dc04e6563e1eda316de3=1561426569; hd_firstaccessurl=http://www.baike.com/; JSESSIONID=aaaUck0tsYlWj534ggCRw; _gid=GA1.2.1755218758.1561426570; _frome_source_=zz_page; base_domain_9e55c6b25c7f4a69b71f3ddf422c5380=baike.com; nextURL=http%3A%2F%2Fpassport.baike.com%2Flogout.do%3Ffrom%3Dadsbaike%26tag%3Dsec; _xbkService_=http%3A%2F%2Fwww.baike.com%2F; xnsetting_9e55c6b25c7f4a69b71f3ddf422c5380=%7B%22connectState%22%3A2%2C%22oneLineStorySetting%22%3A3%2C%22shortStorySetting%22%3A3%2C%22shareAuth%22%3Anull%7D; hduser=73-99-86-112-65-86-71-100-51-44-65-71-82-80-88-85-86-49-85-85-74-81-89-71-56-72-90-49-82-84-82-87-120-89-81-70-78-114-99-119-86-107-81-48-108-71-100-69-100-67-86-72-66-120-68-71-57-79-85-107-120-119-87-70-53-84-97-88-81-; ssr_sid=h70GLHFb99b1k41A; hduser_stat=MzAwNTc2NTE1OTM3OzIxMC4yMi43My4yMDI7MjAxOS0wNi0yNSAwOTo0Nzo0NA%3D%3D; ssr_auth=0dcbABzl7retYKeqOGU94f482gnyX0tQxtEZMiE2NVfVqRfvHKmgA29W%2FfBN8bNtSjmCC7bQFjieCWiU9i5PgWPoh4r2HNllQws; __utma=175268785.239434776.1561019013.1561427267.1561427267.1; __utmc=175268785; __utmz=175268785.1561427267.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __cn_57e9dc04e6563e1eda316de3=6; __utmb=175268785.5.10.1561427267; hd_referer=http://localhost:1050/index.php?admin_hdapi-down; __ft_57fc5af7e6563e06513f79c1=1561427954; __cn_57fc5af7e6563e06513f79c1=2',
  'Host': 'www.baike.com',
  'Referer': 'http://fenlei.baike.com/%E7%BE%8E%E5%9B%BD%E5%86%9B%E4%BA%8B%E4%BA%BA%E7%89%A9/list/',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Cache-Control':'max-age=0',
  'Connection': 'keep-alive'
}

conn = pymysql.connect('localhost','root','root','ceshi')
  #创建游标对象
cursor = conn.cursor()

def getletter(title):
  return list(lazy_pinyin(title)[0])[0].lower()

def insert_into_sql(values):
  timenow = time.time()
  #连接数据库
  sql = """insert into wiki_doc(cid,letter,title,tag,summary,content,author,authorid,time,lastedit,lasteditor,lasteditorid,views,edits,editions,comments,votes,visible,locked)
          values
          (%d,'%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s',%d,%d,%d,%d,%d,%d,%d,%d) """ % (0,values[0],values[1],values[2],values[3],values[4], 'admin',1,timenow,timenow,'admin',1,0,0,0,0,0,1,0)
  #执行插入语句
  try:
    cursor.execute(sql)
    conn.commit()
    print(values[1] + '插入成功')
  except Exception as e:
    print(values[1] + '插入异常')
  timeend = time.time()
  print('耗时：%.2fs'% (timeend-timenow))


def spider(url,title):
  
  resp = requests.get(url,headers = headers).text
  html = etree.HTML(resp)
  letter =  getletter(title)
  cont = html.xpath('//div[@id="content"]')[0]
  cont_text = cont.xpath('string(.)').strip().replace('编辑','\n').replace('""','')
  tags = html.xpath('//dd[@class="h27"]/a/text()')
  tag = ''
  for i in tags:
    tag = tag + i + ';'
  summary = html.xpath('//div[@class="summary"]/p')[0]
  summary_text = summary.xpath('string(.)').strip()
  values = [letter,title,tag,summary_text,cont_text]
  insert_into_sql(values)

def start_spider():
  pools = Pool(processes=20)
  with open('D:/name.txt','r',encoding="utf-8") as f:
    name = f.readlines()
    for i in name:
      try:
        url = "http://www.baike.com/wiki/%s" % i
        p = pools.apply_async(spider, (url,i,))
      except Exception as e:
        print("解析失败")
        print(e)
    pools.close()
    pools.join()
  print('='*20)

if __name__ == "__main__":
  start = time.time()
  start_spider()
  end = time.time()
  conn.close()
  print('total:%.2fs'%(end-start))