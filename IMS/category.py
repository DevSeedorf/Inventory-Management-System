from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox 
import sqlite3
class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed By Seedorf")
        self.root.config(bg="#ddd")
        self.root.focus_force()
        #=========================

        #All Variables===========
        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        ##__title__##
        lbl_title=Label(self.root,text="Manage Product Category",font=("Century Gothic",15,"bold"),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_name=Label(self.root,text="Enter Category Name",font=("Century Gothic",15,"bold"),bg="#ddd").place(x=50,y=80)
        txt_name=Entry(self.root,textvariable=self.var_name ,font=("Century Gothic",12,),bg="#fff").place(x=50,y=120,width=250)
        
        btn_add=Button(self.root,text="Add",command=self.add,font=("Century Gothic",12,"bold"),bg="#0080ff",fg="white",cursor="hand2").place(x=310,y=120,height=25)
        btn_del=Button(self.root,text="Delete",command=self.delete, font=("Century Gothic",12,"bold"),bg="#0080ff",fg="white",cursor="hand2").place(x=360,y=120,height=25)

         ##__Category Details__##
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=650,y=80,width=400,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.categoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        self.categoryTable.heading("cid",text="CID")
        self.categoryTable.heading("name",text="NAME")
                        
        self.categoryTable["show"]="headings"

        self.categoryTable.column("cid",width=90)
        self.categoryTable.column("name",width=100)
        self.categoryTable.pack(fill=BOTH,expand=1)
        self.categoryTable.bind("<ButtonRelease-1>",self.get_data)
        #self.show()

        ##__images__##
        self.im1=Image.open("images/cat1.png")
        self.im1=self.im1.resize((350,280))
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bg="#ddd")
        self.lbl_im1.place(x=150,y=200)

        self.im2=Image.open("images/cat2.png")
        self.im2=self.im2.resize((350,280))
        self.im2=ImageTk.PhotoImage(self.im2)
 
        self.lbl_im2=Label(self.root,image=self.im2,bg="#ddd")
        self.lbl_im2.place(x=580,y=200)

        self.show()
    
    def add(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category Must be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already Present, try different",parent=self.root)
                else:
                    cur.execute("Insert into category (name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)
    
    def show(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("select * from category")  
            rows=cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.categoryTable.focus()
        content=(self.categoryTable.item(f))
        row=content["values"]
        #print(row)
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Select Category Name",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Try again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)
    



if __name__=="__main__":        
    root=Tk()
    obj=categoryClass(root) 
    root.mainloop()