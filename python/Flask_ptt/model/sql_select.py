import pymysql

def select_sql(db , date1 ,date2 , tag , title):
    conninfo = {'host':'localhost' , 'port':3306,'user':'eric' , 'passwd':'123456',
'db':'pttdb','charset':'utf8mb4'}
    conn = pymysql.connect(**conninfo)
    cursor = conn.cursor()
    if (tag == None) or (tag == 'None'):
        select =f"""
        select date,post_tag,post_title,post_author,tag,push,good,bad,url from ptt_{db} 
        where (date between '{date1}' and '{date2}') and ((post_title Like '%{title}%') or (post_author Like '%{title}%'))
        order by date asc ; 
        """
        select＿total =f"""
        select count(id),sum(push),sum(good),sum(bad) from ptt_{db} 
        where (date between '{date1}' and '{date2}') and ((post_title Like '%{title}%') or (post_author Like '%{title}%'))
        order by date asc ; 
        """
    elif (tag != None) or (tag != 'None'):
        select =f"""
        select date,post_tag,post_title,post_author,tag,push,good,bad,url from ptt_{db} 
        where (date between '{date1}' and '{date2}') and (post_tag = '{tag}') and ((post_title Like '%{title}%') or (post_author Like '%{title}%')) 
        order by date asc; 
        """
        select_total =f"""
        select count(id),sum(push),sum(good),sum(bad) from ptt_{db} 
        where (date between '{date1}' and '{date2}') and (post_tag = '{tag}') and ((post_title Like '%{title}%') or (post_author Like '%{title}%')) 
        order by date asc; 
        """

    cursor.execute(select)
    data = cursor.fetchall()
    cursor.execute(select_total)
    data_total = cursor.fetchall()
    cursor.close()
    conn.close()
    return data , data_total

def select_tag(db):
    conninfo = {'host':'localhost' , 'port':3306,'user':'eric' , 'passwd':'123456',
'db':'pttdb','charset':'utf8mb4'}
    conn = pymysql.connect(**conninfo)
    cursor = conn.cursor()
    select =f"""
    select distinct post_tag from ptt_{db}; 
    """
    cursor.execute(select)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

print(select_sql('Stock', '2021-06-08', '2021-06-08', None , '')[1][0])
post_total,push_total,good_total ,bad_total = select_sql('Stock', '2021-06-08', '2021-06-08', None , '')[1][0]
print(post_total)

