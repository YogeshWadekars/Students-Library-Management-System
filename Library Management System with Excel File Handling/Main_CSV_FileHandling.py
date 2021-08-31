
#"""        $$      Student Library Management Syeyem       $$           """

#"""                       Using CSV File Handling                       """

import pandas as pd


class library:
    booked_id=None
    booked_name=None

    def books(self):
        df_book=pd.read_csv("Library_books.csv")
        print(df_book.to_string())
        b_id=int(input("Enter Book Id\n"))
        if b_id not in df_book['Book ID']:
            print("Please enter valid Book ID out of the given list")
            return 0
        else:
            for ind,itr in df_book.iterrows():
                if itr[0]==b_id:
                    nd=ind
            b_name=df_book.loc[nd ,'Book Name']
            self.booked_id=b_id
            self.booked_name=b_name
            return 1

class student(library):
    stud_id=None

    def login(self):
        id=int(input("Enter Student Id\n"))
        passwd=int(input("Enter Password\n"))

        df=pd.read_csv("Login_Details.csv")
        flag=0
        for p,q in df.iterrows():
            if q[0]==id and q[2]==passwd:
                print(f"Hello '{q[1]}'\n")
                flag=1
            else:
                continue
        if flag==0:
            print("Please Enter Valid Details\n")
            return 0
        else:
            self.stud_id=id
            return 1

    def Borrow_book(self,brwd_date):
        borrow=pd.read_csv("Borrowed_book.csv")
        borrow_dict={'Book ID':[self.booked_id] ,'Student ID':[self.stud_id],'Book Name':[self.booked_name],'Borrowed Date':[brwd_date]}
        temp_df=pd.DataFrame(borrow_dict)
        borrow.loc[len(borrow.index)]=temp_df.loc[0]
        borrow.to_csv("Borrowed_book.csv",index=False)
        print(f"\n'{self.booked_name}' Book Borrowed Successfully !!!\n")

    def Return_book(self,R_book_id,Returned_date):
        df_returned=pd.read_csv("Returned_book.csv")
        df_book=pd.read_csv("Library_books.csv")
        if R_book_id not in df_book['Book ID']:
            print(f"Please enter valid Book ID (No record for Book ID: {R_book_id})\n")
        else:
            for c,d in df_book.iterrows():
                if d[0]==R_book_id:
                    print(d[0],d[1])
                    b_name=d[1]
            temp_df=pd.DataFrame({'Book ID':[R_book_id],'Student ID':[self.stud_id],'Book Name':[b_name],'Returned Date':[Returned_date]})
            df_returned.loc[len(df_returned.index)]=temp_df.loc[0]
            df_returned.to_csv("Returned_book.csv",index=False)
            print(f"\n'{b_name}' Book Returned Successfully !!!\n")

    def Fine(self):
        pass

    def change_pass(self,new_pass):
        df_book=pd.read_csv("Login_Details.csv")
        flag=0
        for h,j in df_book.iterrows():
            if self.stud_id==j[0]:
                df_book.loc[h,'Password']=new_pass
                print("\nPassword Updated Successfully !!!\n")
                df_book.to_csv("Login_Details.csv",index=False)
                flag=1
        if flag==0:
            print("\nStudent ID not found.Please enter correct ID and try again.\n")

stud=student()

while True:
    msg1="""\t$$    Login Page    $$\n \
        1.Student Login\n \
        2.Exit\n """
    print(msg1)
    i=int(input(""))
    
    if i==1:
        if stud.login():
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
        3.Calculate total Fine\n \
        4.Back to Student Profile\n"""
                        print(msg3)
                        n=int(input(""))
                        if n==1:
                            if(stud.books()):
                                brwd_date=input("Enter Book Borrowed Date(format: dd/mm/yyyy)\n")
                                stud.Borrow_book(brwd_date)
                                
                        if n==2:
                            book_id=int(input("Enter Book Id\n"))                                
                            returned_date=input("Enter Book Returned Date(format: dd/mm/yyyy)\n")
                            stud.Return_book(book_id,returned_date)
                        
                        if n==3:
                            stud.Fine()

                        if n==4:
                            break

                        if n==4:break
                        x=int(input("Press 1 to Continue to Library Menu\n"))
                        if x!=1:
                            break                    

                if m==2:
                    while True:
                        new_pass=input("\nEnter New Password (Only 4 Integers):\n")
                        if len(new_pass)!=4:
                            print("\nInvalid New Password.only 4 Intergers are allowed.\n")
                        else:
                            stud.change_pass(int(new_pass))
                            break
                                               
                if m==3:
                    break
                y=int(input("Press 1 to Continue to Student Profile System\n"))
                if y!=1:
                    break

    if i==2:
        break
    
    j=int(input("Press 1 to Continue to Login Page\n"))
    if j!=1:
        break


