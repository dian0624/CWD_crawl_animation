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

4. 資料處理以及資料可視化並且動態更新，最後匯聚成py檔讓windows工作排程器自動執行。
    
     1.使用**drop_duplicates對重複數據進行去重**。
     
     2.判斷以datetime.now()獲取目前時間，判斷數據抓取時段範圍是**當前時段加24小時(timedelta(hours=24))**。
     
     3.型態轉換，時間、天氣狀況、風向描述不轉換型態，其他轉為int。
	
     4.舒適度指數的分組。
	
     5.製作圖表
	
	1. **創建日期格式方法，定義圖表x軸格式**
	
		使用**pd.Timedelta和pd.date_range做x軸的範圍縮放以及設定3小時為間隔**，設定**major主刻度格式、autofmt_xdate自動格式化顯示**。
		
	2. **創建早晚時段區分方法**
	
		透過時間區段的判斷與加減，作為**fill_between**參數的調整，設定早上為紅色，晚上為藍色。
		
	3. 創建y軸範圍設定方法
	
		以傳入列標籤名稱返回的y軸最大值與最小值正負4為y軸區間。
		
	4. 創建圖片保存方法
	
		傳入圖片標題名稱，以當前時間到結束時間作為字串拼接成圖片標題名稱。
		
	5. **未來兩天「體感溫度」圖**
	
		特別設置**text標示點y值利用bbox設定文字背景**，以及畫製**點到x軸虛線**方便查看。
		
	![image](https://github.com/dian0624/CWD_crawl_animation/blob/master/CWD_github_image/1585192954278.jpg)
		
	6. **未來兩天「體感溫度」與「降雨機率」圖**
	
		使用**subplot2grid**同一視窗畫製2張圖表並制定子圖不同大小，為子圖共同設定一個標題。
		
	![image](https://github.com/dian0624/CWD_crawl_animation/blob/master/CWD_github_image/1585192978017.jpg)
		
	7. **未來兩天 天氣概況**
	
		使用**subplot2grid**同一視窗畫製3張圖表並制定子圖不同大小，為子圖共同設定一個標題，圖表內容「體感溫度」、「相對溼度」、「風速(m/s)」。
	
	![image](https://github.com/dian0624/CWD_crawl_animation/blob/master/CWD_github_image/1585192999695.jpg)

	8. **未來兩天「體感溫度」動態圖**
	
		使用**matplotlib中的animation**函式製作動態圖。
		![image](https://github.com/dian0624/CWD_crawl_animation/blob/master/CWD_github_image/%E6%96%B0%E5%8C%97%E5%B8%82-%E6%96%B0%E8%8E%8A%E5%8D%80_2020-03-27-15%E6%9C%AA%E4%BE%86%E5%85%A9%E5%A4%A9%E3%80%8C%E9%AB%94%E6%84%9F%E6%BA%AB%E5%BA%A6%E3%80%8D.gif)
	
	9. **未來兩天「體感溫度」與「降雨機率」 動態圖**
	
		使用**matplotlib中的animation**函式製作動態圖。
		![image](https://github.com/dian0624/CWD_crawl_animation/blob/master/CWD_github_image/%E6%96%B0%E5%8C%97%E5%B8%82-%E6%96%B0%E8%8E%8A%E5%8D%80_2020-03-27-15.gif)
	
5.爬蟲程式定期執行

   最後決定每次執行時只顯示**未來兩天-天氣概況圖 和 「體感溫度」與「降雨機率」動態圖**，設定.bat檔作為Windows工作排程器每3個小時一個循環執行爬蟲更新數據庫資訊與顯示圖表、動態圖(10秒後關閉)。
	
![image](https://github.com/dian0624/CWD_crawl_animation/blob/master/CWD_github_image/1585277425034.jpg)





