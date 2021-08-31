
#"""        $$      Student Library Management Syeyem       $$           """

#"""                       Using MySQL Database                           """


import mysql.connector
import pandas as pd
from datetime import date

conn=mysql.connector.connect(user='root',
                            host='localhost',
                            password='Yo1706gesh',
                            database='library_management_system'
                            )
dbms_obj=conn.cursor()


class one_time_load:

    def insert_library_books(self):
        dbms_obj.execute("USE library_management_system;")
        df_books=pd.read_csv("Library_books.csv")
        for p,q in df_books.iterrows():
            dbms_obj.execute(f"INSERT INTO library_books VALUES({q[0]},'{q[1]}','{q[2]}','{q[3]}','{q[4]}');")
            conn.commit()


    def insert_login_details(self):
        df_login=pd.read_csv("Login_Details.csv")
        dbms_obj.execute("USE Library_Management_System;")
        for p,q in df_login.iterrows():
            dbms_obj.execute(f"INSERT INTO login_details VALUES({q[0]},'{q[1]}',{q[2]});")
            conn.commit()


    def insert_borrowed_book(self):
        df_borrowed=pd.read_csv("Borrowed_book.csv")
        dbms_obj.execute("USE Library_Management_System;")
        for p,q in df_borrowed.iterrows():
            dbms_obj.execute(f"INSERT INTO borrowed_books VALUES({q[0]},{q[1]},'{q[2]}','{q[3]}');")
            conn.commit()


    def insert_returned_book(self):
        df_returned=pd.read_csv("Returned_book.csv")
        dbms_obj.execute("USE Library_Management_System;")
        for p,q in df_returned.iterrows():
            dbms_obj.execute(f"INSERT INTO returned_books VALUES({q[0]},{q[1]},'{q[2]}','{q[3]}');")
            conn.commit()


    def insert_librarian_details(self):
        df_lab_login=pd.read_csv("Librarian_Details.csv")
        dbms_obj.execute("USE Library_Management_System;")
        for p,q in df_lab_login.iterrows():
            dbms_obj.execute(f"INSERT INTO librarian_details VALUES({q[0]},'{q[1]}',{q[2]});")
            conn.commit()


    def insert_fine(self):
        t_fine=0
        dbms_obj.execute("SELECT Roll_No,Student_Name,Borrowed_Date,Returned_Date FROM borrowed_books,returned_books,login_details WHERE borrowed_books.Book_ID=returned_books.Book_ID AND borrowed_books.Student_ID=returned_books.Student_ID AND borrowed_books.Student_ID=login_details.Roll_No;")
        lines=dbms_obj.fetchall()
        for q in lines:
            bor_date=q[2]
            ret_date=q[3]
            m1=int(bor_date[3:5])
            d1=int(bor_date[:2])
            y1=int(bor_date[6:])
            m2=int(ret_date[3:5])
            d2=int(ret_date[:2])
            y2=int(ret_date[6:])
            bor_date=date(y1,m1,d1)
            ret_date=date(y2,m2,d2)
            diff=ret_date-bor_date
            diff=diff.days
            if diff>30:
                t_fine=diff-30
            dbms_obj.execute(f"INSERT INTO fine VALUES({q[0]},'{q[1]}',{t_fine});")
            conn.commit()

class Database(one_time_load):

    def clear_database(self):
        dbms_obj.execute("DROP DATABASE Library_Management_System;")
        conn.commit()

    def create_database(self):
        dbms_obj.execute("CREATE DATABASE Library_Management_System;")
        dbms_obj.execute("USE library_management_system;")

        dbms_obj.execute("CREATE TABLE library_books(Book_Id int,Book_name varchar(100),Author varchar(50),Genre varchar(50),SubGenre varchar(50));")
        dbms_obj.execute("CREATE TABLE borrowed_books(Book_ID int,Student_ID int,Book_name varchar(100),Borrowed_Date varchar(50));")
        dbms_obj.execute("CREATE TABLE returned_books(Book_ID int,Student_ID int,Book_name varchar(100),Returned_Date varchar(50));")
        dbms_obj.execute("CREATE TABLE login_details(Roll_No int,Student_Name varchar(50),Password varchar(50));")
        dbms_obj.execute("CREATE TABLE fine(Student_ID int,Student_name varchar(50),Total_Fine int);")
        dbms_obj.execute("CREATE TABLE librarian_details(Librarian_ID int,Librarian_name varchar(50),Password varchar(50));")
        conn.commit()

    def fetch_csv(self):
        self.insert_library_books()
        self.insert_borrowed_book()
        self.insert_returned_book()
        self.insert_login_details()
        self.insert_librarian_details()
        self.insert_fine()


class student(Database):

    Roll_No=None
    Stud_Name=None
    Librarian_ID=None
    
    def login(self,id,id_name,table):
        passwd=input("\nEnter Password :\n")
        try:
            dbms_obj.execute("USE Library_Management_System;")
            dbms_obj.execute(f"SELECT * FROM {table} WHERE {id_name}={id};")
        except:
            print("\nInvalid "+id_name)
            return 0
        db_pass=dbms_obj.fetchall()
        if passwd==db_pass[0][2]:
            print(f"\nHello '{db_pass[0][1]}'")
            if id_name=='Roll_No':
                self.Roll_No=id
                self.Stud_Name=db_pass[0][1]
            else:
                self.Librarian_ID=id
            return 1
        else:
            print("\nInvalid Password\n")
            return 0


    def Borrow_book(self):
        dbms_obj.execute("USE Library_Management_System;")
        dbms_obj.execute("SELECT * FROM library_books WHERE Book_id NOT IN(SELECT Book_ID FROM borrowed_books WHERE Book_ID NOT IN(SELECT Book_ID FROM returned_books));")

        for book in dbms_obj:
            print(book)

        while True:
            dbms_obj.execute("SELECT * FROM library_books WHERE Book_id NOT IN(SELECT Book_ID FROM borrowed_books WHERE Book_ID NOT IN(SELECT Book_ID FROM returned_books));")
            lines=dbms_obj.fetchall()
            b_id=int(input("\nEnter Book ID you want to borrow\n"))
            flag=0
            for book in lines:
                if b_id==book[0]:
                    print(f"You selected '{book[1]}'\n")
                    while True:
                        brwd_date=input("Enter Book Borrowed Date(format: dd/mm/yyyy)\n")
                        if len(brwd_date)==10:
                            dbms_obj.execute(f"INSERT INTO borrowed_books VALUES({book[0]},{self.Roll_No},'{book[1]}','{brwd_date}');")
                            conn.commit()
                            print(f"You borrowed '{book[1]}' book successfully !!!\n")
                            flag=1
                            break
                        else:
                            print("\nEnter date as per formate(dd/mm/yyyy)\n")
            if flag==0:
                print("\nID not exist ,Please select only from the List :\n")
            else:
                break
                                  

    def Return_book(self):
        dbms_obj.execute("USE Library_Management_System;")
        dbms_obj.execute("SELECT * from borrowed_books WHERE Book_ID NOT IN (SELECT Book_ID FROM returned_books);")
        lines=dbms_obj.fetchall()
        if True:
            b_id=int(input("\nEnter Book ID you want to Retrun\n"))
            f1=0
            f2=0
            for borrowed_id in lines:
                if b_id==borrowed_id[0]:
                    f1=1
                    if self.Roll_No==borrowed_id[1]:
                        f2=1
                        print(f"You are returning '{borrowed_id[2]}'\n")
                        while True:
                            rtnd_date=input("Enter Book Returned Date(format: dd/mm/yyyy)\n")
                            if len(rtnd_date)==10:
                                dbms_obj.execute(f"INSERT INTO returned_books VALUES({borrowed_id[0]},{self.Roll_No},'{borrowed_id[2]}','{rtnd_date}');")
                                conn.commit()
                                print(f"\n'{borrowed_id[2]}' Book returned successfully !!!\n")
                                break
                            else:
                                print("\nEnter date as per formate(dd/mm/yyyy)\n")
                    
            if f1==0:
                print("\nCan't return ,Book has not borrowed yet !!\n")
            elif f2==0:
                print(f"\nNo Borrowed record found against the Roll number '{self.Roll_No}'\n")
         

    def fine(self):
        t_fine=0
        dbms_obj.execute("USE Library_Management_System;")
        dbms_obj.execute(f"SELECT Roll_No,Student_Name,Borrowed_Date,Returned_Date FROM borrowed_books,returned_books,login_details WHERE borrowed_books.Book_ID=returned_books.Book_ID AND borrowed_books.Student_ID=returned_books.Student_ID AND borrowed_books.Student_ID=login_details.Roll_No AND borrowed_books.Student_ID={self.Roll_No};")
        lines=dbms_obj.fetchall()
        for line in lines:
            bor_date=line[2]
            ret_date=line[3]
            m1=int(bor_date[3:5])
            d1=int(bor_date[:2])
            y1=int(bor_date[6:])
            m2=int(ret_date[3:5])
            d2=int(ret_date[:2])
            y2=int(ret_date[6:])
            bor_date=date(y1,m1,d1)
            ret_date=date(y2,m2,d2)
            diff=ret_date-bor_date
            diff=diff.days
            if diff>30:
                t_fine=diff-30
            dbms_obj.execute(f"INSERT INTO fine VALUES({line[0]},'{line[1]}',{t_fine});")
            conn.commit()


    def show_fine(self):
        dbms_obj.execute("USE Library_Management_System;")
        dbms_obj.execute(f"SELECT SUM(Total_Fine) FROM fine WHERE Student_ID={stud.Roll_No};")
        line=dbms_obj.fetchall()
        print("\nTotal Fine including all books is :\t",line[0][0])


    def change_pass(self,table_name,user_id,ID):
        while True:
            new_pass=input("\nEnter New Password (Only 4 Integers):\n")
            if len(new_pass)!=4:
                print("\nInvalid New Password.only 4 Intergers are allowed.\n")
            else:                
                dbms_obj.execute("USE Library_Management_System;")
                dbms_obj.execute(f"UPDATE {table_name} SET Password={int(new_pass)} WHERE {user_id}={ID};")
                conn.commit()
                print("\nPassword Updated Successfully !!!\n")
                break


if __name__=="__main__":

    stud=student()

    while True:
        msg1="""\t$$    Login Page    $$\n \
            1.Student Login\n \
            2.Librarian Login\n \
            3.Administrator Login\n \
            4.Exit\n """
        print(msg1)
        i=int(input(""))
        
        if i==1:
            Roll_No=int(input("\nEnter Students Roll No :\n"))
            if stud.login(Roll_No,'Roll_No','login_details'):
                while True:
                    msg2="""\t$$    Student Profile    $$\n \
            1.Visit Library\n \
            2.Change Password\n \
            3.Logout\n """
                    print(msg2)
                    m=int(input(""))
                    if m==1:
                        while True:
                            msg3="""\t$$    Library Menu    $$\n \
            1.Borrow New Book\n \
            2.Return borrowed Book\n \
            3.Fine\n \
            4.Back to Student Profile\n"""
                            print(msg3)
                            n=int(input(""))
                            if n==1:
                                stud.Borrow_book()
                                    
                            if n==2:
                                stud.Return_book()
                                stud.fine()
                            
                            if n==3:
                                stud.show_fine()

                            if n==4:
                                break
                            if n==4:
                                break

                            x=int(input("Press 1 to Continue to Library Menu\n"))
                            if x!=1:
                                break                    

                    if m==2:
                        stud.change_pass('login_details','Roll_No',stud.Roll_No)
                                                
                    if m==3:
                        break
                    y=int(input("Press 1 to Continue to Student Profile System\n"))
                    if y!=1:
                        break

        if i==2:
            Librarian_ID=int(input("\nEnter Librarian ID :"))
            if stud.login(Librarian_ID,'Librarian_ID','librarian_details'):
                while True:
                    msg4="""\t$$    Librarian Profile    $$\n \
                1.Clear and Update Database\n \
                2.Change Password\n \
                3.Logout\n """
                    print(msg4)
                    n=int(input(""))

                    if n==1:
                        stud.clear_database()
                        stud.create_database()
                        stud.fetch_csv()
                        print("\nNew Database Updated Successfully !!!\n")

                    if n==2:
                        stud.change_pass('librarian_details','Librarian_ID',stud.Librarian_ID)

                    if n==3:
                        break
                    if n==3:
                        break

                    y=int(input("Press 1 to Continue to Librarian Profile\n"))
                    if y!=1:
                        break

        if i==3:
            ad_id=int(input("\nEnter Administator ID\n"))
            if ad_id==987654:                                # Administrator Login Details
                passwd=input("\nEnter Password\n")
                if passwd=='Admin':
                    print("Login Successful !!!")
                    print("\nPress 1 to Load Database\n")
                    i=int(input(""))
                    if i==1:
                        stud.create_database()
                        stud.fetch_csv()
                        print("\nNew Database Updated Successfully !!!\n")
                else:
                    print("Wrong Password\n")
            else:
                print("\nWrong ID\n")        

        if i==4:
            break
        
        j=int(input("Press 1 to Continue to Login Page\n"))
        if j!=1:
            break





