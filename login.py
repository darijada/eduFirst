import psycopg2
import time
import inspect
from datetime import datetime

class Connector:

    psqlConnection = None
    psqlCursor = None

    @classmethod
    def Connect(cls):
        try:
            cls.psqlConnection = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                host='localhost',
                password='odoo'
            )
            cls.psqlCursor = cls.psqlConnection.cursor()
        except:
            raise("Unable to connect to database.")

    @classmethod
    def Disconnect(cls):
        try:
            cls.psqlCursor.close()
            cls.psqlConnection.close()
        except:
            raise("Unable to disconnect.")


    @classmethod
    def Insert(cls, username, password):
        insert_query = "INSERT INTO user_list(username, user_password) VALUES(%s, %s);"
        cls.psqlCursor.execute(insert_query, (username,password))
        cls.psqlConnection.commit()

    @classmethod
    def Validation(cls, username, password):
        select_query = "SELECT * FROM user_list;"
        cls.psqlCursor.execute(select_query)
        user_records = cls.psqlCursor.fetchall()
        valid = False
        for user in user_records:
            if user[0]==username and user[1]==password:
                valid = True
        return valid

    @classmethod
    def NewUsername(cls, username):
        select_query = "SELECT * FROM user_list;"
        cls.psqlCursor.execute(select_query)
        user_records = cls.psqlCursor.fetchall()
        valid = False
        for user in user_records:
            if user[0]==username:
                valid = True
        return valid

def login():
    u_n = input("Enter username: ")
    u_pass = input("Enter password: ")

    if Connector.Validation(u_n, u_pass):
        return print("Succesful login!")
    else:
        print("\nYou entered wrong username or password. Please try again.\n")
        login()

def register():
    u_n = input("Enter username: ")

    if Connector.NewUsername(u_n):
        print("\nThat username is already in use. Please enter new username.\n")
        register()
    else:
        u_pass = input("Enter password: ")
        Connector.Insert(u_n, u_pass)
        print("\nSuccesful registration. Welcome!\n")

def home_screen():
    Connector.Connect()
    choice = int(input(("Hello!\nEnter 1 if you want to SIGN IN.\nEnter 2 if you want to SIGN UP.\n")))
    if choice==1:
        login()
    elif choice==2:
        register()
    else:
        print("\nYou entered option that doesn't exist. Please try again.\n")
        home_screen()
    Connector.Disconnect()


if __name__ == '__main__':
    home_screen()
l
