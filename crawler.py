import requests
import json 
import sys

sys.path.append('/usr/Alexandria/')

class Reporter:
    def __init__(self):
        self.blog_path = "./blog/jyy3kblog.json"
        print("hellow class") 

    def set_question(self):
        print("set_question")
        list_status = []
        list_text = []
        list_entire = []
        for i in range(110067524330, 221916718041):
            print(i)
            print("====")
            print(str(((i-110067524330)/(221916718041-110067524330))*100) + " percent completed")
            r=requests.get("https://blog.naver.com/PostView.nhn?blogId=jyy3k&logNo=" + str(i) + "&redirect=Dlog&widgetTypeCall=true&directAccess=false")
            list_status.append(r.status_code)
            list_text.append(r.text)
            list_entire.append(r.json)
            if((i-110067524330)%100 == 0):
                with open(self.blog_path, "w+", encoding="utf-8") as handle: 
                    for element in list_text:
                        handle.write(str(element))
                list_entire = []

if __name__ == "__main__":
    reporter = Reporter()
    reporter.set_question()
    print("hellow world")
