#爬取80s网站电影，并调用迅雷下载
#后台需要搭建一个redis数据库
import urllib.request
import os,re
import redis

#发起爬取网页请求
def request(url):
	headers = {
	"User-Agnet":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
	}
	req = urllib.request.Request(url,headers=headers)
	respon = urllib.request.urlopen(req)
	htmldata = respon.read().decode("utf-8")
	return htmldata

#使用正则匹配url网址
def regular(expression,htmldata):
	rejock = re.compile(expression)
	urldata = rejock.findall(htmldata)
	return urldata

#调用迅雷下载器
def download(downurl):
	os.chdir(r"D:\xunlei\Program")
	os.system("Thunder.exe %s" %(downurl))

#查找网址是否已在数据库中
def redisget(url):
	r = redis.StrictRedis(host="localhost",port="6379",password="sunck")
	return r.exists(url)

#将爬取过的网址存在数据库中
def redisset(url):
	r = redis.StrictRedis(host="localhost",port="6379",password="sunck")
	r.set(url,"1")

#使用递归函数，深度爬取
def run(url):
	key = redisget(url)
	if not key:
		htmldata = request(url)
		downurl = regular("thunderHref=\"(.*?)\"",htmldata)
		httpurl = regular("<a href=\"(.*?)\"",htmldata)
		redisset(url)
		if downurl:
				download(downurl[0])
		if httpurl:
			for h in httpurl:
				if h != "/":
					t = regular("http",h)
					if not t:
						run("https://www.80s.tw%s" %(h))

#执行爬取脚本
if __name__ == "__main__":
	url = "https://www.80s.tw"
	run(url)