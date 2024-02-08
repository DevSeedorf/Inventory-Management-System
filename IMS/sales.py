from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox 
import sqlite3
import os
class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed By Seedorf")
        self.root.config(bg="#ddd")
        self.root.focus_force()
        #=========================
        self.bill_list=[]
        self.var_invoice=StringVar()

        ##__title__##
        lbl_title=Label(self.root,text="View Customer Bill",font=("Century Gothic",15,"bold"),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root,text="Invoice No.",font=("Century Gothic",12,"bold"),bg="#ddd").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("Century Gothic",12)).place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Search",command=self.search,font=("Calibri",15,"bold"),bg="#0080ff",fg="white",cursor="hand2",bd=0).place(x=340,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("Calibri",15,"bold"),bg="#0080ff",fg="white",cursor="hand2",bd=0).place(x=470,y=100,width=120,height=28)

        ####Bill List####
        salesFrame=Frame(self.root,bd=1,relief=RIDGE)
        salesFrame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(salesFrame,orient=VERTICAL)
        self.sales_list=Listbox(salesFrame,font=("Century Gothic",12),yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH,expand=1)
        self.sales_list.bind("<ButtonRelease-1>",self.get_data)

        ####Bill Area####
        billFrame=Frame(self.root,bd=1,relief=RIDGE)
        billFrame.place(x=280,y=140,width=410,height=330)

        lbl_title2=Label(billFrame,text="Customer Bill Area",font=("Century Gothic",15,"bold"),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        scrolly2=Scrollbar(billFrame,orient=VERTICAL)
        self.bill_area=Text(billFrame,yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        ##__Images__##
        self.bill_image=Image.open("images/cart.png")
        self.bill_image=self.bill_image.resize((380,300))
        self.bill_image=ImageTk.PhotoImage(self.bill_image)

        lbl_image=Label(self.root,image=self.bill_image,bd=0)
        lbl_image.place(x=700,y=110)

        self.show()
#=============================================================
    
    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0,END)
        for i in os.listdir("bill"):
            if i.split(".")[-1]=="txt":
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split(".")[0])
    
    def get_data(self,ev):
        index=self.sales_list.curselection()
        file_name=self.sales_list.get(index)
        self.bill_area.delete("1.0",END)
        fp=open(f"bill/{file_name}","r")
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice No. Required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f"bill/{self.var_invoice.get()}.txt","r")
                self.bill_area.delete("1.0",END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invoice No. Not Found",parent=self.root)


    def clear(self):
        self.show()
        self.bill_area.delete("1.0",END)


if __name__=="__main__":        
    root=Tk()
    obj=salesClass(root) 
    root.mainloop()