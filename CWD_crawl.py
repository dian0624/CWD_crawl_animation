import requests
import pymysql

db = pymysql.connect(host="localhost",
                     user="root",
                     password="a123456",
                     port=3306,
                     database="cwddb2",
                     charset="utf8")
cur = db.cursor()

#獲取時間
def get_dataTime(titles, weatherElement,target):
    if titles ==  target:
        times = weatherElement["time"]
        for time in times:
            #每一段時間
            time_dict = {"datatime":time["dataTime"]}
            for key, value in time_dict.items():
                if key not in dataDic:
                    dataDic[key] = []
                dataDic[key].append(value)
#獲取值
def get_value(titles, Element,target):
    if titles ==  target:
        time_list = Element["time"]
        for time in time_list:
            elementValue_list = time["elementValue"]
            for elementValue in elementValue_list:
#               #各標籤對應的所有值
                dicts = {target:elementValue["value"]}
                for key, value in dicts.items():
                    if key not in dataDic:
                        dataDic[key] = []
                    if key == "PoP6h":
                        dataDic[key].append(value)     
                    dataDic[key].append(value)                 
                    
res = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-069?Authorization=CWB-601FC73E-EE68-45D5-9076-E8BECE278671&format=JSON&locationName=%E6%96%B0%E8%8E%8A%E5%8D%80&sort=time')
data = res.json()

location_list = data['records']["locations"]
#存儲天氣資料
dataDic = {}
columns = ["Wx","AT","T","RH","WS","WD","Td","CI","PoP6h"]
erros = ["Wx","CI","WS"]

for location in location_list:
    Element_list = location["location"]
    for Element in Element_list:
        Element_list = Element["weatherElement"]
        for Element in Element_list:
            #各個標籤 PoP12h......
            titles = Element["elementName"]
            #獲取時間
            get_dataTime(titles, Element,"AT")
            #獲取值
            for column in columns:
                 get_value(titles,Element, column)
#處理異常值
for erro in erros :
    CI_values = dataDic.pop(erro)
    dataDic[erro] = []
    size = len(dataDic["datatime"]) *2
    for i in range(0,size,2):
        dataDic[erro].append(CI_values[i])

ins = "insert into data(時間,實際溫度,體感溫度,露點溫度,相對溼度,降雨機率,風向描述,天氣狀況,舒適度指數,風速)\
        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
L = [] #裡面是元組型態（"","",""...)
tuple_list = zip(dataDic["datatime"],dataDic["T"],dataDic["AT"],dataDic["Td"],
                 dataDic["RH"],dataDic["PoP6h"],dataDic["WD"],dataDic["Wx"],
                 dataDic["CI"],dataDic["WS"])  
for i in tuple_list:
    L.append(i)

for i in L:
    print(i)
    cur.execute(ins,i)
    db.commit()
    print("寫入成功")

cur.close()
db.close()

