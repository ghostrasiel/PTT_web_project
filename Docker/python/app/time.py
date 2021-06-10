import time
import os

file = os.path.dirname(os.path.realpath(__file__))

while True :
    time.sleep(600)
    os.system(f"python {file}/ETL_ptt/ETL_python.py") #執行外部指令 /ETL_ptt/ETL_python.py
    t = time.strftime('%H:%M:%S' , time.localtime())
    print(t)
    