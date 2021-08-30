# PTT_web_project
快速瀏覽PTT文章內容標籤及推噓人數
## 專案流程
<img width="942" alt="截圖 2021-06-06 19 01 05" src="https://user-images.githubusercontent.com/58453878/131379915-b536714b-33a1-43f2-9774-7b82692e72c5.png">
## 專案製作過程
1. 製作爬取python PTT網站 , 在爬取時就做資料清洗，並用jieba做文章標籤(八卦版 , 股版)(如要新增別的版要在mysql添加資料表)  
2. 將乾淨資料輸入至mysql   
3. 撰寫mysql API供網頁查詢  
4. 撰寫Flask以及css版型  
5. 撰寫Docker-compose快速安裝環境  

<br>
2021/06/30 update   
更新網站後台功能 , 讓網站管理員可以透過網站後台就更新資料  
![image](https://user-images.githubusercontent.com/58453878/131380945-0033f4c6-f59c-43fb-8a7f-20569b9de421.png)

