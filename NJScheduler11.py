from ipaddress import collapse_addresses
from optparse import Option
from tkinter.tix import COLUMN
from tokenize import String
from xml.sax.handler import DTDHandler

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from http.client import PRECONDITION_FAILED
from tkinter import*
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime

cred = credentials.Certificate("C:\\Users\\cys70\\Downloads\\njtalk.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://njtalk-default-rtdb.firebaseio.com/'})
win = Tk()
#default_app = firebase_admin.initialize_app()

whatclass = StringVar()
dayvar = StringVar()
classvar = StringVar()
changeday = StringVar()

classnumlabel = [[Label(win, width=10, text='value') for i in range(6)] for j in range(8)]
for i in range(7):
    for j in range(5):
        classnumlabel[i][j] = Label(win, width=10, text="value")
        classnumlabel[i][j].grid(row=i+5, column=j+2)

todayclass = ["" for i in range(7)]
todayclasslabel = [Label(win, width=10, text="value") for i in range(7)]
empty3 = Label(win, width=10, text="")
empty3.grid(row=1, column=7)
todaylabel = Label(win, width=10, text="오늘")
todaylabel.grid(row=4, column=8)
for i in range(7):
    todayclasslabel[i].grid(row=i+5, column=8)


def TotalReset():
    resetdayarray = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    resetclassarray = ["1학년1반", "1학년2반", "1학년3반"]
    reallyreset = messagebox.askquestion('전체 초기화', '모든 학급의 담임교사, 교과, 담당교사 등 모든 정보를 삭제하고 초기화합니다. 진행하겠습니까?')
    if reallyreset=='yes':
        reallyreallyreset = messagebox.askquestion('전체 초기화', '전체 초기화를 정말 진행하시겠습니까?')
        if reallyreallyreset=='yes':
            for i in range(3):
                for j in range(5):
                    dir = db.reference(resetclassarray[i]+'/'+resetdayarray[j])
                    for k in range(1, 8):
                        dir.update({"class"+str(k) : "Value"})
                        dir.update({"teacher"+str(k) : "Value"})
                dir = db.reference(resetclassarray[i]+'/today')
                for k in range(1, 8):
                    dir.update({'class'+str(k):'Value'})
                    dir.update({'teacher'+str(k):'Value'})
            messagebox.showinfo('초기화 완료', '데이터베이스 초기화가 완료되었습니다')





def RegistClicked():
    day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    kday = ['월', '화', '수', '목', '금']
    
    global selectclass
    selectclass = whatclass.get()
    classlabel.config(text=selectclass)

    today = datetime.now()
    whatday = int(today.weekday())
    if whatday>4 :
        todaylabel.config(text="주말")
        for i in range(7):
            todayclasslabel[i].config(text="")
    else:
        accessday = day[whatday]
        todaylabel.config(text="오늘("+kday[whatday]+")")
        for i in range(0, 7):
            dir = db.reference(selectclass + '/' + accessday + '/' + 'class' + str(i+1))
            todayclass[i] = dir.get()
            todayclasslabel[i].config(text=todayclass[i])
    
    for i in range(5):
        for j in range(7):
            dir = db.reference(selectclass +'/'+ day[i] +'/'+ 'class' + str(j+1))
            #print(selectclass +'/'+ day[i] +'/'+ 'class' + str(j))
            classnumlabel[j][i].config(text=dir.get())





def dayRegist(selectday):
    if selectday == 'Mon':      numday = 0
    elif selectday == 'Tue':    numday = 1
    elif selectday == 'Wed':    numday = 2
    elif selectday == 'Thu':    numday = 3
    else:                       numday = 4

    for i in range(7):
        dir = db.reference(selectclass+'/'+selectday+'/class'+str(i))
        tempRegist = dir.get()
        classnumlabel[i][numday].config(text=tempRegist)

        



def classRegist(day, classnum):
    if day=='Mon':      numday=0
    elif day=='Tue':    numday=1
    elif day=='Wed':    numday=2
    elif day=='Thu':    numday=3
    else:               numday=4

    dir = db.reference(selectclass+'/'+day+'/class'+classnum)
    print(selectclass+'/'+day+'/class'+classnum)
    tempRegist = dir.get()
    print(tempRegist)
    classnumlabel[int(classnum)-1][numday].config(text=tempRegist)





def ChangeClicked():
    if dayvar.get()!='요일' and classvar.get()!='교시':
        change()
    else:
        messagebox.showinfo('오류', '요일과 교시를 제대로 선택하십시오')





def change():
    if dayvar.get()=='월요일':
        selectday = "Mon"
    elif dayvar.get()=='화요일':
        selectday = 'Tue'
    elif dayvar.get()=='수요일':
        selectday = 'Wed'
    elif dayvar.get()=='목요일':
        selectday = 'Thu'
    elif dayvar.get()=='금요일':
        selectday = 'Fri'
    tempclass = classvar.get()
    changeclass = tempclass[0:1]

    dir = db.reference(selectclass+'/'+selectday+'/'+'class'+str(changeclass))
    nowclass = dir.get()
    dir = db.reference(selectclass+'/'+selectday+'/'+'teacher'+str(changeclass))
    nowteacher = dir.get()

    chgclass = classchange.get()
    chgteacher = teacherchange.get()

    change = messagebox.askquestion('시간표 변경', dayvar.get() + classvar.get() + '변경하시겠습니까?\n변경 전 : ' + nowclass + nowteacher + '\n변경 후 : ' + chgclass + chgteacher)
    if change == 'yes':
        dir = db.reference(selectclass+'/'+selectday)
        dir.update({'class'+changeclass : chgclass})
        dir.update({'teacher'+changeclass : chgteacher})
        classRegist(selectday, changeclass)
        messagebox.showinfo("변경 완료", "선택한 교시 변경이 완료되었습니다.")






def TempChange():
    today = datetime.now()
    global whatday
    whatday = today.weekday()
    if whatday==0:      accessday = 'Mon'
    elif whatday==1:    accessday = 'Tue'
    elif whatday==2:    accessday = 'Wed'
    elif whatday==3:    accessday = 'Thu'
    elif whatday==4:    accessday = 'Fri'
    
    #dir = db.reference(selectclass+'/'+accessday)
    if whatday>4:
        messagebox.showinfo("주말", "주말엔 오늘의 수업 변경이 불가능합니다.")
    else:
        tempwin()





def tempwin():
    tw = Toplevel(win)
    
    twinfo1 = Label(tw, width=10, text="기존")
    twinfo1.grid(row=1, column=1)

    twclass = [Label(tw, width=10, text="") for i in range(7)]
    for i in range(7):
        twclass[i].config(text=todayclass[i])
        twclass[i].grid(row=i+2, column=1)

    twinfo2 = Label(tw, width=10, text="변경교과")
    twinfo2.grid(row=1, column=2)
    global entryclass
    entryclass = [Entry(tw, width=10) for i in range(7)]
    for i in range(7):
        entryclass[i].grid(row=i+2, column=2)

    
    twinfo3 = Label(tw, width=10, text="변경교사")
    twinfo3.grid(row=1, column=3)
    global entryteacher
    entryteacher = [Entry(tw, width=10) for i in range(7)]
    for i in range(7):
        entryteacher[i].grid(row=i+2, column=3)
    
    cancelbutton = Button(tw, width=10, text="취소", command=lambda:tempcancel(tw))
    cancelbutton.grid(row=9, column=2)
    okbutton = Button(tw, width=10, text="변경", command=lambda:tempok(tw))
    okbutton.grid(row=9, column=3)





def tempcancel(tw):
    tw.destroy()



def tempok(tw):
    tempclass = ['','','','','','','']
    tempteacher = ['','','','','','','',]
    day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

    for i in range(7):
        tempclass[i]=entryclass[i].get()
        tempteacher[i]=entryteacher[i].get()
    
    dir=db.reference(selectclass+'/'+day[whatday]+'/today')
    for i in range(7):
        dir.update({'class'+str(i):tempclass[i]})
        dir.update({'teacher'+str(i):tempteacher[i]})

    messagebox.showinfo('오늘의 시간표 변경 완료', '오늘의 시간표 변경이 완료되었습니다.')
    tw.destroy()





def totalWin():
    tw = Toplevel()
    #totalemp1 = Label(tw, width=5, text="")
    #totalemp1.grid(row=1, column=1)
    week = ['월요일', '화요일', '수요일', '목요일', '금요일']
    daylabel = [Label(tw, width=20) for i in range(5)]
    tinfo = [Label(tw, width=10, text="교사") for i in range(5)]
    cinfo = [Label(tw, width=10, text="교과") for i in range(5)]
    for i in range(5):
        tinfo[i].grid(row=2, column=3+i*2)
        cinfo[i].grid(row=2, column=2+i*2)
    for i in range(5):
        daylabel[i].config(text=week[i])
        daylabel[i].grid(row=1, column=2*i+2, columnspan=2)
    ttnum = [Label(tw, width=5) for i in range(7)]
    for i in range(7):
        ttnum[i].config(text=str(i+1))
        ttnum[i].grid(row=i+3, column=1)
        
    teacher = [[Entry(tw, width=10) for i in range(7)] for i in range(5)]
    for i in range(5):
        for j in range(7):
            teacher[i][j].grid(row=j+3, column=3+i*2)

    subject = [[Entry(tw, width=10) for i in range(7)] for i in range(5)]
    for i in range(5):
        for j in range(7):
            subject[i][j].grid(row=j+3, column=2+i*2)

    ttempty = Label(tw, width=5, text=" ")
    ttempty.grid(row=10, column=1)
    okbutton = Button(tw, width=10, text="확인", command=lambda:ttok(teacher, subject))
    cancelbutton = Button(tw, width=10, text="취소", command=lambda:ttcancel(tw))
    okbutton.grid(row=11, column=2)
    cancelbutton.grid(row=11, column=3)

    



def ttok(teacher, subject):
    day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    for i in range(5):
        for j in range(7):
            dir = db.reference(selectclass+'/'+day[i])
            dir.update({'class'+str(j+1):subject[i][j]})
            dir.update({'teacher'+str(j+1):teacher[i][j]})






def ttcancel(tw):
    tw.destroy()





def TotalChange():
    totalWin()





def DayChange():
    print()









win.title("NJScheduler Administor")
prginfo = Label(win, text="Administor 1.0.0")
prginfo.grid(row=1, column=1)
totalreset = Button(win, width=10, text="전체 초기화", command=TotalReset)
totalreset.grid(row=1, column=2)

empty1 = Label(win, text="")
empty1.grid(row=2, column=1)
rgstinfo = Label(win, width=8, text="시간표 확인")
rgstinfo.grid(row=3, column=1)

"""
testlabel = Label(win, text="")
testlabel.grid(row=5, column=2)
"""

chooselabel = Label(win, width=10, text="반 선택")
chooselabel.grid(row=3, column=1)

whatclass.set('  학년 반 ')
classlist = OptionMenu(win, whatclass, '1학년1반', '1학년2반', '1학년3반')
classlist.grid(row=3, column=2)

viewbutton = Button(win, width=10, text="조회", command=RegistClicked)
viewbutton.grid(row=3, column=3)



classlabel = Label(win, width=10, height=2, text="학년 반")
classlabel.grid(row=4, column=1)

dayarray = ["월요일", "화요일", "수요일", "목요일", "금요일"]
daylabel = [0 for i in range(5)]
numlabel = [0 for i in range(8)]

for i in range(0, 5):
    daylabel[i] = Label(win, width=10, height=2, text=dayarray[i])
    daylabel[i].grid(row=4, column=i+2)
for i in range(0, 7):
    numlabel[i] = Label(win, width=10, height=2, text=i+1)
    numlabel[i].grid(row=i+5, column=1)

blanklabel1 = Label(win, width=10, text=" ")
blanklabel1.grid(row=12, column=1)
soojeonglabel = Label(win, width=10, text="시간표 수정")
soojeonglabel.grid(row=13, column=1)

dayvar.set("요일")
classvar.set("교시")
dayselect = OptionMenu(win, dayvar, '월요일', '화요일', '수요일', '목요일', '금요일')
dayselect.grid(row=13, column=2)
classselect = OptionMenu(win, classvar, '1교시', '2교시', '3교시', '4교시', '5교시', '6교시', '7교시')
classselect.grid(row=13, column=3)

classchangelabel = Label(win, width=10, text="과목")
classchangelabel.grid(row=14, column=1)
classchange = Entry(win, width=10)
classchange.grid(row=14, column=2)
teacherchangelabel = Label(win, width=10, text="선생님")
teacherchangelabel.grid(row=15, column=1) 
teacherchange = Entry(win, width=10)
teacherchange.grid(row=15, column=2)

classchangebutton = Button(win, width=5, text="변경", command=ChangeClicked)
classchangebutton.grid(row=15, column=3)

empty2 = Label(win, width=10, text=" ")
empty2.grid(row=14, column=4)

tempchangebutton = Button(win, width=10, text="임시 변경", command=TempChange)
tempchangebutton.grid(row=13, column=5)
totalchangebutton = Button(win, width=10, text="전체 변경", command=TotalChange)
totalchangebutton.grid(row=13, column=6)


daychangelist = OptionMenu(win, changeday, '월요일', '화요일', '수요일', '목요일', '금요일')
daychangelist.grid(row=15, column=5)
changeday.set('요일')
daychangebutton = Button(win, width=10, text="요일 변경", command=DayChange)
daychangebutton.grid(row=15, column=6)
"""
while True:
    if selectclass=="1학년1반":
        dir = db.reference("1학년 1반/Mon")
        for i in range(1, 8):
            subject = dir.get()
"""

win.mainloop()