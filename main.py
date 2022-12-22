import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as my

from tkinter import *

mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
mycursor = mysqldb.cursor()

mycursor.execute("create database if not exists gym_mgmt")
mycursor.execute("use gym_mgmt")

# creating the tables we need


# creation of trainer table to reference it later in main member table
mycursor.execute(
    "create table if not exists Trainer_det(t_id int primary key, t_name varchar(30) ,t_level int ,"
    "age int,address varchar(30),contact varchar(15),monthly_salary int(10))")

# creation of different package table to reference it later in main member table
mycursor.execute("create table if not exists Sub_det(sub_id int primary key, sub_name varchar(30)  ,sub_price float) ")

# creation of member details table with fk as trainer id and package id
mycursor.execute(
    "create table if not exists Mem_details(mem_id int primary key, f_name varchar(20),l_name varchar(20),"
    " sex varchar(15),age int,address varchar(50),contact varchar(15),pkg_id int,tr_id int,"
    "FOREIGN KEY (pkg_id) REFERENCES Sub_det(sub_id),FOREIGN KEY (tr_id) REFERENCES Trainer_det(t_id))")


#
# # creating table for storing the username and password of the user
# mycursor.execute(
#     "create table if not exists user_data(username varchar(30) primary key,password varchar(30) default'000')")


# Functionality for member page

def getValue(event=""):
    for i in (e1, e2, e3, e4, e5, e6, e7, e8, e9):
        i.delete(0, END)
    row_id = listBox.selection()[0]
    select = listBox.set(row_id)
    e1.insert(0, select['Mem id'])
    e2.insert(0, select['First name'])
    e3.insert(0, select['Last name'])
    e4.insert(0, select['Gender'])
    e5.insert(0, select['Age'])
    e6.insert(0, select['Location'])
    e7.insert(0, select['Contact'])
    e8.insert(0, select['Pkg Id'])
    e9.insert(0, select['Trainer Id'])


# cols = ('Mem id', 'First name', 'Last name', 'Gender', 'Age', 'Location', 'Contact', 'Pkg Id', 'Trainer Id')
# cols = ('Member id', 'First name', 'Last name', 'Gender', 'Contact', 'Subscription Id', 'Trainer Id')


def add_member():
    Mem_id = e1.get()
    first = e2.get()
    last = e3.get()
    gender = e4.get()
    age = e5.get()
    loaction = e6.get()
    mobile = e7.get()
    plan = e8.get()
    trainer = e9.get()

    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()

    try:
        sql = "insert into mem_details (mem_id , f_name ,l_name ,sex ,age ,address ,contact ,pkg_id ,tr_id ) " \
              "value(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (Mem_id, first, last, gender, age, loaction, mobile, plan, trainer)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Employee inserted successfully")
        # e1.delete(0, END)
        # e2.delete(0, END)
        # e3.delete(0, END)
        # e4.delete(0, END)
        for i in (e1, e2, e3, e4, e5, e6, e7, e8, e9):
            i.delete(0, END)
        e1.focus_set()

    except Exception as e:
        print(e)
        messagebox.showwarning("                        Input error",
                               "        Duplicate Id number or \nRecords not inserted completely")
        mysqldb.rollback()
        mysqldb.close()


def delete_member():
    Mem_id = e1.get()
    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()

    try:
        sql = "delete from mem_details where mem_id = %s"
        val = (Mem_id,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Record deleted successfully")
        for i in (e1, e2, e3, e4, e5, e6, e7, e8, e9):
            i.delete(0, END)
        e1.focus_set()

    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()


def search_member():
    for item in listBox.get_children():
        listBox.delete(item)
    Mem_id = e1.get()

    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()
    mycursor.execute(
        "select mem_id , f_name ,l_name ,sex  ,contact ,pkg_id ,tr_id from mem_details where mem_id = '" + Mem_id + "'")
    records = mycursor.fetchall()
    if len(records) == 1:
        print(records)
        for i, (mem_id, f_name, l_name, Gender, contact, pkg_id, tr_id) in enumerate(records, start=0):
            listBox.insert("", 'end', values=(mem_id, f_name, l_name, Gender, contact, pkg_id, tr_id))
            mysqldb.close()

    else:
        messagebox.showwarning("Input error", "Id not found")


def show_all_member():
    for item in listBox.get_children():
        listBox.delete(item)
    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()
    mycursor.execute("select * from mem_details")
    records = mycursor.fetchall()

    print(records)
    for i, (mem_id, f_name, l_name, Gender, age, address, contact, pkg_id, tr_id) in enumerate(records, start=0):
        listBox.insert("", 'end', values=(mem_id, f_name, l_name, Gender, age, address, contact, pkg_id, tr_id))
        mysqldb.close()


def show_frame(frame):
    frame.tkraise()


def show_all_trainer_on_main():
    for item in listBox_trainer2.get_children():
        listBox_trainer2.delete(item)
    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()
    mycursor.execute("select t_id,t_name from trainer_det")
    records = mycursor.fetchall()
    print(records)
    for i, (t_id, t_name) in enumerate(records, start=0):
        listBox_trainer2.insert("", 'end', values=(t_id, t_name))
        mysqldb.close()


def show_all_package_on_main():
    for item in listBox_package2.get_children():
        listBox_package2.delete(item)
    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()
    mycursor.execute("select * from  sub_det")
    records = mycursor.fetchall()

    print(records)
    for i, (sub_id, sub_name, sub_price) in enumerate(records, start=0):
        listBox_package2.insert("", 'end', values=(sub_id, sub_name, sub_price))
        mysqldb.close()


def refresh_all():
    show_all_trainer_on_main()
    show_all_package_on_main()
    show_all_member()


# functionality for trainer page

def getValueTrainer(event=""):
    for i in (e11, e12, e13, e14, e15, e16, e17):
        i.delete(0, END)
    row_id = listBox_trainer.selection()[0]
    select = listBox_trainer.set(row_id)
    e11.insert(0, select['Trainer ID'])
    e12.insert(0, select['Trainer Name'])
    e13.insert(0, select['Trainer Level '])
    e14.insert(0, select['Age'])
    e15.insert(0, select['Address'])
    e16.insert(0, select['Contact'])
    e17.insert(0, select['Monthly Salary'])


# cols = ('Trainer ID', 'Trainer Name', 'Trainer Level ', 'Age', 'Address', 'Contact', 'Monthly Salary')

def add_trainer():
    t_id = e11.get()
    t_name = e12.get()
    t_level = e13.get()
    age = e14.get()
    address = e15.get()
    contact = e16.get()
    monthly_salary = e17.get()

    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()

    try:
        sql = "insert into trainer_det (t_id , t_name ,t_level ,age ,address ,contact ,monthly_salary ) " \
              "values(%s,%s,%s,%s,%s,%s,%s)"
        val = (t_id, t_name, t_level, age, address, contact, monthly_salary)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Employee inserted successfully")

        for i in (e11, e12, e13, e14, e15, e16, e17):
            i.delete(0, END)
        e11.focus_set()

    except Exception as e:
        print(e)
        messagebox.showwarning("                        Input error",
                               "        Duplicate Id number or \nRecords not inserted completely")
        mysqldb.rollback()
        mysqldb.close()


def delete_trainer():
    t_id = e11.get()
    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()

    try:
        sql = "delete from trainer_det where t_id = %s"
        val = (t_id,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Record deleted successfully")
        for i in (e11, e12, e13, e14, e15, e16, e17):
            i.delete(0, END)
        e1.focus_set()

    except Exception as e:
        print(e)
        messagebox.showerror("Trainer assigned to Member",
                             "Cannot delete trainer who is assigned to member \nKindly change trainer Id in main page for respective users.")
        mysqldb.rollback()
        mysqldb.close()


def search_trainer():
    for item in listBox_trainer.get_children():
        listBox_trainer.delete(item)
    t_id = e11.get()

    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()
    mycursor.execute("select * from trainer_det where t_id = '" + t_id + "'")
    records = mycursor.fetchall()
    if len(records) == 1:
        print(records)
        for i, (t_id, t_name, t_level, age, address, contact, monthly_salary) in enumerate(records, start=0):
            listBox_trainer.insert("", 'end', values=(t_id, t_name, t_level, age, address, contact, monthly_salary))
            mysqldb.close()
    #
    else:
        messagebox.showwarning("Input error", "Id not found")


def show_all_trainer():
    for item in listBox_trainer.get_children():
        listBox_trainer.delete(item)
    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()
    mycursor.execute("select * from trainer_det")
    records = mycursor.fetchall()

    print(records)
    for i, (t_id, t_name, t_level, age, address, contact, monthly_salary) in enumerate(records, start=0):
        listBox_trainer.insert("", 'end', values=(t_id, t_name, t_level, age, address, contact, monthly_salary))
        mysqldb.close()


# Functionality for package page


# cols = ('Subscription Id', 'Subscription Name ', 'Subscription Cost')
def getValuePackage(event=""):
    for i in (e21, e22, e23):
        i.delete(0, END)
    row_id = listBox_package.selection()[0]
    select = listBox_package.set(row_id)
    e21.insert(0, select['Subscription Id'])
    e22.insert(0, select['Subscription Name '])
    e23.insert(0, select['Subscription Cost'])


def add_package():
    sub_id = e21.get()
    sub_name = e22.get()
    sub_price = e23.get()

    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()

    try:
        sql = "insert into sub_det (sub_id, sub_name, sub_price ) " \
              "values(%s,%s,%s)"
        val = (sub_id, sub_name, sub_price)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Employee inserted successfully")

        for i in (e21, e22, e23):
            i.delete(0, END)
        e11.focus_set()

    except Exception as e:
        print(e)
        messagebox.showwarning("                        Input error",
                               "   Duplicate Id number or \nRecords not inserted completely")
        mysqldb.rollback()
        mysqldb.close()


def delete_package():
    package_id = e21.get()
    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()

    try:
        sql = "delete from sub_det where sub_id = %s"
        val = (package_id,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Record deleted successfully")
        for i in (e21, e22, e23):
            i.delete(0, END)
        e1.focus_set()

    except Exception as e:
        print(e)
        messagebox.showerror("Subscription linked to USER", "The selected Package is linked to members")
        mysqldb.rollback()
        mysqldb.close()


def search_package():
    for item in listBox_package.get_children():
        listBox_package.delete(item)
    package_id = e21.get()

    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()
    mycursor.execute("select * from sub_det where sub_id = '" + package_id + "'")
    records = mycursor.fetchall()
    if len(records) == 1:
        print(records)
        for i, (sub_id, sub_name, sub_price) in enumerate(records, start=0):
            listBox_package.insert("", 'end', values=(sub_id, sub_name, sub_price))
            mysqldb.close()
    #
    else:
        messagebox.showwarning("Input error", "Id not found")


def show_all_package():
    for item in listBox_package.get_children():
        listBox_package.delete(item)
    mysqldb = my.connect(host='localhost', user='root', password='root', database='gym_mgmt')
    mycursor = mysqldb.cursor()
    mycursor.execute("select * from  sub_det")
    records = mycursor.fetchall()

    print(records)
    for i, (sub_id, sub_name, sub_price) in enumerate(records, start=0):
        listBox_package.insert("", 'end', values=(sub_id, sub_name, sub_price))
        mysqldb.close()


window = tk.Tk()
window.title('Prime Fitness Club')
window.geometry('970x750')
window.configure(bg="#e4d9ff")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

Main_page = tk.Frame(window, bg="#f0e6ef")
Trainer_page = tk.Frame(window, bg="#1e2749")
Package_page = tk.Frame(window, bg="#0b3954")

for frame in (Main_page, Trainer_page, Package_page):
    frame.grid(row=0, column=0, sticky='nsew')

# #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Main Page code #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

lbl1 = tk.Label(Main_page, text='PRIME FITNESS CLUB', font='times 30 bold', bg='#f0e6ef', fg='#332e3c')
lbl1.place(x=10, y=5)
lblNote = tk.Label(Main_page,
                   text='Note- You can add new packages and Trainers by going their respective pages.'
                        ' \n Refresh is needed after adding records.',
                   font='times 15 bold', bg='#f0e6ef', fg='#332e3c')
lblNote.place(x=15, y=690)

# #----------------------------- buttons in Main page-----------------


# add button allows us to add new the member from database
add_member_btn = tk.Button(Main_page, text='Add Member', padx=79, pady=7, bd=7, bg="#036370", font='times 14 ',
                           fg='white',
                           command=add_member)
add_member_btn.place(x=655, y=225)

# search button allows us to search the member from database
search_member_btn = tk.Button(Main_page, text='Search Member', padx=70, pady=7, bd=7, font='times 14 ', bg="#087e8b",
                              fg='white',
                              command=search_member)
search_member_btn.place(x=655, y=85)

# delete button allows us to delete the member from database
delete_member_btn = tk.Button(Main_page, text='Delete member', padx=72, pady=7, bd=7, font='times 14 ', bg="#087e8b",
                              fg='white',
                              command=delete_member)
delete_member_btn.place(x=655, y=85 + 85 - 15)

# add trainer btn redirects to trainer page
add_tr_btn = tk.Button(Main_page, text='Register new Trainer', padx=7, pady=15, bd=7, font='times 14 ', bg="#06616b",
                       fg='white',
                       command=lambda: show_frame(Trainer_page))
add_tr_btn.place(x=750, y=520)

# add pkg btn redirects to package page
add_pkg_btn = tk.Button(Main_page, text='Register new Package', padx=3, pady=15, bd=7, font='times 14 ', bg="#06616b",
                        fg='white',
                        command=lambda: show_frame(Package_page))
add_pkg_btn.place(x=750, y=610)

# #------------------------- Entry box and labels ----------------------------------
lbl4 = tk.Label(Main_page, text=" Add details here", font='times 17 bold', bg='#f0e6ef', fg='#332e3c')
lbl4.place(x=15, y=60)

tk.Label(Main_page, text='Member Id', bg='#f0e6ef', fg='#332e3c', font='times 13 bold').place(x=20, y=120 - 20)
tk.Label(Main_page, text='First Name', bg='#f0e6ef', fg='#332e3c', font='times 13 bold').place(x=20, y=160 - 20)
tk.Label(Main_page, text="Last Name", bg='#f0e6ef', fg='#332e3c', font='times 13 bold').place(x=20, y=200 - 20)
tk.Label(Main_page, text="Gender", bg='#f0e6ef', fg='#332e3c', font='times 13 bold').place(x=20, y=240 - 20)
tk.Label(Main_page, text="Age", bg='#f0e6ef', fg='#332e3c', font='times 13 bold').place(x=350, y=120 - 20)
tk.Label(Main_page, text="Location", bg='#f0e6ef', fg='#332e3c', font='times 13 bold').place(x=350, y=160 - 20)
tk.Label(Main_page, text="Contact", bg='#f0e6ef', fg='#332e3c', font='times 13 bold').place(x=350, y=200 - 20)
tk.Label(Main_page, text="Plan Id", bg='#f0e6ef', fg='#332e3c', font='times 13 bold').place(x=350, y=240 - 20)
tk.Label(Main_page, text="Trainer Id", bg='#f0e6ef', fg='#332e3c', font='times 12 bold').place(x=347, y=280 - 20)

e1 = Entry(Main_page, bg='#284b63', font='times 13 bold', fg="white")
e1.place(x=140, y=120 - 20)

e2 = Entry(Main_page, bg='#284b63', font='times 13 bold', fg="white")
e2.place(x=140, y=160 - 20)

e3 = Entry(Main_page, bg='#284b63', font='times 13 bold', fg="white")
e3.place(x=140, y=200 - 20)

e4 = Entry(Main_page, bg='#284b63', font='times 13 bold', fg="white")
e4.place(x=140, y=240 - 20)

e5 = Entry(Main_page, bg='#284b63', font='times 13 bold', fg="white")
e5.place(x=430, y=120 - 20)

e6 = Entry(Main_page, bg='#284b63', font='times 13 bold', fg="white")
e6.place(x=430, y=160 - 20)

e7 = Entry(Main_page, bg='#284b63', font='times 13 bold', fg="white")
e7.place(x=430, y=200 - 20)

e8 = Entry(Main_page, bg='#284b63', font='times 13 bold', fg="white")
e8.place(x=430, y=240 - 20)

e9 = Entry(Main_page, bg='#284b63', font='times 13 bold', fg="white")
e9.place(x=430, y=280 - 20)

# #------------------- Tree view Main -------------------------
Tree_view_Main_label = Label(Main_page, text=" Membership details", font='times 20 bold', bg='#f0e6ef', fg='#332e3c')
Tree_view_Main_label.place(x=15, y=260)
cols = ('Mem id', 'First name', 'Last name', 'Gender', 'Age', 'Location', 'Contact', 'Pkg Id', 'Trainer Id')
listBox = ttk.Treeview(Main_page, columns=cols, show='headings', height=8)
for col in cols:
    listBox.heading(col, text=col)
listBox.grid(row=1, column=0, columnspan=2)

# center aligning Items

for i in range(9):
    listBox.column(cols[i], anchor="c")

# Setting The size of columns
cols2 = ('First name', 'Last name', 'Gender', 'Location', 'Contact')
for col in cols2:
    listBox.column(col, minwidth=0, width=120)
listBox.place(x=15, y=300)

cols3 = ('Mem id', 'Gender', 'Age', 'Pkg Id', 'Trainer Id')
for col in cols3:
    listBox.column(col, minwidth=0, width=90)

listBox.bind('<Double-Button-1>', getValue)

# #xxxxxxxxxxxxxxxxxxxxxxx Tree view trainer for main page ##################
Tree_view_trainer_label = Label(Main_page, text=" Trainer Details", font='times 15 bold', bg='#f0e6ef', fg='#332e3c')
Tree_view_trainer_label.place(x=450, y=490)
# cols = ('Trainer ID', 'Trainer Name', 'Trainer Level ', 'Age', 'Address', 'Contact', 'Monthly Salary')
cols = ('Trainer ID', 'Trainer Name')
listBox_trainer2 = ttk.Treeview(Main_page, columns=cols, show='headings', height=7)

for col in cols:
    listBox_trainer2.heading(col, text=col)
listBox_trainer2.grid(row=1, column=0)

# setting column width
for col in cols:
    listBox_trainer2.column(col, minwidth=0, width=130)

listBox_trainer2.place(x=450, y=520)

# center aligning Items
for i in range(len(cols)):
    listBox_trainer2.column(cols[i], anchor="c")

# #------------------- Tree view package details for main window-------------------------
Tree_view_pkg_label = Label(Main_page, text=" Package Details", font='times 15 bold', bg='#f0e6ef', fg='#332e3c')
Tree_view_pkg_label.place(x=15, y=495)
cols = ('sub_id', 'sub_name', 'sub_price')
listBox_package2 = ttk.Treeview(Main_page, columns=cols, show='headings', height=7)

for col in cols:
    listBox_package2.heading(col, text=col)
listBox_package2.grid(row=1, column=0)

# setting column width
for col in cols:
    listBox_package2.column(col, minwidth=0, width=140)

listBox_package2.place(x=15, y=520)

# center aligning Items
for i in range(len(cols)):
    listBox_package2.column(cols[i], anchor="c")
# #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Add Trainer Page code #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxButtons in Trainer page #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


Trainer_page_btn = tk.Button(Trainer_page, text='Go to Main Page', padx=15, pady=3, fg="White", bg="#0b3954", bd=9,
                             font='times 16 bold',
                             command=lambda: show_frame(Main_page))
Trainer_page_btn.place(x=730, y=20)

# add button allows us to add new the trainer  from database
add_member_btn = tk.Button(Trainer_page, text='Add New Trainer ', padx=18, pady=20, fg="black", bg='#00afb9', bd=12,
                           font='times 16 bold',
                           command=add_trainer)
add_member_btn.place(x=40, y=270)

# search button allows us to search the trainer from database
search_member_btn = tk.Button(Trainer_page, text='Search trainer ', padx=15, pady=20, fg="black", bg='#00afb9', bd=12,
                              font='times 16 bold',
                              command=search_trainer)
search_member_btn.place(x=290, y=270)

# delete button allows us to delete the trainer  from database
delete_member_btn = tk.Button(Trainer_page, text='Delete trainer ', padx=15, pady=20, fg="black", bg='#00afb9', bd=12,
                              font='times 16 bold',
                              command=delete_trainer)
delete_member_btn.place(x=510, y=270)

# show_all button allows us to show all records in treeview
show_all_btn = tk.Button(Trainer_page, text='Refresh Records', padx=15, pady=20, fg="black", bg='#00afb9', bd=12,
                         font='times 16 bold',
                         command=show_all_trainer)
show_all_btn.place(x=730, y=270)

# t_id , t_name ,t_level ,age ,address ,contact ,monthly_salary
# #------------------------- Entry box and labels ----------------------------------

tk.Label(Trainer_page, text='Trainer Module  ', bg='#1e2749', fg='#e4d9ff', font='times 35 bold').place(x=20, y=5)
tk.Label(Trainer_page, text='Add new trainer: ', bg='#1e2749', fg='#e4d9ff', font='times 15 bold').place(x=20, y=80)

tk.Label(Trainer_page, text='Trainer id', bg='#1e2749', fg='#e4d9ff', font='times 13 bold').place(x=20, y=120)
tk.Label(Trainer_page, text='Trainer Name', bg='#1e2749', fg='#e4d9ff', font='times 13 bold').place(x=20, y=160)
tk.Label(Trainer_page, text="Level", bg='#1e2749', fg='#e4d9ff', font='times 13 bold').place(x=350, y=120)
tk.Label(Trainer_page, text="Age", bg='#1e2749', fg='#e4d9ff', font='times 13 bold').place(x=350, y=160)
tk.Label(Trainer_page, text="Addresss", bg='#1e2749', fg='#e4d9ff', font='times 13 bold').place(x=630, y=120)
tk.Label(Trainer_page, text="Contact", bg='#1e2749', fg='#e4d9ff', font='times 13 bold').place(x=630, y=160)
tk.Label(Trainer_page, text="Salary", bg='#1e2749', fg='#e4d9ff', font='times 13 bold').place(x=20, y=200)

e11 = Entry(Trainer_page, bg='#00afb9', font='times 13 bold')
e11.place(x=140, y=120)

e12 = Entry(Trainer_page, bg='#00afb9', font='times 13 bold')
e12.place(x=140, y=160)

e13 = Entry(Trainer_page, bg='#00afb9', font='times 13 bold')
e13.place(x=420, y=120)

e14 = Entry(Trainer_page, bg='#00afb9', font='times 13 bold')
e14.place(x=420, y=160)

e15 = Entry(Trainer_page, bg='#00afb9', font='times 13 bold')
e15.place(x=740, y=120)

e16 = Entry(Trainer_page, bg='#00afb9', font='times 13 bold')
e16.place(x=740, y=160)

e17 = Entry(Trainer_page, bg='#00afb9', font='times 13 bold')
e17.place(x=140, y=200)
# #------------------- Tree view Trainer-------------------------
cols = ('Trainer ID', 'Trainer Name', 'Trainer Level ', 'Age', 'Address', 'Contact', 'Monthly Salary')
listBox_trainer = ttk.Treeview(Trainer_page, columns=cols, show='headings', height=10)

for col in cols:
    listBox_trainer.heading(col, text=col)
listBox_trainer.grid(row=1, column=0)

listBox_trainer.place(x=20, y=400)
listBox_trainer.bind('<Double-Button-1>', getValueTrainer)

# center aligning Items
for i in range(len(cols)):
    listBox_trainer.column(cols[i], anchor="c")

# setting column width
cols2 = ('Trainer Name', 'Trainer Level ', 'Address', 'Contact', 'Monthly Salary')
for col in cols2:
    listBox_trainer.column(col, minwidth=0, width=140)

# setting column width2
cols3 = ('Trainer ID', 'Age')
for col in cols3:
    listBox_trainer.column(col, minwidth=0, width=105)
# #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Add Package code #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Package_page_title = tk.Label(Package_page, text='package details', font='times 35', bg='green')
# Package_page_title.pack(fill='both', expand=True)

# #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxButtons in package page #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxFtra


package_page_btn = tk.Button(Package_page, text='Go to Main Page', bd=10, padx=13, pady=8, bg='#0F7562', fg='#ACF2B3',
                             font='times 17 bold',
                             command=lambda: show_frame(Main_page))
package_page_btn.place(x=640, y=100)

# search button allows us to search the package from database
search_package_btn = tk.Button(Package_page, text='Search package ', padx=15, pady=12, bg='#4A5D60', fg='#ACF2B3',
                               font='times 17 bold', bd=10,
                               command=search_package)
search_package_btn.place(x=340, y=280)

# add button allows us to add new the package  from database
add_pkg_btn = tk.Button(Package_page, text='Add new package ', padx=15, pady=12, bg='#4A5D60', fg='#ACF2B3',
                        font='times 17 bold', bd=10,
                        command=add_package)
add_pkg_btn.place(x=35, y=280)

# delete button allows us to delete the package  from database
delete_pkg_btn = tk.Button(Package_page, text='Delete Package ', padx=19, pady=12, bg='#4A5D60', fg='#ACF2B3',
                           font='times 17 bold', bd=10,
                           command=delete_package)
delete_pkg_btn.place(x=640, y=280)

# show_all button allows us to show all records in treeview
show_all_btn = tk.Button(Package_page, text='Refresh Data', padx=30, pady=3, bg='#457b9d', fg='#ACF2B3',
                         font='times 17 bold', bd=10,
                         command=show_all_package)
show_all_btn.place(x=640, y=400)

# #------------------------- Entry box and labels ----------------------------------

tk.Label(Package_page, text='SUBSCRIPTION PAGE ', bg='#0b3954', fg='#ACF2B3', font='times 35 bold',
         bd=10).place(x=240, y=15)

tk.Label(Package_page, text='Fill Package details here: ', bg='#0b3954', fg='#ACF2B3', font='times 17 bold',
         bd=10).place(x=90, y=85)

tk.Label(Package_page, text='Packge Details here: ', bg='#0b3954', fg='#ACF2B3', font='times 17 bold',
         bd=10).place(x=80, y=410)
tk.Label(Package_page, text='Package id', bg='#0b3954', fg='#ACF2B3', font='times 17 bold').place(x=30, y=140)
tk.Label(Package_page, text='Package Name', bg='#0b3954', fg='#ACF2B3', font='times 17 bold').place(x=30, y=180)
tk.Label(Package_page, text="Price", bg='#0b3954', fg='#ACF2B3', font='times 17 bold').place(x=30, y=220)

e21 = Entry(Package_page, bg='#20ECBA', font='times 13 bold')
e21.place(x=200, y=140)

e22 = Entry(Package_page, bg='#20ECBA', font='times 13 bold')
e22.place(x=200, y=180)

e23 = Entry(Package_page, bg='#20ECBA', font='times 13 bold')
e23.place(x=200, y=220)

# #------------------- Tree view package details -------------------------
#  sub_id, sub_name ,sub_price

cols = ('Subscription Id', 'Subscription Name ', 'Subscription Cost')
listBox_package = ttk.Treeview(Package_page, columns=cols, show='headings', height=8)

for col in cols:
    listBox_package.heading(col, text=col)
listBox_package.grid(row=1, column=0)

listBox_package.place(x=80, y=495)
listBox_package.bind('<Double-Button-1>', getValuePackage)

# center aligning Items
for i in range(len(cols)):
    listBox_package.column(cols[i], anchor="c")

# setting column width
for col in cols:
    listBox_package.column(col, minwidth=0, width=270)

# #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
show_all_trainer_on_main()
refresh_all()
show_frame(Main_page)

refresh_all_btn = tk.Button(Main_page, text='Refresh All Tables', padx=59, pady=7, bd=7, font='times 14 ', bg="#087e8b",
                            fg='white',
                            command=lambda: refresh_all())
refresh_all_btn.place(x=655, y=15)

# #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Treview Styling xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
tree = ttk.Treeview(window)
style = ttk.Style()
style.configure("Treeview", foreground='white', background="#5E5259", font='times 13 ', activebackground="black")
style.configure("Treeview.Heading", background="red", foreground='black', font='times 13 bold')
listBox_package.column(cols[0], anchor="c")

# scrollbar


window.mainloop()
