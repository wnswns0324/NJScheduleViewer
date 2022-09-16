from tkinter.tix import COLUMN
from tokenize import String
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from http.client import PRECONDITION_FAILED
from tkinter import*
from tkinter import ttk
from tkinter import messagebox

cred = credentials.Certificate("C:\\Users\\cys70\\Downloads\\njtalk.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://njtalk-default-rtdb.firebaseio.com/'})
win = Tk()
#default_app = firebase_admin.initialize_app()

whatclass = StringVar()
dayvar = StringVar()
classvar = StringVar()

classnumlabel = [[Label(win, width=10, text='value') for i in range(6)] for j in range(8)]
for i in range(7):
    for j in range(5):
        classnumlabel[i][j] = Label(win, width=10, text="value")
        classnumlabel[i][j].grid(row=i+5, column=j+2)


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
            messagebox.showinfo('초기화 완료', '데이터베이스 초기화가 완료되었습니다')

def RegistClicked():
    day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    
    global selectclass
    selectclass = whatclass.get()
    classlabel.config(text=selectclass)

    for i in range(5):
        for j in range(7):
            dir = db.reference(selectclass +'/'+ day[i] +'/'+ 'class' + str(j+1))
            #print(selectclass +'/'+ day[i] +'/'+ 'class' + str(j))
            classnumlabel[j][i].config(text=dir.get())

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
        RegistClicked()


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

"""
while True:
    if selectclass=="1학년1반":
        dir = db.reference("1학년 1반/Mon")
        for i in range(1, 8):
            subject = dir.get()
"""

win.mainloop()