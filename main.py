import socket,json
from requests import *
import random
import time
import pymysql
import json
import requests
from email.mime.text import MIMEText
from email.header import Header
import atexit
from PIL import Image
import os
import qrcode
from pyzbar.pyzbar import decode
quitlist=[]
sendlist=[]
gamelist=[]
path=os.path.dirname(os.path.abspath(__file__))
Alphabet={'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15}
def pt():
    with open('log.txt','w') as f:
        f.write(time.strftime("%Y%m%d%H%M",time.localtime()))
        f.close()
atexit.register(pt)
BotID=1053466995
headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"}
HttpResponseHeader = '''HTTP/1.1 200 OK

Content-Type: text/html

'''
conn= pymysql.connect(host='192.168.0.107',user = "korinbot",passwd = "korinbot",db = "korinbot",charset='utf8')
cur=conn.cursor(cursor=pymysql.cursors.DictCursor)
cur.execute('select * from game')
gamelist=cur.fetchall()
ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(('127.0.0.1', 5701))
ListenSocket.listen(100)
def rev_msg():
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    rev_json=request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    return rev_json
def request_to_json(msg):
   for i in range(len(msg)):
       if msg[i]=="{" and msg[-1]=="\n":
          return json.loads(msg[i:])
def gs(who,what):
    js={
        "group_id":who,
        "message":what
       }
    code=post("http://127.0.0.1:5700/send_group_msg",json=js)
def checktime(timestr):
    boo=True
    lis=timestr.split('：')
    if len(lis[0])!=4 or len(lis[1])!=2 or len(lis[2])!=2 or len(lis[3])!=2 or len(lis[4])!=2:
        boo='nt'
    try:
        times=int(''.join(lis))
        nowstr=int(time.strftime("%Y%m%d%H%M",time.localtime()))
        
        if int(lis[1])>12 or int(lis[3])>23 or int(lis[4])>59:
            boo='nt'
        if (int(lis[1])%2==0 and int(lis[1])<7) or (int(lis[1])%2!=0 and int(lis[1])>8):
            if int(lis[2])==31:
                boo='nt'
        if int(lis[1])==2 and int(lis[2])>29:
            boo='nt'
        if int(lis[0])%4!=0 or (int(lis[0])%100==0 and int(lis[0])%400!=0):
            if int(lis[2])>28 and int(lis[1])==2:
                boo='rn'
                
        if times<=nowstr:
            boo='te'
    except:
        boo='nt'
    return boo
def give_the_correct_time(t):
    global cur
    global gs
    global conn
    cur.execute('SELECT * from timesave')
    gtct=cur.fetchone()
    gtct=gtct['hour']
    now_t=int(time.strftime("%H",time.localtime()))

    if now_t!=gtct:
        with open('qun.txt','r') as f:
            ql=f.read()
            ql=ql.split(',')
            f.close()
        for i in ql:
            gs(int(i),'{0}\n现在是{1}点，Korin Bot自动报时了喵~'.format(t,now_t))
        cur.execute("update timesave set `hour`={0} where `hour`={1}".format(now_t,gtct))
        conn.commit()
def read_qr_code():
    img = Image.open('./pic/qrcode_read_data.png')
    barcodes = decode(img)
    
    urls = []
    # 图片包含多个二维码，识别成功会返回多个链接
    for barcode in barcodes:
        url = barcode.data.decode("utf-8")
        urls.append(url)
        
    return urls
def get_user_list():
    global cur
    global conn
    cur.execute("select * from user")
    user_list=cur.fetchall()
    return user_list
def reconnect():
    global conn
    conn.commit()
def clockring():
    global cur
    global conn
    global reconnect
    clocktimelist=[]
    cur.execute('select * from clock')
    clocktimelist=cur.fetchall()
    cur.execute('select * from notice')
    noticelist=cur.fetchall()
    for i in clocktimelist:
        t=int(time.strftime("%Y%m%d%H%M",time.localtime()))
        if t>=i['time']:
            cur.execute('select * from user where FIND_IN_SET({0},`uid`)'.format(i['ownerid']))
            info=cur.fetchone()
            gs(info['groupid'],'您设置的闹钟时间到啦~[CQ:at,qq={0}]'.format(i['ownerid']))
            cur.execute('delete from clock where cid={0}'.format(i['cid']))
            conn.commit()
    for i in noticelist:
        t=int(time.strftime("%Y%m%d%H%M",time.localtime()))
        if t>=i['time']:
            cur.execute('select * from user where FIND_IN_SET({0},`uid`)'.format(i['ownerid']))
            info=cur.fetchone()
            gs(info['groupid'],'来自定时提醒：{1}[CQ:at,qq={0}]'.format(i['ownerid'],i['text']))
            cur.execute('delete from notice where ID={0}'.format(i['ID']))
            conn.commit()
def ps(who,what):
    js={
        "user_id":who,
        "message":what
       }
    code=post("http://127.0.0.1:5700/send_private_msg",json=js)
def gett():
  t=int(time.strftime("%H",time.localtime()))
  if t<=4:
            t='很晚了，早点睡吧~'
  elif t<=10 and t>4:
            t='早上好！'
  elif t>10 and t<=14:
            t="日安~"
  elif t>14 and t<=16:
            t='下午好~'
  elif t>16 and t<=22:
            t='傍晚了喵~'
  elif t>22:
            t='晚上好~早睡早起身体好哦~'
  return t
def getgame(gid):
    global cur
    if gid=='':
        return False
    else:
        try:
            cur.execute('select * from game where gid={0}'.format(gid))
            game=cur.fetchall()
            if game==() or game==[]:
                raise
            else:
                game=game[0]
                return game
        except:
            return False
def stopgame(gid,info,reason,winner='no',second='no',third='no',fourth='no'):
    global cur
    global conn
    group=info['groups']
    group=group.split(',')
    group=map(int,group)
    print(info)
    if info['type']==1:
        p=2
    else:
        p=4
    try:

        if reason=='userstop':
            t='因为玩家用指令终止了这个对局'
        elif reason=='win':
            if p==2:
                t='赢家是{0}'.format(winner)

        bc('GID为{0}的游戏结束，{1}'.format(gid,t),gid)
        cur.execute('delete from game where gid={0}'.format(gid))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
def bc(text,gid):
    global getgame
    info=getgame(gid)
    group=info['groups']
    group=group.split(',')
    group=map(int,group)
    for i in group:
        gs(i,text)
def b_p(pic,gid):
    global gs
    global ps
    global bc
    bg=Image.open(path+'/pic/gobang.jpg')
    bp=Image.open(path+'/pic/black.jpg')
    wp=Image.open(path+'/pic/white.jpg')
    picl=pic.split(',')
    for i in range(len(picl)):
        picl[i]=picl[i].split('&')
        x=(int(picl[i][1])-1)*48+51
        y=(int(picl[i][2])-1)*48+51
        if picl[i][0]=='b':
            bg.paste(bp,(x,y))
        else:
            bg.paste(wp,(x,y))
    dp=path+'/data/gobangdata.jpg'
    bg.save(dp)
    
    bc("[CQ:image,file=file:///{0}]".format(dp),gid)
def coorturn(coo,who):
    try:
        if who==0:
            who='b'
        else:
            who='w'
        x=Alphabet[coo[:1]]
        y=int(coo[1:])
        return "{0}&{1}&{2}".format(who,x,y)
    except:
        return False
def gobangwin(pic,borw):
    l=pic.split(',')
    dic={}
    leftlength=0
    rightlength=0
    uplength=0
    downlength=0
    leftuplength=0
    rightdownlength=0
    leftdownlength=0
    rightuplength=0
    for i in range(len(l)):
        l[i]=l[i].split('&')
        l[i][1]=int(l[i][1])
        l[i][2]=int(l[i][2])
        k=tuple([l[i][1],l[i][2]])
        v=l[i][0]
        dic[k]=v
    j=1
    while True:
        try:
            tryvalue=dic[(k[0]-j,k[1])]
            if tryvalue==borw:
                j+=1
                leftlength+=1
            else:
                raise
        except:
            break
    j=1
    while True:
        try:
            tryvalue=dic[(k[0]+j,k[1])]
            if tryvalue==borw:
                j+=1
                rightlength+=1
            else:
                raise
        except:
            break
    j=1
    while True:
        try:
            tryvalue=dic[(k[0],k[1]-j)]
            if tryvalue==borw:
                j+=1
                uplength+=1
            else:
                raise
        except:
            break
    j=1
    while True:
        try:
            tryvalue=dic[(k[0],k[1]+j)]
            if tryvalue==borw:
                j+=1
                downlength+=1
            else:
                raise
        except:
            break
    j=1
    while True:
        try:
            tryvalue=dic[(k[0]-j,k[1]-j)]
            if tryvalue==borw:
                j+=1
                leftuplength+=1
            else:
                raise
        except:
            break
    j=1
    while True:
        try:
            tryvalue=dic[(k[0]+j,k[1]+j)]
            if tryvalue==borw:
                j+=1
                rightdownlength+=1
            else:
                raise
        except:
            break
    j=1
    while True:
        try:
            tryvalue=dic[(k[0]-j,k[1]+j)]
            if tryvalue==borw:
                j+=1
                leftdownlength+=1
            else:
                raise
        except:
            break
    j=1
    while True:
        try:
            tryvalue=dic[(k[0]+j,k[1]-j)]
            if tryvalue==borw:
                j+=1
                rightuplength+=1
            else:
                raise
        except:
            break
    if (leftlength+rightlength>=4) or (uplength+downlength>=4) or (leftuplength+rightdownlength>=4) or (leftdownlength+rightuplength>=4):
        return True
    else:
        return False

def create_qr_code(url):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    img = qr.make_image(fill_color='black', back_color='white')
    img.show()
    img.save("./pic/qrcode_make_data.png")
while True:
  rev=rev_msg()
  if rev==None:
    rev={'post_type': 'meta_event', 'meta_event_type': 'heartbeat', 'time': 1675395869, 'self_id': 1053466995, 'status': {'app_enabled': True, 'app_good': True, 'app_initialized': True, 'good': True, 'online': True, 'plugins_good': None, 'stat': {'packet_received': 2681, 'packet_sent': 2523, 'packet_lost': 0, 'message_received': 45, 'message_sent': 32, 'disconnect_times': 2, 'lost_times': 0, 'last_message_time': 1675395851}}, 'interval': 1000}
  if rev['post_type']!='meta_event':
    print(rev)
  for i in quitlist:
    js={"group_id":i}
    post('http://127.0.0.1:5700/set_group_leave',json=js)
  quitlist=[]
  for i in sendlist:
    gs(i,'你好！我是Korin Bot，一个QQBot，查看帮助请用/kb about，请多指教！')
  sendlist=[]
  if rev==None:
    rev={'post_type': 'meta_event', 'meta_event_type': 'heartbeat', 'time': 1674994167, 'self_id': 1053466995, 'status': {'app_enabled': True, 'app_good': True, 'app_initialized': True, 'good': True, 'online': True, 'plugins_good': None, 'stat': {'packet_received': 4025, 'packet_sent': 3890, 'packet_lost': 0, 'message_received': 22, 'message_sent': 47, 'disconnect_times': 0, 'lost_times': 0, 'last_message_time': 1674994101}}, 'interval': 5000}
  user_list=get_user_list()
  t=gett()
  give_the_correct_time(t)
  clockring()
  if rev['post_type']=='notice' and rev['notice_type']=='notify':
    if rev['sub_type']=='poke':
        if rev['sender_id']!=BotID and rev['target_id']==BotID:
                m=random.randint(0,2)
                gi=rev['group_id']
                if m==0:
                    gs(gi,'不要戳了呜呜呜')
                elif m==1:
                    gs(gi,'再戳就是笨蛋！')
                elif m==2:
                    gs(rev['group_id'],'[CQ:poke,qq={}]'.format(rev['user_id']))
                    gs(gi,'我也会戳！')
  if rev['post_type']=='request' and rev['request_type']=='friend':
    cur.execute('select * from rootaccount')
    ownerlist=cur.fetchall()
    loginname=rev['comment']
    loginname=loginname.split('\n')
    del loginname[0]
    del loginname[1]
    for i in range(2):
        loginname[i]=loginname[i].split(':')
        loginname[i]=loginname[i][1]
    loginpwd=loginname[1]
    loginname=loginname[0]
    for i in ownerlist:
        if loginname==i['name']:
            if loginpwd==i['password']:
                    js={"flag":rev['flag'],"approve":"true","remark":"Owner:{0}".format(loginname)}
                    code=post("http://127.0.0.1:5700/set_friend_add_request",json=js)
                    cur.execute('update rootaccount set `qq`={0} where `name`={1}'.format(rev['user_id'],i['name']))
                    conn.commit()
                    break
  if rev['post_type']=='message' and rev['message_type']=='private':
    zt=False
    cur.execute('select * from rootaccount')
    rootlist=cur.fetchall()
    for i in rootlist:
        if i['qq']==rev['sender']['user_id']:
            ra=i
            if i['qq']==2605619532:
                Administrator=True
            zt=True
    if zt:
        ms=rev['message']
        sp=rev['sender']['user_id']
        if ms=='buy':
            cur.execute('select * from user where uid={0}'.format(sp))
            info=cur.fetchone()
            if info==():
                ps(sp,'您似乎没有绑定Korin Bot Account,这是一个不应该发生的错误，请联系作者（2605619532）获取帮助')
            else:
                if info['KorinCoin']>=10:
                    cur.execute('update user set `KorinCoin`={0} where `uid`={1}'.format(info['KorinCoin']-10,info['uid']))
                    conn.commit()
                    cur.execute('update rootaccount set `times`={0} where `qq`={1}'.format(ra['times']+1,ra['qq']))
                    conn.commit()
                    ps(sp,'购买成功，您现在有调用次数共{0}次'.format(ra['times']+1))
                else:
                    ps(sp,'KorinCoin不足~要10KorinCoin才能购买一次调用次数哦~')
        elif ms=='Self Info' or ms=='self info' or ms=='selfinfo':
            ps(sp,'[Root Account Self Info]\nID：{0}\n用户名：{1}\n密码：{2}\n剩余调用次数：{3}'.format(ra['uid'],ra['name'],ra['password'],ra['times']))
        if Administrator:
            if ms=='clock':
                cur.execute("select * from clock")
                table=cur.fetchall()
                t=''
                for i in table:
                    t+='\n'
                    t+=str(i['cid'])
                    t+='  '
                    t+=str(i['time'])
                    t+='  '
                    t+=str(i['ownerid'])
                ps(sp,'Table Information\nlines:{0}\ncid time ownerid{1}'.format(len(table),t))
            elif ms=='memo':
                cur.execute("select * from memo")
                table=cur.fetchall()
                t=''
                for i in table:
                    t+='\n'
                    t+=str(i['mid'])
                    t+='  '
                    t+=str(i['text'])
                    t+='  '
                    t+=str(i['ownerid'])
                ps(sp,'Table Information\nlines:{0}\nmid text ownerid{1}'.format(len(table),t))
            elif ms=='notice':
                cur.execute("select * from notice")
                table=cur.fetchall()
                t=''
                for i in table:
                    t+='\n'
                    t+=str(i['ID'])
                    t+='  '
                    t+=str(i['time'])
                    t+='  '
                    t+=str(i['text'])
                    t+='  '
                    t+=str(i['ownerid'])
                ps(sp,'Table Information\nlines:{0}\nID time text ownerid{1}'.format(len(table),t))
            elif ms=='rootaccount':
                cur.execute("select * from rootaccount")
                table=cur.fetchall()
                t=''
                for i in table:
                    t+='\n'
                    t+=str(i['uid'])
                    t+='  '
                    t+=str(i['name'])
                    t+='  '
                    t+=str(i['password'])
                    t+='  '
                    t+=str(i['times'])
                    t+='  '
                    t+=str(i['qq'])
                ps(sp,'Table Information\nlines:{0}\nuid name password times qq{1}'.format(len(table),t))
            elif ms=='timesave':
                cur.execute("select * from timesave")
                table=cur.fetchall()
                ps(sp,'timesave:{0}'.format(table[0]['hour']))
            elif ms=='user':
                cur.execute("select * from user")
                table=cur.fetchall()
                t=''
                for i in table:
                    t+='\n'
                    t+=str(i['uid'])
                    t+='  '
                    t+=str(i['KorinCoin'])
                    t+='  '
                    t+=str(i['groupid'])
                    t+='  '
                    t+=str(i['signdate'])
                ps(sp,'Table Information\nlines:{0}\nuid KorinCoin groupid signdate{1}'.format(len(table),t))
    else:
        ps(rev['sender']['user_id'],'您的QQ账户似乎没有绑定Root Account,这意味着您无法使用除游戏指令外的私聊指令')
  if rev['post_type']=='request' and rev['request_type']=='group':
    cur.execute('select * from rootaccount where qq={0}'.format(rev['user_id']))
    use=cur.fetchone()

    if use==None:
        quitlist.append(rev['group_id'])
    elif use['times']<=0:
        quitlist.append(rev['group_id'])

    else:
        cur.execute('update rootaccount set `times`={0} where `uid`={1}'.format(use['times']-1,use['uid']))
        conn.commit()
        t=time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
        js={"flag":rev['flag'],"sub_type":rev['sub_type'],"approve":"true"}
        post("http://127.0.0.1:5700/set_group_add_request",json=js)
        ps(rev['user_id'],'您在{0}邀请了Korin Bot进入群{1}，您现在还有{2}次调用次数'.format(t,rev['group_id'],use['times']-1))
        with open ('qun.txt','a') as f:
            f.write(',{0}'.format(rev['group_id']))
            f.close()
        
        sendlist.append(rev['group_id'])
  if rev['post_type']=='message' and rev['message_type']=='group':
    b=True
    for i in user_list:
        if rev['sender']['user_id']==i['uid']:
            user=i
            b=False
    if b:
        cur.execute('insert into user values({0},0,{1},0)'.format(rev['sender']['user_id'],rev['group_id']))
        reconnect()
        get_user_list()
        user={'uid':rev['sender']['user_id'],'KorinCoin':0,'groupid':rev['group_id'],'signdate':0}
    ms=rev['message']
    gi=rev['group_id']
    try:
        msl=ms.split(']')
        if msl[1]=='/kb 10 1':
            msl=msl[0].split(',')
            msl=msl[3].split('=')
            url=msl[1]
        T= requests.get(url,headers=headers,timeout=2)
        with open('./pic/qrcode_read_data.png','wb') as f:
            f.write(T.content)
            f.close()
        text=read_qr_code()
        if text==[]:
            gs(gi,'没有读取到二维码信息，请检查图片')
        else:
            st='共读取到{0}个信息：'.format(len(text))
            for i in range(len(text)):
                st+='\n{0}.{1}'.format(i+1,text[i])
    except:
                pass
    if ms=='/kb about' or ms=='/kb help':
        gs(gi,'''你好！我是Korin Bot/科林QQ机器人
前我可以为你提供一些普通服务
1.闹钟设置
2.整点报时
3.天气查询
4.必应每日图片
5.历史上的今天
6.各类小游戏
7.今日早报
8.备忘录  
9.获取头像
10.二维码服务
请使用/kb 序号 来获取该功能的帮助
请使用/kb 序号 参数 来使用该功能
签到请使用【/kb sign】或【korin早】或【Korin早】或【korinbot早】
关于您的KorinBot账户信息请使用/korinbot获取
关于KorinBot账户帮助请使用/kb help user
关于将KorinBot加入您的群请使用/kb help join获取帮助
关于KorinCoin帮助请使用/kb help korincoin
提供反馈或建议可使用/kb b 内容，这将完全匿名
想使Korin Bot退出群聊请使用/kb quit group，不要踢！不要踢！''')
    elif ms=='/kb b' or ms=='/kb b ':
        gs(gi,'请使用/kb b 内容')
    elif ms=='/kb quit group':
        gs(gi,'正在实行退出程序，再见喵~')
        js={"group_id":gi}
        code=post('http://127.0.0.1:5700/set_group_leave',json=js)
        with open('qun.txt','r') as f:
            q=[int(i) for i in f.read().split(',')]
            del q[q.index(gi)]
            q=','.join(q)
            f.close()
        with open('qun.txt','w') as f:
            f.write(q)
            f.close()
    elif ms=='/kb help korincoin':
        gs(gi,'KorinCoin是KorinBot中的一种货币，可通过签到获得，现在的基本作用在于为Root Account购买调用次数（关于Root Account请使用/kb help join获取帮助）\n您可以在与Korin Bot的私聊信息中发送buy购买，每个调用次数的价格为10个KorinCoin\n更多功能开发中~')
    elif ms[:6]=='/kb b ' and ms[6:]!='':
        nr=ms[6:]
        a='来自反馈：'+nr
        ps(2605619532,a)
        gs(gi,'您的反馈已经发送给开发者！谢谢喵~')
    elif ms=='/korinbot':
        if user['signdate']!=int(time.strftime("%Y%m%d",time.localtime())):
            sf='今日未签到'
        else:
            sf='今日已签到'
        gs(gi,'[Self Info]\n绑定QQ号：{0}\nKorinCoin：{1}\n通知群号：{2}\n{3}'.format(user['uid'],user['KorinCoin'],user['groupid'],sf))
    elif ms=='/kb sign' or ms=='korin早' or ms=='Korin早' or ms=='korinbot早':
        cur.execute('select * from user where uid={0}'.format(user['uid']))
        zt=cur.fetchall()
        zt=zt[0]
        t=int(time.strftime("%Y%m%d",time.localtime()))
        if t!=zt['signdate']:
            cur.execute('update user set `signdate`={0} where `uid`={1}'.format(t,user['uid']))
            cur.execute('update user set `KorinCoin`={0} where `uid`={1}'.format(zt['KorinCoin']+2,user['uid']))
            conn.commit()
            gs(gi,'签到成功~')
        else:
            gs(gi,'已经签到过啦~')
    elif ms=='/kb help join':
        gs(gi,'请首先联系开发者（2605619532）以获得一个Root Account，并在添加Korin Bot为好友时正确填写UserName和Password，Korin Bot只会接受来自剩余可调用次数不为0的Root Account的入群邀请，否则将自动退出该群。您可以将Korin Bot拉入您的群内，Bot会自动检查您的Root Account并扣除您的一次调用次数，如果Korin Bot退出该群将不会返回调用次数，如果Korin Bot被踢出该群我们将永久封禁邀请者的Root Account，因为这会影响Korin Bot的风控级别，会导致不可预料的后果，所以请勿随意踢出Korin Bot，请使用/kb quit group让Korin Bot退出，谢谢喵~\n关于调用次数的获取请参阅KorinCoin帮助（/kb help korincoin)\n关于您的Root Account信息您可以在与Korin Bot的私聊中使用【Self Info】或【self info】或【selfinfo】获取')
    elif ms=='/kb help 1':
        gs(gi,'''欢迎游玩KorinBot提供的五子棋服务owo
落子：/l GID 坐标（先字母后数字） ''')
    elif ms=='/kb help user':
        gs(gi,'''我们会在您第一次使用Korin Bot时自动为您创建一个KBA（Korin Bot Account），这个KBU将自动绑定您的QQ号并使用您的QQ号作为唯一标识符。我们将会使用这个KBU来记录您设置的闹钟或备忘录，以便您能在任何地方通过Korin Bot获取您的记录。一个QQ号至多绑定一个KBU，KBU也同理。如果您需要为您的KBU或QQ更换绑定，又或是希望为我们提供反馈和建议，请联系管理员：2605619532。希望使用愉快喵~''')
    elif ms=='/kb a group ' or ms=='/kb a group':
        gs(gi,'请使用/kb a group 群号')
    elif ms[:12]=='/kb a group ' and ms[12:]!='':
        try:
            int(ms[12:])
            gs(gi,'修改成功')
            cur.execute('update user set `groupid`={0} where `uid`={1}'.format(int(ms[12:]),rev['sender']['user_id']))
            reconnect()
        except:
            gs(gi,'群号不合法')

    elif ms=='/kb 1' or ms=='/kb 1 ':
        gs(gi,'请使用/kb 1 年：月：日：小时：分（不足两位请补足两位）')
    elif ms[:6]=='/kb 1 ' and ms[6:]!='':
        t=ms[6:]
        b=checktime(t)
        if b=='nt':
            gs(gi,'时间输入不合法，请严格按照格式【年：月：日：小时：分】（不足两位请补足两位）')
        elif b=='te':
            gs(gi,'你在逗我吗？')
        elif b=='rn':
            gs(gi,'闰年相关问题导致时间非法，请检查时间是否正确。')
        else:
            cur.execute('select max(cid) from clock')
            cid=cur.fetchone()
            cid=cid['max(cid)']+1
            ts=t.split("：")
            ts=''.join(ts)
            ts=int(ts)
            cur.execute('insert into clock values({0},{1},{2})'.format(cid,ts,rev['sender']['user_id']))
            reconnect()
            gs(gi,'添加时间为{0}的闹钟成功，将在群号为{1}通知您，如要修改通知群号请使用/kb a group 群号'.format(t,rev['group_id']))
    elif ms=='/kb 2' or ms=='/kb 2 ':
        gs(gi,'Korin Bot会自动报时的喵~')
    elif ms=='/kb 3'or ms=='/kb 3 ':
        gs(gi,'请使用/kb 3 所在城市')
    elif ms[:6]=='/kb 3 ' and ms[6:]!='':
        re1=get('https://api.ooomn.com/api/weather?city={}'.format(ms[6:]))
        r=re1.json()['data']
        gs(gi,'{0}\n{1}今天{2}，最高温度{3}，最低温度{4}，空气质量{5}~\nKorin tips：{6}'.format(t,r['city'],r['wea'],r['tem_day'],r['tem_night'],r['air_level'],r['air_tips']))
    elif ms=='/kb 4' or ms=='/kb 4 ':
        gs(gi,'{0}\n今天是{1}，必应每日图片奉上~[CQ:image,file=https://api.ooomn.com/api/bing]'.format(t,time.strftime("%Y年%m月%d日",time.localtime())))
    elif ms=='/kb 5' or ms=='/kb 5 ':
        con=get('https://api.ooomn.com/api/history?format=json')
        con=con.json()
        content="\n".join(con['content'])
        gs(gi,'''{0}\n今天是{1}\n历史上今天的事件有：\n{2}'''.format(t,con['day'],"\n".join(con['content'])))
    elif ms=='/kb 6' or ms=='/kb 6 ':
        gs(gi,'''目前小游戏共有1个：
1.五子棋
我们会使用一个唯一的GID来标识一个游戏进程
您可以使用/kb 6 游戏序号来开始一个游戏，我们会等待游戏玩家全部加入后自动开始，在此之前将不能进行游戏
您可以将这个游戏序号发送给您的朋友或者让群友们参加，参加指令为/kb 6 join GID（支持跨群聊！）
您也可以用/kb 6 watch GID或/kb 6 stopwatch GID来观战或停止观战
当游戏决出胜负时会自动结束该游戏进程，您也可以使用/kb 6 stop GID来结束游戏
具体每个游戏的指令请使用/kb help 游戏序号''')
    elif ms[:11]=='/kb 6 watch':
        gid=ms[12:]
        info=getgame(gid)
        group=info['groups']
        group.split(',')
        group=set(map(int,group))
        if (gi in group):
            gs(gi,'这个群已在观战/参加中')
        else:
            cur.execute("update game set `groups`='{0}' where `gid`={1}".format(info['groups']+','+str(gi),gid))
            conn.commit()
    elif ms[:15]=='/kb 6 stopwatch':
        gid=ms[16:]
        info=getgame(gid)
        group=info['groups']
        group.split(',')
        group=set(map(int,group))
        if (gi in group):
            gs(gi,'这个群已在观战/参加中')
        else:
            t=list(group)
            t.remove(gi)
            st=','.join(t)
            
            cur.execute("update game set `groups`='{0}' where `gid`={1}".format(st,gid))
            conn.commit()
    elif ms[:5]=='/kb 6' and ms[7:]=='':
        typ=ms[6:]
        try:
            typ=int(typ)
        except:
            pass
        if typ==1:
            cur.execute("select max(gid) from game")
            gid=cur.fetchone()
            gid=gid['max(gid)']+1
            cur.execute("insert into game values({0},1,{1},0,'','','{2}',0,0)".format(gid,user['uid'],str(gi)))
            conn.commit()
            gs(gi,'[CQ:at,qq={0}]成功创建了一个GID为{1}的五子棋游戏'.format(user['uid'],gid))
    elif ms[:10]=='/kb 6 join':
        gid=ms[11:]
        info=getgame(gid)
        group=info['groups']
        group=group.split(',')
        group=set(map(int,group))
        if (gi in group):
            pass
        else:
            cur.execute("update game set `groups`='{0}' where `gid`={1}".format(info['groups']+','+str(gi),gid))
            conn.commit()
        if info['binduser2']==0:
            cur.execute("update game set `binduser2`={0} where `gid`={1}".format(rev['sender']['user_id'],gid))
            cur.execute("update game set `starttime`={0} where `gid`={1}".format(time.time(),gid))
            cur.execute("update game set `who`={0} where `gid`={1}".format(0,gid))

            conn.commit()
            gs(gi,'参加成功哦~')
            bc('用户{0}（{1}）加入了游戏（GID：{2}）'.format(rev['sender']['nickname'],user['uid'],gid),gid)
            bc('[CQ:image,file=file:///{0}]'.format(path+'/pic/gobang.jpg'),gid)
        else:
            gs(gi,'满人了ovo')
    elif ms[:10]=='/kb 6 stop':
        gid=ms[11:]
        info=getgame(gid) 
        stopgame(gid,info,'userstop')   
    elif ms=='/kb 7' or ms=='/kb 7 ':
        yd=get('http://bjb.yunwj.top/php/60miao/qq.php')
        yd=yd.json()
        yd=yd['wb']
        ydm=''
        for i in range(len(yd)-1):
            ydm+=yd[i][0]
        sms='''{0}\n今日早报：\n{1}'''.format(t,ydm)
        gs(gi,sms)
    elif ms=='/kb 8' or ms=='/kb 8 ':
        gs(gi,'''Korin Bot的备忘录具有两种形式：
1.定时提醒
这种形式的指令为/kb 8 1 时间 提醒内容（仅支持文本和emoji）
时间格式为：【年：月：日：小时：分】（不足两位请补足两位）
我们将在您设定的时间向您发送文本内容并@您

2.记录
这种形式的指令为/kb 8 2 记录内容（仅支持文本和emoji）
我们将会返回一个唯一的记录ID
您可以使用/my note查看您的所有记录（包含记录ID）
使用/note 记录ID查看指定记录
使用/delete 记录ID删除指定记录（仅支持记录创建者）''')
    elif ms=='/kb 8 1' or ms=='/kb 8 1 ':
        gs(gi,'请使用/kb 8 1 时间 提醒内容')
    elif ms[:8]=='/kb 8 1 ' and ms[8:]!='':
        try:
            noticetime=ms[8:]
            noticetime=noticetime.split(' ')
            text=noticetime[1]
            noticetime=noticetime[0]
            result=checktime(noticetime)
            if result!=True:
                raise
            noticetimestr=noticetime.split("：")
            noticetimestr=''.join(noticetimestr)
            noticetimestr=int(noticetimestr)
            cur.execute('select max(ID) from notice')
            mid=cur.fetchone()
            mid=mid['max(ID)']+1
            cur.execute("insert into notice values({0},{1},'{2}',{3})".format(mid,noticetimestr,text,user['uid']))
            conn.commit()
            gs(gi,'设定完毕')
        except Exception as e:
            gs(gi,'发生错误，请检查输入')
    elif ms=='/kb 8 2' or ms=='/kb 8 2 ':
        gs(gi,'请使用/kb 8 2 记录文本')
    elif ms[:8]=='/kb 8 2 ' and ms[8:]!='':
        text=ms[8:]
        cur.execute('select max(mid) from memo')
        mid=cur.fetchone()
        mid=mid['max(mid)']+1
        cur.execute("insert into memo values({0},'{1}',{2})".format(mid,text,user['uid']))
        conn.commit()
        gs(gi,'设定完毕，这条记录的记录ID为{0}'.format(mid))
    elif ms=='/my note' or ms=='/my note ':
        cur.execute("select * from memo where ownerid={0}".format(user['uid']))
        memolist=cur.fetchall()
        if memolist==():
            gs(gi,'您暂未记录，请使用/kb 8 2 记录内容来添加一条记录')
        else:
            s='共查询到您的{0}条记录，内容如下：\n'.format(len(memolist))
            for i in range(len(memolist)):
                s+=str(i+1)
                s+='.'
                s+=memolist[i]['text']
                s+='  记录ID：{0}\n'.format(memolist[i]['mid'])
            s+='以上就是所有记录。'
            gs(gi,s)
    elif ms=='/note' or ms=='/note ':
        gs(gi,'请使用/note 记录ID')
    elif ms[:6]=='/note 'and ms[6:]!='':
        cur.execute('select * from memo where mid={0}'.format(ms[6:]))
        note=cur.fetchall()
        if note==():
            gs(gi,'无指定记录，请检查记录ID或输入格式')
        else:
            gs(gi,'记录ID：{0}\n记录内容：{1}\n所有者：{2}'.format(ms[6:],note[0]['text'],note[0]['ownerid']))
    elif ms=='/delete' or ms=='/delete ':
        gs(gi,'请使用/delete 记录ID')
    elif ms[:8]=='/delete ' and ms[8:]!='':
        cur.execute('select * from memo where mid={0}'.format(ms[8:]))
        note=cur.fetchall()
        if note==():
            gs(gi,'无指定记录，请检查记录ID或输入格式')
        else:
            if note[0]['ownerid']==user['uid']:
                cur.execute('delete from memo where mid={0}'.format(ms[8:]))
                conn.commit()
                gs(gi,'删除记录ID为{0}的记录成功'.format(note[0]['mid']))
            else:
                gs(gi,'不允许非创建者的用户删除指定记录')
    elif ms=='/kb 9' or ms=='/kb 9 ':
        sms='您的QQ号：{0}\n您的昵称：{1}\n您的头像：[CQ:image,file=headimg_dl.image,subType=0,url=https://q.qlogo.cn/headimg_dl?dst_uin={0}&spec=100]'.format(int(rev['sender']['user_id']),rev['sender']['nickname'])
        gs(gi,sms)
    elif ms[:2]=='/l':
        inf=ms.split(' ')
        try:
            gid=int(inf[1])
            coor=inf[2]
            info=getgame(gid)
            if info==False:
                raise
            if info['binduser2']!=user['uid'] and info['binduser1']!=user['uid']:
                gs(gi,'您不是这个游戏的玩家哦~')
            elif (info['binduser1']==user['uid'] and info['who']==1) or (info['binduser2']==user['uid'] and info['who']==0):
                gs(gi,'没轮到你呢！')
            elif info['starttime']==0:
                gs(gi,'游戏未开始')
            else:
                coor=coorturn(coor,info['who'])
                if coor==False:
                    raise
                else:
                    if info['pic']=='':
                        pic=coor
                    else:
                        pic=info['pic']+','+coor
                    if info['who']==0:
                        who=1
                    else:
                        who=0
                    if info['who']==0:
                        t='黑方'
                        n='白方'
                        wh='b'
                    else:
                        t='白方'
                        n='黑方'
                        wh='w'
                    cur.execute("update game set `pic`='{0}' where `gid`={1}".format(pic,gid))
                    cur.execute('update game set `who`={0} where `gid`={1}'.format(who,gid))
                    conn.commit()
                    b_p(pic,gid)
                    winornot=gobangwin(pic,wh)
                    if winornot:
                        bc('{0}在{1}落子'.format(t,inf[2]),gid)
                        boo=stopgame(gid,info,'win',rev['sender']['nickname'])
                    else:  
                        bc('{0}在{1}落子，现在轮到{2}'.format(t,inf[2],n),gid)
        except Exception as e:
            gs(gi,'输入错误')
    elif ms=='/kb 10':
        gs(gi,'生成二维码请使用/kb 10 2 需要转化成二维码的内容\n读取二维码内容请使用/kb 10 1+图片（请务必使用图片加文字的组合消息！否则无法获取到图片！）')
    elif ms[:11]=='/kb 10 2':
        print('a')
        wha=ms[11:]
        create_qr_code(wha)
        gs(gi,'[CQ:image,file=file:///{0}/pic/qrcode_make_data.png]')
        