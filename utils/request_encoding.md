import requests 를 사용하여 한글을 다룰때의 문제 해결 방법

requests 에서 웹 페이지를 가져오면 아래 순서로 진행한다.

1. Web에서 Response 객체로 데이터를 담는다.
   1.  requests 모듈에서 자동으로 인코딩할 정보를 지정한다.   
   1.  Response 객체는 1.에서 저장한 인코딩 정보를 사용하여 데이터를 담는다.   
1. encoding 속성을 사용하여 저장된 text를 가져온다. 

따라서 다음과 같이 진행해 주어야 한다. 

```python
import requests
res = requests.get('URL')
res.encoding = None
```

이 효과는 Crwaling한 Web page 에서 ISO-8859-1을 사용했을 때, Crawling 결과가 깨질 경우에 유용하다. 
