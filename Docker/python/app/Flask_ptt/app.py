from flask import Flask ,render_template , request
from model import sql_select
import datetime
import os

file = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__ , static_url_path='/assets',static_folder=f'{file}/assets')

@app.route('/' , methods = ['GET' , 'POST'])
def dashboard():
    method = request.method
    coulmns = [ '時間','文章標籤','文章標題','作者','文章標記','回文數','推','噓','url']
    ptt_dict={'Gossiping':'八卦版' ,'Stock':'股票版','None':'請選擇看板'}
    ptt_db =''
    post_tag=[]

    if method == 'GET':
        datas = []
        post_tag=[]
        date1 = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        date2 = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        ptt = 'None'
        tag = None
        title =''
        post_total,push_total,good_total ,bad_total = [0,0,0,0]

    if method == 'POST':
        ptt_db =request.form.get('ppt')
        ptt =ptt_dict[request.form.get('ppt')]
        date1 = request.form.get('date1')
        date2 = request.form.get('date2')

        if ptt_db != 'None': #沒有選擇時過濾
            tag=request.form.get('tag')
            title = request.form.get('title')
            datas = sql_select.select_sql(ptt_db , date1 , date2 , tag , title)[0]
            data_total = sql_select.select_sql(ptt_db , date1 , date2 , tag , title)[1][0]
            post_tag =sql_select.select_tag(ptt_db)
            post_total,push_total,good_total ,bad_total = data_total #文章,回文,推,噓總數
            if push_total == None:
                push_total = 0
            if good_total == None:
                good_total = 0
            if bad_total == None:
                bad_total = 0

        else:
            datas=[]
            post_tag=[]
            ptt = 'None'
            tag = 'None'
            title = ''
            post_total,push_total,good_total ,bad_total = [0,0,0,0]

    return render_template('/Dashboard.html' ,method = method ,coulmns=coulmns , datas = datas ,ptt =ptt,date1 = date1 ,date2=date2
    ,post_tag=post_tag ,post_total=post_total,push_total=push_total,good_total=good_total 
    ,bad_total=bad_total ,select_title = title ) 

if __name__ == '__main__':
    app.run(debug=True , host = '0.0.0.0' , port=5000)

