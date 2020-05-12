import requests
import json
import time
import random
import threading
class NewThread(threading.Thread):
    def __init__(self,learntime,x):
        threading.Thread.__init__(self)
        self.deamon = True
        self.learntime = learntime
        self.x = x
    def run(self):
        startstudy(self.learntime,self.x)
def startstudy(learntime,x):
#    print('\n位置: '+x['location']+'\n已学习: '+x['learntime']+'
#    即将学习'+str(learntime)+'秒～',end='')
    scoid = x['id']
    url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
    req1 = session.post(url,data={'action':'getscoinfo_v7','uid':uid,'cid':cid,'scoid':scoid},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
    if('学习数据不正确' in req1.text):
        req1 = session.post(url,data={'action':'startsco160928','uid':uid,'cid':cid,'scoid':scoid},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
        req1 = session.post(url,data={'action':'getscoinfo_v7','uid':uid,'cid':cid,'scoid':scoid},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
        if('学习数据不正确' in req1.text):
            print('\n错误:',x['location'])
            wrong.append(x['location'])
            return 0
    back = json.loads(req1.text)['comment']
    if('cmi' in back):
        back = json.loads(back)['cmi']
        cstatus = back['completion_status']
        progress = back['progress_measure']
        session_time = back['session_time']
        total_time = back['total_time']
        crate = back['score']['scaled']
    else:
        cstatus = 'not_attempted'
        progress = session_time = total_time = '0'
        crate = ''
    url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
    req1 = session.post(url,data={'action':'keepsco_with_getticket_with_updatecmitime','uid':uid,'cid':cid,'scoid':scoid,'session_time':session_time,'total_time':total_time},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
    for nowtime in range(1,learntime + 1):
#        print(str(nowtime)+'～',end='')
        time.sleep(1)
        if(nowtime % 60 == 0):
#            print('发送心跳包～',end='')
            url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
            req1 = session.post(url,data={'action':'keepsco_with_getticket_with_updatecmitime','uid':uid,'cid':cid,'scoid':scoid,'session_time':session_time,'total_time':total_time},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
#    print('增加学习时间～')
    url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
    req1 = session.post(url,data={'action':'savescoinfo160928','cid':cid,'scoid':scoid,'uid':uid,'progress':progress,'crate':crate,'status':'unknown','cstatus':cstatus,'trycount':'0'},headers={'Referer':'https://welearn.sflep.com/Student/StudyCourse.aspx'})


print('**********  Created By Avenshy  **********\nVersion:0.2dev\n')
session = requests.Session()
username = input('Username: ')
password = input('Password: ')

print('Login...',end=' ')
url = 'https://sso.sflep.com/cas/login?service=http%3a%2f%2fwelearn.sflep.com%2f2019%2fuser%2floginredirect.aspx'
req = session.get(url)
lt = req.text[req.text.find('name="lt" value="') + 17:req.text.find('name="lt" value="') + 17 + 76]
url = 'https://sso.sflep.com/cas/login?service=http%3a%2f%2fwelearn.sflep.com%2f2019%2fuser%2floginredirect.aspx'
req = session.post(url,data={'username':username,'password':password,'lt':lt,'_eventId':'submit','submit':'LOGIN'})
if('请登录' in req.text):
    input('Fail!!\n')
    exit(0)
print('Success!!\n\n')
while True:
    url = 'https://welearn.sflep.com/ajax/authCourse.aspx?action=gmc'
    req = session.get(url,headers={'Referer':'https://welearn.sflep.com/2019/student/index.aspx'})
    back = json.loads(req.text)['clist']
    i = 1
    for x in back:
        print('[id:{:>2d}]  完成度 {:>2d}%  {}'.format(i,x['per'],x['name']))
        i+=1
    i = int(input('\n请输入需要刷时长的课程id（id为上方[]内的序号）: '))

    cid = str(back[i - 1]['cid'])
    url = 'https://welearn.sflep.com/2019/student/course_info.aspx?cid=' + cid
    req = session.get(url,headers={'Referer':'https://welearn.sflep.com/2019/student/index.aspx'})
    uid = req.text[req.text.find('"uid":') + 6:req.text.find('"',req.text.find('"uid":') + 7) - 2]
    classid = req.text[req.text.find('classid=') + 8:req.text.find('&',req.text.find('classid=') + 9)]


    url = 'https://welearn.sflep.com/ajax/StudyStat.aspx'
    req = session.get(url,params={'action':'courseunits','cid':cid,'uid':uid},headers={'Referer':'https://welearn.sflep.com/2019/student/course_info.aspx'})
    back = json.loads(req.text)['info']

    print('\n\n[id: 0]  按顺序刷全部单元学习时长')
    i = 0
    unitsnum = len(back)
    for x in back:
        i+=1
        print('[id:{:>2d}]  {}  {}'.format(i,x['unitname'],x['name']))
    unitidx = int(input('\n\n请选择要刷时长的单元id（id为上方[]内的序号，输入0为刷全部单元）： '))


    inputdata = input('\n\n\n模式1:每个练习增加指定学习时长，请直接输入时间\n如:希望每个练习增加30秒，则输入 30\n\n模式2:每个练习增加随机时长，请输入时间上下限并用英文逗号隔开\n如:希望每个练习增加10～30秒，则输入 10,30\n\n\n请严格按照以上格式输入: ')
    if(',' in inputdata):
        inputtime = eval(inputdata)
        mode = 2
    else:
        inputtime = int(inputdata)
        mode = 1


    threads = 100 #最大线程数设置
    running = []
    runningnumber = maxtime = 0
    wrong = []

    if(unitidx == 0):
        i = 0
    else:
        i = unitidx - 1
        unitsnum = unitidx

#    while '异常' not in req.text and '出错了' not in req.text:
    for unit in range(i,unitsnum):
        url = 'https://welearn.sflep.com/ajax/StudyStat.aspx?action=scoLeaves&cid=' + cid + '&uid=' + uid + '&unitidx=' + str(unit) + '&classid=' + classid
        req = session.get(url,headers={'Referer':'https://welearn.sflep.com/2019/student/course_info.aspx?cid=' + cid})
        back = json.loads(req.text)['info']
        for x in back:
            if(mode == 1):
                learntime = inputtime
            else:
                learntime = random.randint(inputtime[0],inputtime[1])
            if(runningnumber == threads):
                for nowtime in range(1,maxtime + 1):
                    print('\r已启动线程:',runningnumber,'当前秒数:',nowtime,'秒，总时间:',maxtime,'秒',end='')
                    time.sleep(1)
                print('  等待线程退出…')
                for t in running:
                    t.join()
                runningnumber = maxtime = 0
                running = []
            running.append(NewThread(learntime,x))
            running[runningnumber].start()
            runningnumber+=1
            if(learntime > maxtime):
                maxtime = learntime
            print('线程:',runningnumber,'位置:',x['location'],'\n已学: ',x['learntime'],'将学:',learntime,'秒')

        if(runningnumber > 0):
            for nowtime in range(1,maxtime + 1):
                print('\r已启动线程:',runningnumber,'当前秒数:',nowtime,'秒，总时间:',maxtime,'秒',end='')
                time.sleep(1)
            print('  等待线程退出…')
            for t in range(runningnumber):
                running[t].join()
            runningnumber = maxtime = 0
            running = []

    if (unitidx == 0):
        break
    else:
        print('\n\n本单元结束！错误:',len(wrong),'个')
        for i in range(len(wrong)):
            print('第',i + 1,'个错误:',wrong[i])
        print('回到选课处！！\n\n\n\n')

print('运行结束!!\n错误:',len(wrong),'个')
for i in range(len(wrong)):
    print('第',i + 1,'个错误:',wrong[i])
print("\n\n\n**********  Created By Avenshy  **********\n\n\n")
input("Press any key to exit...")
