# CWD_crawl_animation

# 項目:新北市新莊區未來2天天氣預報
功能說明:

	透過中央氣象局，**API串聯數據庫**抓取資料，進行**資料持久性儲存並且自動更新**，
	使用jupyter notebook處理數據，最後進行**每日更新並可視化動態顯示**。
	
1.數據來源:
	中央氣象局，API串聯數據庫:
  
	https://opendata.cwb.gov.tw/dist/opendata-swagger.html#/%E8%A7%80%E6%B8%AC/get_v1_rest_datastore_O_A0017_001

2. 使用工具:

        Spyder、requests、MySQL、jupyter notebook、numpy、pandas、matplotlib
	
---------------------------------------------------------------------------------------------------------------------------------------
項目分析:

1.獲取API資料

    1.連接中央氣象局API擷取數據庫，填寫選項，獲取新北市未來2天天氣預報 API的URL。
  
      Authorization 授權碼 ->> xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      
      format 回傳資料格式 ->> json
      
      sort 同時對 startTime、endTime 做升冪排序  ->> time
	
2.使用requests.get返回json格式檔案，解析json資料。
            
    新北市新莊區URL:

    https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-069?Authorization=CWB-601FC73E-EE68-45D5-9076-E8BECE278671&format=JSON&locationName=%E6%96%B0%E8%8E%8A%E5%8D%80&sort=time
  
    1.使用字典儲存資訊:{"columns":"value"} 
      
    2.將訊息處理成 {"columns":"value"}格式
      
	4.dataTime取值只取 starTime或dataTime(都是3小時一個循環)
     
    5.將PoP6h值拆分，6小時拆分成3小時(2個值一樣)
      
    6.儲存MySQL數據庫
		
	
3.MySQL 數據儲存

	天氣預報因子 data表 (*號要做篩選)
		id varchar(32) primary key auto_increment 
		dataTime         時間			datetime    
		AT		 體感溫度(攝氏)		varchar(5)	
		Td		 露點溫度(攝氏)		varchar(5) 
		T		 實際溫度(攝氏)		varchar(5) 
		*WX		 天氣狀況代號		varchar(12)  (08 -> 短暫陣雨or短暫雨)  
		RH		 相對濕度(百分比)	varchar(5) 
		*CI		 舒適度指數		varchar(5) 
		*WS 	         風速 公尺/秒		varchar(5) 
		WD	 	 風向描述		varchar(10) 
		*PoP3h	         降雨機率(百分比)	varchar(5)  
----------------------------------------------------------------------------------------------------------------------------------------
4. 資料處理以及資料可視化並且動態更新，最後匯聚成py檔讓windows工作排程器自動執行。
    
        1.使用**drop_duplicates對重複數據進行去重**。
        2.判斷以datetime.now()獲取目前時間，判斷數據抓取時段範圍是**當前時段加24小時(timedelta(hours=24))**。
        3.型態轉換，時間、天氣狀況、風向描述不轉換型態，其他轉為int。
        4.舒適度指數的分組。
        5.製作圖表
        
	
			

----------------------------------------------------------------------------------------------------------------------------------------
5.爬蟲程式定期執行

----------------------------------------------------------------------------------------------------------------------------------------


