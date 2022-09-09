import ddddocr
import requests

ocr = ddddocr.DdddOcr(old=True)

headers = {
    'Cookie':'sensorsdata2015jssdkcross={"distinct_id":"17e49496d8ffa-039dd061c3bd6b4-5e181552-1821369-17e49496d90d47","first_id":"","props":{},"$device_id":"17e49496d8ffa-039dd061c3bd6b4-5e181552-1821369-17e49496d90d47"}; JSESSIONID=ADFDA133F72862536E9894925655AAAB; Hm_lvt_87cf2c3472ff749fe7d2282b7106e8f1=1662390785; username=2018112701; Hm_lpvt_87cf2c3472ff749fe7d2282b7106e8f1=1662390810',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
}

res = requests.get('http://jwc.swjtu.edu.cn/vatuu/GetRandomNumberToJPEG', headers=headers)

code = ocr.classification(res.content)
print(code)


search_data = {
    'setAction': 'queryStudent',
    'selectType': 'studentName',
    'keyword': '王%',
    'ranstring': code,
    'btn1': '执行查询'
}
rsp = requests.post('http://jwc.swjtu.edu.cn/vatuu/PublicInfoQueryAction', data=search_data, headers=headers)



print(rsp.text)

while len(code) != 4:
    pass
