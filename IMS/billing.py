from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
class billClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed By Seedorf")
        self.root.config(bg="#ddd")
        self.cartList=[]
        self.chk_print=0

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

        #==Product Frame==#
        ProductFrame1=Frame(self.root,bd=2,relief=RIDGE)
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame1,text="All Products",font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        #============Search Frame===========#
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=1,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("Century Gothic",12,"bold"),bg="white").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text="Product Name",font=("Century Gothic",12,"bold"),bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("Century Gothic",12)).place(x=125,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white",cursor="hand2").place(x=280,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white",cursor="hand2").place(x=280,y=10,width=100,height=25)

        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.productTable=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("pid",text="PID")
        self.productTable.heading("name",text="NAME")
        self.productTable.heading("price",text="PRICE")
        self.productTable.heading("qty",text="QTY")
        self.productTable.heading("status",text="STATUS")
                
        self.productTable["show"]="headings"

        self.productTable.column("pid",width=40)
        self.productTable.column("name",width=100)
        self.productTable.column("price",width=100)
        self.productTable.column("qty",width=40)
        self.productTable.column("status",width=90)
        self.productTable.pack(fill=BOTH,expand=1)
        self.productTable.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame1,text="Note: Enter 0 Quantity to remove product from the Cart",font=("Century Gothic",10),bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #====Customer Frame===#
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=2,relief=RIDGE)
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Customer Details",font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("Century Gothic",12,"bold")).place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("Century Gothic",12)).place(x=80,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("Century Gothic",12,"bold")).place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("Century Gothic",12)).place(x=380,y=35,width=140)
        
        Cal_CartFrame=Frame(self.root,bd=2,relief=RIDGE)
        Cal_CartFrame.place(x=420,y=190,width=530,height=360)

        #===Calculator Frame===#
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_CartFrame,bd=3,relief=RIDGE)
        Cal_Frame.place(x=5,y=10,width=260,height=340)

        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=("Calibri",12,"bold"),width=30,bd=4,relief=GROOVE,state="readonly",justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text="7",font=("Calibri",15,"bold"),command=lambda:self.get_input(7),bd=1,width=5,pady=18,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text="8",font=("Calibri",15,"bold"),command=lambda:self.get_input(8),bd=1,width=5,pady=18,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text="9",font=("Calibri",15,"bold"),command=lambda:self.get_input(9),bd=1,width=5,pady=18,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text="+",font=("Calibri",15,"bold"),command=lambda:self.get_input("+"),bd=1,width=5,pady=18,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text="4",font=("Calibri",15,"bold"),command=lambda:self.get_input(4),bd=1,width=5,pady=18,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text="5",font=("Calibri",15,"bold"),command=lambda:self.get_input(5),bd=1,width=5,pady=18,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text="6",font=("Calibri",15,"bold"),command=lambda:self.get_input(6),bd=1,width=5,pady=18,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text="-",font=("Calibri",15,"bold"),command=lambda:self.get_input("-"),bd=1,width=5,pady=18,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text="1",font=("Calibri",15,"bold"),command=lambda:self.get_input(1),bd=1,width=5,pady=18,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text="2",font=("Calibri",15,"bold"),command=lambda:self.get_input(2),bd=1,width=5,pady=18,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text="3",font=("Calibri",15,"bold"),command=lambda:self.get_input(3),bd=1,width=5,pady=18,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text="*",font=("Calibri",15,"bold"),command=lambda:self.get_input("*"),bd=1,width=5,pady=18,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text="0",font=("Calibri",15,"bold"),command=lambda:self.get_input(0),bd=1,width=5,pady=18,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text="C",font=("Calibri",15,"bold"),command=self.clear_cal,bd=1,width=5,pady=18,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text="=",font=("Calibri",15,"bold"),command=self.perform_cal,bd=1,width=5,pady=18,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text="/",font=("Calibri",15,"bold"),command=lambda:self.get_input("/"),bd=1,width=5,pady=18,cursor="hand2").grid(row=4,column=3)


        Cart_Frame=Frame(Cal_CartFrame,bd=3,relief=RIDGE)
        Cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(Cart_Frame,text="Cart \t Total Product: [0]",font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(Cart_Frame,orient=HORIZONTAL)

        self.cartTable=ttk.Treeview(Cart_Frame,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)

        self.cartTable.heading("pid",text="PID")
        self.cartTable.heading("name",text="NAME")
        self.cartTable.heading("price",text="PRICE")
        self.cartTable.heading("qty",text="QTY")
        self.cartTable.heading("status",text="STATUS")
        self.cartTable["show"]="headings"
        self.cartTable.column("pid",width=40)
        self.cartTable.column("name",width=100)
        self.cartTable.column("price",width=90)
        self.cartTable.column("qty",width=40)
        self.cartTable.column("status",width=90)
        self.cartTable.pack(fill=BOTH,expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        
        #==Add Cart Widget==#
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE)
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("Century Gothic",12,"bold")).place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("Century Gothic",12),bg="white",state="readonly").place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("Century Gothic",12,"bold")).place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("Century Gothic",12),bg="white",state="readonly").place(x=230,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("Century Gothic",12,"bold")).place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty ,font=("Century Gothic",12),bg="white").place(x=390,y=35,width=120,height=22)

        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="In Stock [999]",font=("Century Gothic",12,"bold"))
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white",cursor="hand2").place(x=180,y=70,width=100,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update",command=self.add_update_cart,font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white",cursor="hand2").place(x=340,y=70,width=150,height=30)

        #============Billing Area===========#
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=410,height=410)

        bTitle=Label(billFrame,text="Customer Bill",font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview) 

        #============Billing Buttons===========#
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=410,height=140)

        self.lbl_amnt=Label(billMenuFrame,text="Bill Amt\n[0]",font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(billMenuFrame,text="Discount\n[5%]",font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)


        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white",cursor="hand2")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white",cursor="hand2")
        btn_clear_all.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(billMenuFrame,text="Generate/Save Bill",command=self.generate_bill,font=("Century Gothic",12,"bold"),bg="#0f4d7d",fg="white",cursor="hand2")
        btn_generate.place(x=246,y=80,width=160,height=50)

        ##__footer__##
        lbl_footer=Label(self.root,text="Inventory Management System\nCall",font=("Century Gothic",15,"bold"),bg="#0080ff",fg="white").pack(side=BOTTOM,fill=X)

        self.show()
        #self.bill_top()
        self.update_date_time()

#==================All Functions=================#
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)
    
    def clear_cal(self):
        self.var_cal_input.set("")
    
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))


    def show(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")  
            rows=cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    
    def search(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search Input Required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status= 'Actice'")  
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert("",END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        # con=sqlite3.connect(database=r"ims.db")
        # cur=con.cursor()
        # cur.execute("select * from product")
        # rows=cur.fetchall()
        # for row in rows: 
            f=self.productTable.focus()
            content=(self.productTable.item(f))
            row=content['values']
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.lbl_inStock.config(text=f"In Stock[{str(row[3])}]")
            self.var_stock.set(row[3])
            self.var_qty.set('1')

    def get_data_cart(self,ev):
        f=self.cartTable.focus()
        content=(self.cartTable.item(f))
        row=content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])
    
    
    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please Select a Product",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root )
        else:
           # price_cal=int(self.var_qty.get())*float(self.var_price.get())
           # price_cal=float(price_cal)
            price_cal=self.var_price.get()

            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            self.cartList.append(cart_data)

            ####=========Update Cart=========####
            present='no'
            index_=0 
            for row in self.cartList:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=="no":
                op=messagebox.askyesno('Confirm',"Product Already Present\nDo you want to Update | Remove from the Cart",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cartList.pop(index_)
                    else:
                        self.cartList[index_][2]=price_cal
                        self.cartList[index_][3]=self.var_qty.get()
                #else:
                    #self.cartList.append(cart_data)
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cartList:
            self.bill_amnt=self.bill_amnt+float(row[2])*int(row[3])
        
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f"Bill Amt(Na.)\n[{str(self.bill_amnt)}]")
        self.lbl_net_pay.config(text=f"Net pay(Na.)\n[{str(self.net_pay)}]")
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cartList))}]")

    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cartList:
                self.cartTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Enter Customer Details",parent=self.root)
        elif len(self.cartList)==0:
            messagebox.showerror("Error",f"Please Add Product to Cart",parent=self.root)
        else:
            #======Bill Top=====#
            self.bill_top()
            #======Bill Middle=====#
            self.bill_middle()
            #======Bill Bottom=====#
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated",parent=self.root)
            self.chk_print=1
            #self.clear_all()


    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 98725****, Nigeria-125001
{str("="*47)}
 Customer Name: {self.var_cname.get()}
 Phone No: {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
    
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tNa.{self.bill_amnt}
 Discount\t\t\t\tNa.{self.discount}
 Net Pay\t\t\t\tNa.{self.net_pay}
{str("="*47)}\
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
    
    def bill_middle(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            for row in self.cartList:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'

                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tNa."+price)
                #
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid

                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    
    def clear_cart(self):
        self.var_pid.set=('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')
    
    def clear_all(self):
        del self.cartList[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0
    
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d/%m/%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)
    
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please generate bill",parent=self.root)
    
    def logout(self):
        self.root.destroy()
        os.system("python login.py")
    
   
if __name__=="__main__":        
    root=Tk()
    obj=billClass(root) 
    root.mainloop()