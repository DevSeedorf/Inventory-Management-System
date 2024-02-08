from tkinter import *
from PIL import Image,ImageTk
import sqlite3
from tkinter import messagebox
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import employee
class loginSystem:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed By Seedorf")
        self.root.config(bg="#ddd")
        self.root.resizable(False,False)

        ################
        self.employee=StringVar()
        self.password=StringVar()

        self.otp=''

        self.icon_title=Image.open("images/pc.png")
        self.icon_title=self.icon_title.resize((500,400))
        self.icon_title=ImageTk.PhotoImage(self.icon_title)
             
        image=Label(self.root,image=self.icon_title).place(x=50,y=70)

        frame=Frame(self.root,width=350,height=350,bg="white")
        frame.place(x=600,y=70)

        heading=Label(frame,text="Employee Login",fg="#57a1f8",bg="white",font=("Microsoft YaHei UI Bold",20,"bold"))
        heading.place(x=60, y=5)

        txt_user=Label(frame,text="Username",fg="#000",bg="white",font=("Century Gothic",12,"bold")).place(x=25, y=60)
        user=Entry(frame,textvariable=self.employee,width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        user.place(x=30, y=80)
        thick_line=Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)

        ###Password###
        txt_pass=Label(frame,text="Password",fg="#000",bg="white",font=("Century Gothic",12,"bold")).place(x=25, y=140)
        password=Entry(frame,textvariable=self.password,width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        password.place(x=30, y=160)
        thick_line=Frame(frame, width=295, height=2, bg="black").place(x=25, y=187)

        Button(frame, width=39, pady=7, text="Sign In",command=self.login, bg="#57a1f8", fg="white", border=0).place(x=35, y=220)
        Button(frame, width=39, pady=7, text="Forgot Password",command=self.forget_window, bg="#57a1f8", fg="white", border=0).place(x=35, y=270)

        label = Label(frame, text="Don't have an account?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
        label.place(x=75, y=310)

        sign_up= Button(frame, width=6, text="Sign Up", border=0, bg="white", cursor="hand2", fg="#57a1f8")
        sign_up.place(x=215, y=310)

    def login(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.employee.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"All fields are required",parent=self.root)
            else:
                cur.execute("select utype from employee where name=? AND pass=?",(self.employee.get(),self.password.get()))  
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"Invalid Username or Password",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def forget_window(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.employee.get()=="":
                messagebox.showerror('Error',"Username Required",parent=self.root)
            else:
                cur.execute("select email from employee where name=?",(self.employee.get(),))  
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid Username",parent=self.root)
                else:
                    #===Forgot Password===#
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_confirm_pass=StringVar()

                    chk=self.send_email(email[0])
                    if chk!='f':
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title('Reset Password')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text='Reset Password',font=('Century Gothic',12,"bold"),bg='blue',fg='#FFF').pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP Sent to Registered Email",font=("Century Gothic",12,"bold")).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("Century Gothic",12,)).place(x=20,y=100,width=250,height=30)
                        self.btn_reset=Button(self.forget_win,text="SUBMIT",command=self.validate_otp,font=("Century Gothic",12,"bold"),bg="blue",fg="#FFF",bd=0)
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        new_pass=Label(self.forget_win,text="Enter New Password",font=("Century Gothic",12,"bold")).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("Century Gothic",12,)).place(x=20,y=190,width=250,height=30)
                        
                        confirm_pass=Label(self.forget_win,text="Confirm New Password",font=("Century Gothic",12,"bold")).place(x=20,y=225)
                        txt_confirm_pass=Entry(self.forget_win,textvariable=self.var_confirm_pass,font=("Century Gothic",12,)).place(x=20,y=255,width=250,height=30)
                        
                        
                        self.btn_update=Button(self.forget_win,text="UPDATE",command=self.update_password,font=("Century Gothic",12,"bold"),bg="blue",fg="#FFF",bd=0)
                        self.btn_update.place(x=150,y=300,width=100,height=30)
                    else:
                        messagebox.showerror("Error","Connection Error, Try again",parent=self.root)


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_confirm_pass.get()=="":
            messagebox.showerror("Error","Password is Required",parent=self.forget_win)
        elif self.var_new_pass.get()!= self.var_confirm_pass.get():
            messagebox.showerror("Error","Password Must be the same",parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r"ims.db")
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where name=?",(self.var_new_pass.get(),self.employee.get()))
                con.commit()
                messagebox.showinfo("Success","Password Updated Successfully",parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP, Try Again",parent=self.forget_win)
    
    def send_email(self,to_):
        # Sender and receiver email addresses
        sender_email = "olalekan496@gmail.com"
        receiver_email = "saheedabdulganiyu01@gmail.com"
        password = "svqb ggko sops ntqx"

        # Create a MIME message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "IMS Password Reset OTP"

        # Email body
        self.otp=int(time.strftime("%H%M%S"))+int(time.strftime("%S"))
        body = f'Your Password Reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team'
        message.attach(MIMEText(body, "plain"))

        # Establish a secure connection with the SMTP server
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            # Log in to the email account
            server.login(sender_email, password)
            
            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())

   
if __name__=="__main__":        
    root=Tk()
    obj=loginSystem(root) 
    root.mainloop()
 