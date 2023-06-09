import http.client as httplib
def checknetconnect():
    url="www.google.com"
    timeout=3
    connection = httplib.HTTPConnection(url,timeout=timeout)
    try:
        connection.request("HEAD", "/")
        connection.close()  # connection closed
        print("Internet On")
        return True
    except Exception as exep:
        print("Internet Off")
        return False

#main
inter=checknetconnect()
if inter==False:
    def speak():
        v=tts.init()
        v.setProperty('rate',135)
        v.say("Please check your Internet Connection Sir!")
        v.runAndWait()
    import tkinter as tk
    from tkinter import *
    import pyttsx3 as tts
    from PIL import ImageTk, Image
    import time
    root = tk.Tk()
    root.title("Oops!")
    root.state('zoomed')
    mycanvas = tk.Canvas(root, width=200, height=25)
    mycanvas.create_rectangle(0, 0, 200, 40)
    mycanvas.place(x=100, y=100)
    text_canvas = mycanvas.create_text(10, 10, anchor="nw")
    mycanvas.itemconfig(text_canvas, text="Look no background! Thats new!")
    bgimg = ImageTk.PhotoImage(Image.open('C:\\Users\\Joel\\Desktop\\LITEPAY\\nointbg.png'))  # "C:\Users\Joel\Desktop\pybg.png"
    limg = Label(root, i=bgimg)
    limg.pack()
    root.after(50,speak)
    #time.sleep(10)
    # messagebox.showinfo("Oops!","NO INTERNET CONNECTION!",parent=root,icon='warning')
    root.mainloop()
else:
    import tkinter as tk
    from tkinter import *
    import time
    from PIL import ImageTk,Image
    from tkinter import messagebox
    import cx_Oracle
    import random
    import smtplib
    import webbrowser
    from tkinter import ttk
    import pyttsx3 as tts
    import cv2
    from cv2 import *
    import winsound



    def send_credentials(uid):
        # getting details from sql
        con = cx_Oracle.connect('system/joel@localhost:1521/xe')
        cur = con.cursor()
        cur.execute('select * from litepay where userid={}'.format(uid))
        li = [x for x in cur]
        details = li[0]
        # sending email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('bintujmj@gmail.com', 'cumfbgztetaoubxx')
        f = open('User_Credentials.txt', 'r')
        form = f.read()
        server.sendmail('bintujmj@gmail.com', details[2],form.format(details[1], details[0], details[3], details[2], details[5], details[4]))

    def contin(amount,ruid,suid,tnc,window):
        cb = tnc.state()
        st=""
        if len(cb)>1:
            st=cb[1]
        print(st)
        ans=messagebox.askyesno("Confirm!","Are you Sure?",parent=window)
        if st=='selected':
            if ans==False:
                print("Confirming details again...")
                pass
            else:
                con = cx_Oracle.connect('system/joel@localhost:1521/xe')
                cur = con.cursor()
                cur.execute('select * from litepay where userid={}'.format(int(suid))) #Sender Userid
                li = [x for x in cur]
                sname=li[0][0]#sender name
                sacblnc = li[0][4] #Sender account balance
                print(sacblnc)
                if int(amount)>sacblnc:
                    messagebox.showwarning("Low balance","Insufficient Balance",parent=window)
                elif ruid=="":
                    messagebox.showwarning("Error", "Enter Receiver UID", parent=window)
                else:
                    messagebox.showinfo("Please Wait!", "Please Wait for 30 secs\n Your details will be updated.",parent=window)
                    cur.execute('update litepay set accblnc={} where userid={}'.format(sacblnc-int(amount),int(suid)))
                    try:
                        cur.execute('select * from litepay where userid={}'.format(int(ruid)))  # Receiver Userid
                        ls = [x for x in cur]
                        rname=ls[0][0]
                        racblnc = ls[0][4]
                    except:
                         messagebox.showinfo("Incorrect Details", "Please check Receiver's User id",parent=window)
                    cur.execute('update litepay set accblnc={} where userid={}'.format(racblnc + int(amount), int(ruid)))
                    cur.execute('insert into lp{}hist values({},{},(select systimestamp from dual))'.format(str(suid),ruid,amount))
                    cur.execute('insert into lp{}hist values({},{},(select systimestamp from dual))'.format(str(ruid),suid,amount))
                    con.commit()
                    print("Money Sent Successfully i.e., Rows updated")
                    #Mailing txn details
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login('bintujmj@gmail.com', 'cumfbgztetaoubxx')
                    f = open('Transaction_details.txt', 'r')
                    form = f.read()
                    cur.execute('select * from litepay where userid={}'.format(int(suid)))  # Sender Userid
                    ln = [x for x in cur]
                    nacblnc = ln[0][4] #New Balance
                    server.sendmail('bintujmj@gmail.com',li[0][2] , form.format(li[0][1],li[0][0],ls[0][0],int(amount),nacblnc))
                    window.after(100,lambda:speak("Money transferred successfully!"))
                    messagebox.showinfo("Success!", "Money Transferred Successfully!!", parent=window)
                    print("Transaction details Sent Successfully")
        else:
            messagebox.showwarning("Check!","Accept Terms and conditions!",parent=window)

    def check_blnc(uid,lab):
        con = cx_Oracle.connect('system/joel@localhost:1521/xe')
        cur = con.cursor()
        cur.execute('select * from litepay where userid={}'.format(uid))
        li = [x for x in cur]
        acblnc=li[-1][4]
        lab.config(text=str(acblnc))
        con.commit()
        pass

    def insertrow(name,gmail,phno):
        con = cx_Oracle.connect('system/joel@localhost:1521/xe')
        cur = con.cursor()
        cur.execute('select * from litepay')
        li=[int(x[0]) for x in cur]
        cur.execute('select * from litepay')
        passs=[int(x[5]) for x in cur]
        uid=max(li)+1
        pas=max(passs)+1
        print(uid,pas)
        accblnc=10000
        cur.execute('insert into litepay values({},\'{}\',\'{}\',{},{},{})'.format(uid,name,gmail,phno,accblnc,pas))
        cur.execute('create table lp{}hist(RecId number(10),amount number(10),dateoftxn char(35))'.format(str(uid)))
        cur.execute('insert into lp{}hist values({},{},(select systimestamp from dual))'.format(str(uid),uid,10000))
        print("HistoryTable Created and Initiated!")
        con.commit()
        print("Details inserted as a row")
        return uid,pas

    def getdetails_sendotp(uid,window):
        messagebox.showinfo("Please Wait","Please wait 20 secs for OTP\nIf not received Try sending again",parent=window)
        con = cx_Oracle.connect('system/joel@localhost:1521/xe')
        cur = con.cursor()
        cur.execute('select * from litepay where userid={}'.format(uid))
        li = [x for x in cur]
        phno = li[0][3] #int
        gmail=li[0][2]
        pas=li[0][5] #int
        print(phno,gmail,pas)
        genotp('+91'+str(phno), gmail, window)
        print("Got details... now sending gmail...")

    def genotp(phno, gmail,window):
        if gmail=="" or phno=="" or len(phno)<10 or "@gmail.com" not in gmail:
            messagebox.showwarning("Insufficient details","Insufficient/Incorrect Details\nPlease Check Contact Details...",parent=signw)
        else:
            #messagebox.showinfo("Please Wait", "Please wait 20 secs for OTP\nIf not received Try sending again",parent=window)
            otp = (random.randint(1111, 9999))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('bintujmj@gmail.com', 'cumfbgztetaoubxx')
            f = open('mailformat.txt', 'r')
            form = f.read()
            server.sendmail('bintujmj@gmail.com', gmail, form.format(otp,otp))
            print('Gmail sent!...Sms sending...')
            f = open('mailformat.txt', 'r')
            bodyformat = f.read()
            ###################
            phnos = phno[0:3] + '*******' + phno[11::]
            gmails = gmail[0] + '**********' + gmail[-12::1]
            messagebox.showinfo("OTP SENT!","OTP sent successfully!\n Check your Gmail:-{}".format(gmails),parent=window)
            f = open('otpgenerated.txt', 'w')
            f.write(str(otp))
            return otp

    def otpgenerate(window):
        f=open('otpgenerated.txt','r')
        otpg=f.read()
        print("Got otp from text file...")
        return int(otpg)

    def getstarted():  #LOGIN PAGE
        print("Getstarted!!!...")
        rotp=0
        global mainp
        try:
            win.destroy()
        except:
            pass
        mainp = tk.Tk()
        mainp.title("Home Page")
        mainp.state('zoomed')
        seticon(mainp)
        bgimg = ImageTk.PhotoImage(Image.open('C:\\Users\\Joel\\Desktop\\LITEPAY\\mainpbg.png'))
        limg = Label(mainp, i=bgimg)
        limg.pack()
        uid=Entry(mainp,font=("Arial Rounded MT Bold",20))
        uid.place(x=630,y=270)
        pas=Entry(mainp,font=("Arial Rounded MT Bold", 20))
        pas.place(x=630, y=400)

        forpass = Button(command=lambda:forgotpass(int(uid.get())), text="         Forgot Password         ",font=("Arial Rounded MT Bold", 13))
        forpass.place(x=660, y=510)
        sub = Button(command=lambda: checkpass(uid.get(), pas.get()), text="        S U B M I T       ",font=("Arial Rounded MT Bold", 15))
        sub.place(x=670, y=460)
        sign = Button(command=signup, text="      NEW ACCOUNT      ", font=("Arial Rounded MT Bold", 18))
        sign.place(x=640,y=660)
        backbtn=Button(command=lambda:ofcourseyes(mainp),text="<-Back",font=("Arial Rounded MT Bold",15),fg='blue',bg='white').place(x=100,y=50)
        mainp.after(100,lambda:speak("Welcome Please Login if you are new    else create new account"))
        mainp.mainloop()


    def backf(window):
        window.destroy()


    def checkpass(uid,pasr):
        con  = cx_Oracle.connect('system/joel@localhost:1521/xe')
        cur  = con.cursor()
        try:
            cur.execute('select * from litepay where userid={}'.format(int(uid)))  # Userid
            li   = [x for x in cur]
            pas  = int(li[0][5]) # Sender account balance
            name = li[0][1]
            print(pas)
        except:
            messagebox.showinfo("Incorrect details","Incorrect Details!\nPlease check again..")
        if pas!=int(pasr):
            messagebox.showinfo("Error","Incorrect Password!!",icon='error')
        else:
            global sub
            sub = tk.Toplevel()
            sub.title("SUBMITTED")
            sub.state('zoomed')
            seticon(sub)
            bgimg = ImageTk.PhotoImage(Image.open('C:\\Users\\Joel\\Desktop\\LITEPAY\\transactionbg.png'))  # "C:\Users\Joel\Desktop\pybg.png"
            limg = Label(sub, i=bgimg)
            limg.pack()
            #global uname
            #uname="Hello, Welcome Back "+name+"!", font=("Arial Rounded MT Bold", 20),fg='white',bg='darkblue')
            #uname.place(x=600, y=10)
            global blnc
            blnc = Label(sub, text="          ", font=("Arial Rounded MT Bold", 20), width=20)
            blnc.place(x=200, y=600)
            e1 = Entry(sub, font=("Arial Rounded MT Bold", 25), width=17)
            e1.place(x=1030, y=300)
            e2 = Entry(sub, font=("Arial Rounded MT Bold", 25), width=17)
            e2.place(x=1030, y=450)
            v=tk.IntVar()
            tnc = ttk.Checkbutton(sub)
            tnc.place(x=1000, y=600)
            back=Button(sub, command=lambda:backf(sub), text="<- BACK ",font=("Arial Rounded MT Bold", 15),bg='white',fg='blue')
            back.place(x=10,y=30)
            Button(sub, command=lambda: check_blnc(uid, blnc), text="CHECK BALANCE", font=("Arial Rounded MT Bold", 20),width=20, bg='white', fg='blue').place(x=200, y=670)
            Button(sub, command=lambda: contin(e1.get(), e2.get(), uid,tnc, sub), text="Continue",font=("Arial Rounded MT Bold", 20), width=20, bg='white', fg='blue').place(x=1000, y=660)
            Button(sub, command=lambda: view_history(uid), text="Mail History",font=("Arial Rounded MT Bold", 20), width=10, bg='white', fg='blue').place(x=650, y=680)            
            welcomemsg = "Hello, Welcome Back " + name + "!"
            leng=len(welcomemsg)
            image = Image.open("C:\\Users\\Joel\\Desktop\\LITEPAY\\blue.png")
            resize_image = image.resize((leng*30, 50))
            img = ImageTk.PhotoImage(resize_image)
            global label3
            label3 = tk.Label(sub, text='', image=img, compound='center', font=("Algerian", 30), fg='white')
            label3.place(x=320, y=15)
            sub.after(100,lambda:speak("Hello Welcome Back {}! ".format(name+" sir")))
            run(1, welcomemsg,label3)
            sub.mainloop()


    def view_history(uid):
        con = cx_Oracle.connect('system/joel@localhost:1521/xe')
        cur = con.cursor()
        cur.execute('select * from litepay where userid={}'.format(uid))
        li = [x for x in cur]
        uname = li[0][1]
        cur.execute('select * from lp{}hist'.format(str(uid)))
        lhist=[x for x in cur]
        f=open('emailhist.txt','r')
        form = f.read()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('bintujmj@gmail.com', 'cumfbgztetaoubxx')
        server.sendmail('bintujmj@gmail.com', li[0][2], form.format(lhist[::]))
        print("Transaction History Sent!")
        messagebox.showinfo("Done!","Txn History Details sent to your registerd mail! Thank you!",parent=sub)
        pass


    def forgotpass(uid):
        f=open('password.txt','w')
        f.write("")
        f2 = open('otpgenerated.txt', 'w')
        f2.write("")
        global forp
        forp=tk.Toplevel()
        forp.title("Forgot Password?")
        forp.state('zoomed')
        seticon(forp)
        bgimg = ImageTk.PhotoImage(Image.open('C:\\Users\\Joel\\Desktop\\LITEPAY\\forpasbg.png'))  # "C:\Users\Joel\Desktop\pybg.png"
        limg = Label(forp, i=bgimg)
        limg.pack()
        otp = Entry(forp, font=("Arial Rounded MT Bold", 20))
        otp.place(x=530, y=300)
        global p
        p=Label(forp,text="*******",width=20,font=("Arial Rounded MT Bold",20))
        p.place(x=530,y=550)
        back = Button(forp, command=lambda: backf(forp), text="<- BACK ", font=("Arial Rounded MT Bold", 15))
        back.place(x=75, y=75)
        sendotp = Button(forp,command=lambda: getdetails_sendotp(uid, forp), text="Send OTP",font=("Arial Rounded MT Bold", 15))
        sendotp.place(x=860,y=300)
        sub = Button(forp,command=lambda: checkotpf2(otp.get(),forp,uid), text="        S U B M I T       ",font=("Arial Rounded MT Bold", 15))
        sub.place(x=600, y=400)
        rpas = Button(forp, command=lambda: rpass(uid), text="R E V E A L  P A S S W O R D",font=("Arial Rounded MT Bold", 15))
        rpas.place(x=550, y=625)
        forp.mainloop()


    def rpass(uid):
        con = cx_Oracle.connect('system/joel@localhost:1521/xe')
        cur = con.cursor()
        cur.execute('select * from litepay where userid={}'.format(uid))
        li = [x for x in cur]
        pas = li[0][5]
        f=open('password.txt','r')
        try:
            pa=int(f.read())
            win.after(100,lambda:speak("Your password is {}".format(pa)))
        except:
            messagebox.showinfo("Verify OTP", "OTP Not Verified!", parent=forp)
        if pa==int(pas):
            p.config(text=str(pa))
            pass
        else:
            messagebox.showinfo("Verify OTP","OTP Not Verified!",parent=forp)


    def signup():
        global signw
        print("Signup started...")
        signw=tk.Toplevel()
        signw.state('zoomed')
        seticon(signw)
        signw.title("Hello There!")
        signw.geometry("1600x900")
        bgimg = ImageTk.PhotoImage(
        Image.open('C:\\Users\\Joel\\Desktop\\LITEPAY\\signupbg.png'))  # "C:\Users\Joel\Desktop\pybg.png"
        limg = Label(signw, i=bgimg)
        limg.pack()
        name = Entry(signw, font=("Arial Rounded MT Bold", 20))
        name.place(x=180, y=300)
        phno = Entry(signw, font=("Arial Rounded MT Bold", 20))
        phno.place(x=180, y=420)
        gmail = Entry(signw, font=("Arial Rounded MT Bold", 20))
        gmail.place(x=180, y=525)
        otp = Entry(signw, font=("Arial Rounded MT Bold", 20))
        otp.place(x=170, y=620)

        nic = Entry(signw, font=("Arial Rounded MT Bold", 20))
        nic.place(x=1000, y=300)
        city = Entry(signw, font=("Arial Rounded MT Bold", 20))
        city.place(x=1000, y=420)
        state = Entry(signw, font=("Arial Rounded MT Bold", 20))
        state.place(x=1000, y=525)
        pin = Entry(signw, font=("Arial Rounded MT Bold", 20))
        pin.place(x=1000, y=620)
        back=Button(signw, command=lambda:backf(signw), text="<- BACK ",font=("Arial Rounded MT Bold", 15))
        back.place(x=75,y=75)
        send=Button(signw,command=lambda:genotp("+91"+phno.get(),gmail.get(),signw), text="Send OTP ",font=("Arial Rounded MT Bold", 15))
        send.place(x=500,y=620)
        checkotp=Button(signw,command=lambda:checkotpf(int(otp.get()),signw), text="Check OTP",font=("Arial Rounded MT Bold", 15))
        checkotp.place(x=500,y=665)
        submitbtn = Button(signw, command=lambda:enter_details_into_db(name.get(),gmail.get(),phno.get()), text="S U B M I T",font=("Arial Rounded MT Bold", 15))
        submitbtn.place(x=708, y=720)
        signw.after(100,lambda:speak("Hello Please enter your credentials and have a great journey Happy Litepay!"))
        signw.mainloop()


    def enter_details_into_db(name,gmail,phno):
        if name=="" or gmail=="" or phno=="" or len(phno)<10 or "@gmail.com" not in gmail or name[0].isnumeric()==True:
            messagebox.showwarning("Insufficient details","Insufficient/Incorrect Details\nPlease Check Basic Details...",parent=signw)
        else:
            ans=messagebox.askyesno("Confirm!","Are you sure about the data you have entered!",parent=signw)
            if ans==True:
                messagebox.askyesno("Wait!", "Please wait for 15 secs to save your credentials!!\n HOLD ON!!", parent=signw)
                uid,pas=insertrow(name,gmail,phno) #This return uid and sends credentials as SMS and GMAIL.
                send_credentials(uid)
                messagebox.showinfo("Submitted!","Your Credentials have been Saved!\n CONGRATULATIONS!!\n You'll Recieve Details through Gmail Soon\nThis is your \nUID:{}\nPASSWORD:{}".format(uid,pas),parent=signw)
                cam = cv2.VideoCapture(0)
                result, image = cam.read()
                if result:
                    cv2.imwrite("C:\\Users\\Joel\\Desktop\\LITEPAY\\Users\\{}.png".format(name),image)
                    cv2.waitKey(0)
                    print("Image captured...")
                signw.destroy()
            else:
                print("No")


    def checkotpf2(otp,window,uid):
        otps = otpgenerate(window)
        if otp=="":
            messagebox.showinfo("Incorrect Input!", "Enter OTP", parent=window)
        else:
            otp=int(otp)
        if(otp==otps):
            con = cx_Oracle.connect('system/joel@localhost:1521/xe')
            cur = con.cursor()
            cur.execute('select * from litepay where userid={}'.format(uid))
            li = [x for x in cur]
            phno = li[0][3]  # int
            gmail = li[0][2]
            pas = li[0][5]  # int
            f = open('password.txt', 'w')
            f.write(pas)
            messagebox.showinfo("Done!!","Credentials Verified!!",parent=window)
        else:
            messagebox.showinfo("Wrong Input!", "OTP didn't Matched!!",parent=window)


    def checkotpf(otp,window):
        otps = otpgenerate(window)
        if otp=="":
            messagebox.showinfo("Incorrect Input!", "Enter OTP", parent=window)
        else:
            otp=int(otp)
        if(otp==otps):
            messagebox.showinfo("Done!!","Credentials Verified!!",parent=window)
        else:
            messagebox.showinfo("Wrong Input!", "OTP didn't Matched!!",parent=window)

    def aboutweb(window):
        print('Opened About the developer website')
        window.after(1000,lambda:speak("This LITEPAY Application and Portfolio Website was Created by Mister Joel Mark Joseph S. He is a computer science major at PBR Vits and a passionate coder. He was born and brought up in Bitragunta, Andhra Pradesh, India"))
        webbrowser.open("D:\VITSCHOOL\My First Website Details(All about JMJ) 000webhost\index.html")

    def run(counter,word,lab):
        lab.config(text=word[:counter])
        if counter < len(word):
            win.after(100, lambda: run(counter + 1,word,lab))

    def ofcourseyes(window):
        window.destroy()
        mainf()

    def seticon(window):
        img = PhotoImage(file="C:\\Users\\Joel\\Desktop\\LITEPAY\\icon.png")
        window.iconphoto(False, img)
    
    def speak(text):
        v=tts.init()
        v.setProperty('rate',135)
        v.say(text)
        v.runAndWait()
    def mainf():
        global win
        win=tk.Tk()
        win.title("LITEPAY")
        win.state('zoomed')
        seticon(win)
        bgimg=ImageTk.PhotoImage(Image.open('C:\\Users\\Joel\\Desktop\\LITEPAY\\pybg.png'))  # "C:\Users\Joel\Desktop\pybg.png"
        limg=Label(win, i=bgimg)
        limg.pack()
        getstart=Button(command=getstarted,text="Get Started >",font=("Arial Rounded MT Bold",20),fg='white',bg='darkblue').place(x=100,y=475)
        Button(text="  Home  ",font=("Arial Rounded MT Bold",15),fg='blue',bg='white').place(x=860,y=50)
        Button(command=getstarted,text="  Login  ",font=("Arial Rounded MT Bold",15),fg='blue',bg='white').place(x=1130,y=50)
        Button(command=signup,text=" Signup ",font=("Arial Rounded MT Bold",15),fg='blue',bg='white').place(x=1000,y=50)
        Button(command=lambda:aboutweb(win),text=" About the Developer ",font=("Arial Rounded MT Bold",15),fg='blue',bg='white').place(x=1250,y=50)
        image = Image.open("C:\\Users\\Joel\\Desktop\\LITEPAY\\blue.png")
        resize_image = image.resize((550, 50))
        img = ImageTk.PhotoImage(resize_image)
        label = tk.Label(win, text='', image=img, compound='center', font=("Algerian", 35),fg='white')
        label.place(x=80,y=160)
        word = " WELCOME TO LITEPAY"
        win.after(50,lambda:speak("Welcome To Litepay,Make money Movable"))
        run(1,word,label)
        win.mainloop()

    #MAIN
    winsound.PlaySound("C:\\Users\\Joel\\Downloads\\Intromuzik.wav", winsound.SND_FILENAME)
    print("Played sound")
    mainf()