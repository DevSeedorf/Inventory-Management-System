from tkinter import *
from PIL import Image,ImageTk
import sqlite3
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from tkinter import messagebox
import os
import time
class IMS:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed By Seedorf")
        self.root.config(bg="#ddd")

        ##___title___##
        self.icon_title=Image.open("images/cart1.png")
        self.icon_title=self.icon_title.resize((90,70))
        self.icon_title=ImageTk.PhotoImage(self.icon_title)

        #self.icon_title=PhotoImage(file="images/cart1.png ")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("Century Gothic",30,"bold"),bg="#0080ff",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        ##__button_logout__##
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("Calibri",15,"bold"),bg="white",fg="#0080ff",bd=0,cursor="hand2").place(x=1150, y=10,height=50,width=150)

        ##__clock__##
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("Century Gothic",15,"bold"),bg="#0f4d7d",fg="white",anchor="w",padx=180)
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        ##__left menu__##
        self.Menulogo=Image.open("images/cart.png")
        self.Menulogo=self.Menulogo.resize((200,200))
        self.Menulogo=ImageTk.PhotoImage(self.Menulogo)
 
        leftmenu=Frame(self.root,bg="#ddd",bd=1,relief=RAISED)
        leftmenu.place(x=10,y=102,width=200,height=565)

        lbl_menulogo=Label(leftmenu,image=self.Menulogo,bg="#ddd")
        lbl_menulogo.pack(side=TOP,fill=X)

        lbl_menu=Label(leftmenu,text="Menu",font=("Century Gothic",18,"bold"),bg="#0080ff",fg="white").pack(side=TOP,fill=X)
        btn_employee=Button(leftmenu,text="Employee",command=self.employee,compound=LEFT,padx=5,anchor="w",font=("Calibri",18,"bold"),bg="#0080ff",fg="white",bd=1,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(leftmenu,text="Supplier",command=self.supplier,compound=LEFT,padx=5,anchor="w",font=("Calibri",18,"bold"),bg="#0080ff",fg="white",bd=1,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(leftmenu,text="Category",command=self.category,compound=LEFT,padx=5,anchor="w",font=("Calibri",18,"bold"),bg="#0080ff",fg="white",bd=1,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(leftmenu,text="Product",command=self.product,compound=LEFT,padx=5,anchor="w",font=("Calibri",18,"bold"),bg="#0080ff",fg="white",bd=1,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(leftmenu,text="Sales",command=self.sales,compound=LEFT,padx=5,anchor="w",font=("Calibri",18,"bold"),bg="#0080ff",fg="white",bd=1,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(leftmenu,text="Exit",compound=LEFT,padx=5,anchor="w",font=("Calibri",18,"bold"),bg="#0080ff",fg="white",bd=1,cursor="hand2").pack(side=TOP,fill=X)

        ##__content__##
        self.lbl_employee=Label(self.root,text="Total Employee\n[ 0 ]",bg="#0080ff",fg="white",font=("Century Gothic",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Supplier\n[ 0 ]",bg="#0080ff",fg="white",font=("Century Gothic",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Category\n[ 0 ]",bg="#0080ff",fg="white",font=("Century Gothic",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Product\n[ 0 ]",bg="#0080ff",fg="white",font=("Century Gothic",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n[ 0 ]",bg="#0080ff",fg="white",font=("Century Gothic",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)

        ##__footer__##
        lbl_footer=Label(self.root,text="Inventory Management System\nCall",font=("Century Gothic",15,"bold"),bg="#0080ff",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()
#=====================================================================================================
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
    
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
    
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Products\n[ {str(len(product))} ]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))} ]')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total Categories\n[ {str(len(category))} ]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employees\n[ {str(len(employee))} ]')
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales [{str(bill)}]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d/%m/%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":        
    root=Tk()
    obj=IMS(root) 
    root.mainloop()
 