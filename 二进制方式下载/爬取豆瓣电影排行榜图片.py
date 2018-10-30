import urllib.request
import re

def request(url):
	headers = {
	"User-Agnet":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
	}
	req = urllib.request.Request(url,headers=headers)
	respon = urllib.request.urlopen(req)
	htmldata = respon.read().decode("utf-8")
	return htmldata

def regular(expression,htmldata):
	rejock = re.compile(expression)
	urldata = rejock.findall(htmldata)
	return urldata

#使用二进制读取写入方式下载文件
def download(urldata,path):
	a = 0
	for i in urldata:
		a = a + 1
		headers = {
		"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"
		}
		req = urllib.request.Request(i,headers=headers)
		respon = urllib.request.urlopen(req)
		data = respon.read()
		imagespath = path + "/%s.jpg" %(a)
		with open(imagespath,"wb") as f:
			f.write(data)

def images(url,expression,path):
	htmldata = request(url)
	urldata = regular(expression,htmldata)
	download(urldata,path)

expression = "http[a-z0-9./:_]+jpg"
url = "https://movie.douban.com/chart"
path = r"D:\BaiduBrowser\aaa"
#url = "https://www.80s.tw/"
images(url,expression,path)