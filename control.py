# Import package

from tkinter import *
import tkinter.font
import pictureCollecting as pC 
import os
import threading


# 함수 선언

def stopapp():
    os.system("sudo reboot")
def startapp2():
    def startapp():
        try:
            os.system("make clean")
            os.system("make")
            os.system("make run")
        except:
            return 0
    try:
        thread = 0
        thread = threading.Thread(target=startapp)
        thread.start()
    except:
        return 0


def security():
    root1 = Toplevel()
    root1.title("사용자 등록")
    root1.resizable(0,0)

    #텍스트에 폰트와 padding을 지정할 수 있다.
    titleFont1=tkinter.font.Font(family="맑은 고딕", size=20, weight="bold", slant="italic")
    titleLabel = Label(root1, text="사용자 등록", font=titleFont1, fg="#424242", pady="5")
    titleLabel.pack()

    entryLabel = Label(root1, text="등록 할 사용자의 이름 입력: ", pady="5")
    entryLabel.pack()

    # ip 입력창 추가 
    entry = Entry(root1, width=40, bg="#CEECF5", borderwidth=1) #height는 왜 없어?
    entry.pack(pady=5)

    #ip 설정 함수
    def settingIP():
        global user
        if len(entry.get()) == 0: # entry.get() 입력 받는 것
            message = "등록 할 사용자의 이름을 입력하세요!."
        else:
            # user = entry.get()\
            text = entry.get()
            pC.pictureCollecting(text)
            pC.modelTraining(text)
            message = entry.get() + " 모델 제작 완료!"
            resultLabel.config(text=message)
            return 0

    settingButton = Button(root1, text="입력", command=settingIP, fg="#151515", bg="#BDBDBD", width=10)
    settingButton.pack(pady="5", padx="20") # anchor="nw",

    #result 
    resultLabel = Label(root1, text="")
    resultLabel.pack(pady=10)

    root1.geometry("600x400") # 600x400


# main function


if __name__ == "__main__":
    root = Tk()
    root.geometry("350x300")
    root.title('침입 관제 프로그램 for Raspberry')
    root.resizable(0,0)

    titleFont=tkinter.font.Font(family="맑은 고딕", size=20, weight="bold")
    sensorFont = tkinter.font.Font(size=10, weight="bold")

    label = Label(root, font=titleFont, text="침입 관제 프로그램", pady="5")
    label.pack(pady="30", padx="20")

    certifyButton = Button(root, text="인증하기", command=startapp2, fg="#151515", bg="#BDBDBD", width=20, pady="5")
    certifyButton.pack()
    securityButton = Button(root, text="사용자 등록", command=security, fg="#151515", bg="#BDBDBD", width=20, pady="5")
    securityButton.pack(pady="30", padx="20")
    stopButton = Button(root, text="STOP", command=stopapp, fg="#151515", bg="#BDBDBD", width=20, pady="5")
    stopButton.pack()

    root.mainloop()           