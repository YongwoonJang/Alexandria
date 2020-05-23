import requests
import json 
import sys

from bs4 import BeautifulSoup

sys.path.append('/usr/Alexandria/')

class Reporter:
    def __init__(self):
        self.blog_path = "./blog/"
        print("hellow class") 

    def set_question(self):
        print("set_question")
        list_status = []
        list_text = []
        list_entire = []
        #for i in range(110077139722, 110190693131):
        #print(str(((i-110067524330)/(110190693131-110067524330))*100) + " percent completed")
        
        r=requests.get("https://blog.naver.com/PostView.nhn?blogId=jyy3k&logNo=" + str(110077139722) + "&redirect=Dlog&widgetTypeCall=true&directAccess=false")

        soup = BeautifulSoup(r.text, 'html.parser')
        print(r.text)
        print(soup.span['class'])

        #print(soup.title.string)
        print("above")
        
       #  if(len(str(soup.title.string)) > 7):
       #      with open(self.blog_path+soup.title.string+"-"+str(i)+".html", "w+", encoding="utf-8") as handle: 
       #          handle.write(str(soup))

if __name__ == "__main__":
    reporter = Reporter()
    reporter.set_question()
    print("hellow world")
