from tkinter import *
from tkinter import messagebox
import psycopg2

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
                password='postgres'
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
    def UpdateUserData(cls, column, column_value, username):
        if column == 'username':
            insert_query = 'UPDATE user_list SET ' + column + " = '" + column_value + "' WHERE username = '" + username + "';"
            cls.psqlCursor.execute(insert_query)
            cls.psqlConnection.commit()

        insert_query = 'UPDATE user_data SET ' + column + " = '" + column_value + "' WHERE username = '" + username + "';"
        cls.psqlCursor.execute(insert_query)
        cls.psqlConnection.commit()

    @classmethod
    def Register(cls, username, password):
        insert_query = "INSERT INTO user_list(username, user_password) VALUES(%s, %s);"
        cls.psqlCursor.execute(insert_query, (username, password))
        cls.psqlConnection.commit()
        insert_query = "INSERT INTO user_data(username) VALUES(%s);"
        cls.psqlCursor.execute(insert_query, (username,))
        cls.psqlConnection.commit()

    @classmethod
    def RetrieveData(cls, username):
        select_query = "SELECT * FROM user_data;"
        cls.psqlCursor.execute(select_query)
        user_records = cls.psqlCursor.fetchall()
        for user in user_records:
            if user[1]==username:
                return user

    @classmethod
    def ValidationUserList(cls, username, password):
        select_query = "SELECT * FROM user_list;"
        cls.psqlCursor.execute(select_query)
        user_records = cls.psqlCursor.fetchall()
        valid = False
        for user in user_records:
            if user[1]==username and user[2]==password:
                valid = True
        return valid

    @classmethod
    def ValidationUserData(cls, username):
        select_query = "SELECT * FROM user_data;"
        cls.psqlCursor.execute(select_query)
        user_records = cls.psqlCursor.fetchall()
        valid = False
        for user in user_records:
            if user[1]==username:
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

def register():
    global register_user_tk
    register_user_tk = Toplevel()
    register_user_tk.title("Register user")
    register_user_tk.geometry("300x250")
    register_user_tk.configure(bg="azure")

    global username
    global password
    username = StringVar()
    password = StringVar()

    Label(register_user_tk, bg="azure").pack()
    Label(register_user_tk, text="Username", font = "Verdana 10 bold", bg="azure").pack()
    username_entry = Entry(register_user_tk, textvariable=username).pack()
    Label(register_user_tk, text="Password", font = "Verdana 10 bold", bg="azure").pack()
    password_entry = Entry(register_user_tk, textvariable=password, show='*').pack()
    Label(register_user_tk, bg="azure").pack()
    Button(register_user_tk, text="Register", command=register_user, width=10, height=1, bg='pale turquoise', fg='dark slate gray', activebackground='dark slate gray', activeforeground='pale turquoise').pack()
    Label(register_user_tk, bg="azure").pack()
    Button(register_user_tk, text="Cancel", command=lambda: register_user_tk.destroy(), width=10, height=1, bg='light pink', fg='red4', activebackground='red4', activeforeground='light pink').pack()

def register_user():
    if username.get() and password.get():
        if Connector.NewUsername(username.get()) == True:
            messagebox.showwarning("Registration failed", "That username is already in use. \nPlease enter new username.")
        else:
            Connector.Register(username.get(), password.get())
            register_user_tk.destroy()
    else:
        messagebox.showwarning("Registration failed", "Please enter valid username and password.")

def login():
    global login_user_tk
    login_user_tk = Toplevel()
    login_user_tk.title("Login user")
    login_user_tk.geometry("300x250")
    login_user_tk.configure(bg="azure")

    global username
    global password
    username = StringVar()
    password = StringVar()

    Label(login_user_tk, bg="azure").pack()
    Label(login_user_tk, text="Username", font = "Verdana 10 bold", bg="azure").pack()
    username_entry = Entry(login_user_tk, textvariable=username).pack()
    Label(login_user_tk, text="Password", font = "Verdana 10 bold", bg="azure").pack()
    password_entry = Entry(login_user_tk, textvariable=password, show='*').pack()
    Label(login_user_tk, bg="azure").pack()
    Button(login_user_tk, text="Login", command=login_user, width=10, height=1, bg='pale turquoise', fg='dark slate gray', activebackground='dark slate gray', activeforeground='pale turquoise').pack()
    Label(login_user_tk, bg="azure").pack()
    Button(login_user_tk, text="Cancel", command=lambda: login_user_tk.destroy(), width=10, height=1, bg='light pink', fg='red4', activebackground='red4', activeforeground='light pink').pack()

def login_user():
    if Connector.ValidationUserList(username.get(), password.get()):
        login_user_tk.destroy()
        studomat_logged_screen()
    else:
        messagebox.showwarning("Login failed", "Please enter valid username and password.")

def edit():
    global edit_about_me
    edit_about_me = Toplevel()
    edit_about_me.geometry("500x600")
    edit_about_me.title("STUDOMAT - Edit data - " + username.get())
    edit_about_me.configure(bg="azure")

    global changed_username
    global first_name
    global last_name
    global age
    global course
    global marks

    changed_username = StringVar()
    first_name = StringVar()
    last_name = StringVar()
    age = IntVar()
    course = StringVar()
    marks = StringVar()

    Label(edit_about_me, bg="azure").pack()
    Label(edit_about_me, text="USERNAME", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
    changed_username_entry = Entry(edit_about_me, textvariable=changed_username).pack()
    Label(edit_about_me, bg="azure").pack()
    Label(edit_about_me, text="FIRST NAME", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
    first_name_entry = Entry(edit_about_me, textvariable=first_name).pack()
    Label(edit_about_me, bg="azure").pack()
    Label(edit_about_me, text="LAST NAME", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
    last_name_entry = Entry(edit_about_me, textvariable=last_name).pack()
    Label(edit_about_me, bg="azure").pack()
    Label(edit_about_me, text="AGE", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
    age_entry = Entry(edit_about_me, textvariable=age).pack()
    Label(edit_about_me, bg="azure").pack()
    Label(edit_about_me, text="COURSE", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
    course_entry = Entry(edit_about_me, textvariable=course).pack()
    Label(edit_about_me, bg="azure").pack()
    Label(edit_about_me, text="MARKS", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
    marks_entry = Entry(edit_about_me, textvariable=marks).pack()

    Label(edit_about_me, bg="azure").pack()
    Label(edit_about_me, bg="azure").pack()
    save_data_button = Button(edit_about_me, text="Save data", command=edit_data, width=10, height=1, bg='pale turquoise', fg='dark slate gray', activebackground='dark slate gray', activeforeground='pale turquoise').pack()
    Label(edit_about_me, bg="azure").pack()
    cancel_button = Button(edit_about_me, command=lambda: edit_about_me.destroy(), text = "Cancel", bg='light pink', fg='red4', activebackground='red4', activeforeground='light pink', width=10, height=1).pack()

def edit_data():
    global username
    if first_name.get() != "":
        Connector.UpdateUserData('first_name', first_name.get(), username.get())
    if last_name.get() != "":
        Connector.UpdateUserData('last_name', last_name.get(), username.get())
    if age.get() != 0:
        Connector.UpdateUserData('age', str(age.get()), username.get())
    if course.get() != "":
        Connector.UpdateUserData('course', course.get(), username.get())
    if marks.get() != "":
        Connector.UpdateUserData('marks', marks.get(), username.get())
        avg = 0
        for i in range(len(marks.get())):
            avg += int(marks.get()[i])
        avg = round(avg/len(marks.get()))
        avg = str(avg)
        Connector.UpdateUserData('avg_mark', avg, username.get())
    if changed_username.get() != "":
        Connector.UpdateUserData('username', changed_username.get(), username.get())
        username = changed_username

    edit_about_me.destroy()

def studomat_home_screen():
    Connector.Connect()
    global studomat
    studomat = Tk()
    studomat.geometry("300x250")
    studomat.title("STUDOMAT")
    studomat.configure(bg="azure")

    Label(studomat, bg="azure").pack()
    login_button = Button(studomat, text = "LOGIN", command=login, height="2", width="30", bg='pale turquoise', fg='dark slate gray', activebackground='dark slate gray', activeforeground='pale turquoise').pack()
    Label(studomat, bg="azure").pack()
    register_button = Button(studomat, text = "REGISTER", command=register, height="2", width="30", bg='pale turquoise', fg='dark slate gray', activebackground='dark slate gray', activeforeground='pale turquoise').pack()
    Label(studomat, bg="azure").pack()
    exit_the_app_button = Button(studomat, command=lambda: studomat.destroy(), text = "EXIT", height="2", width="30", bg='light pink', fg='red4', activebackground='red4', activeforeground='light pink').pack()

    studomat.mainloop()

def studomat_logged_screen():
    global logged
    logged = Tk()
    logged.geometry("500x250")
    logged.title("STUDOMAT - Welcome " + username.get())
    logged.configure(bg="azure")

    Label(logged, bg="azure").pack()
    list_data_button = Button(logged, text = "About you", command = about_me_screen, height="2", width="30", bg='pale turquoise', fg='dark slate gray', activebackground='dark slate gray', activeforeground='pale turquoise').pack()
    Label(logged, bg="azure").pack()
    edit_data_button = Button(logged, text = "Edit your data", command=edit, height="2", width="30", bg='pale turquoise', fg='dark slate gray', activebackground='dark slate gray', activeforeground='pale turquoise').pack()
    Label(logged, bg="azure").pack()
    exit_the_app_button = Button(logged, command=lambda: logged.destroy(), text = "EXIT", bg='light pink', fg='red4', activebackground='red4', activeforeground='light pink', height="2", width="30").pack()

    logged.mainloop()

def about_me_screen():
    global about_me
    about_me = Tk()
    about_me.geometry("500x600")
    about_me.title("STUDOMAT - About me - " + username.get())
    about_me.configure(bg="azure")

    u_marks = ""

    user_data = Connector.RetrieveData(username.get())
    if user_data:
        user_marks = user_data[6]
        if user_marks:
            for i in range(len(user_marks)):
                if i == len(user_marks)-1:
                    u_marks += str(user_marks[i])
                else:
                    u_marks = u_marks + str(user_marks[i]) + ", "

        Label(about_me, bg="azure").pack()
        Label(about_me, text="USERNAME", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, text=user_data[1], font = "Verdana 10 bold", bg="white", foreground = "DeepSkyBlue4", justify = "left", borderwidth=2, relief="groove", width=20, height=1).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="FIRST NAME", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, text=user_data[2], font = "Verdana 10 bold", bg="white", foreground = "DeepSkyBlue4", justify = "left", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="LAST NAME", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, text=user_data[3], font = "Verdana 10 bold", bg="white", foreground = "DeepSkyBlue4", justify = "left", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="AGE", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, text=user_data[4], font = "Verdana 10 bold", bg="white", foreground = "DeepSkyBlue4", justify = "left", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="COURSE", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, text=user_data[5], font = "Verdana 10 bold", bg="white", foreground = "DeepSkyBlue4", justify = "left", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="MARKS", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, text=u_marks, font = "Verdana 10 bold", bg="white", foreground = "DeepSkyBlue4", justify = "left", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="AVERAGE MARK", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, text=user_data[7], font = "Verdana 10 bold", bg="white", foreground = "DeepSkyBlue4", justify = "left", borderwidth=2, relief="groove", width=20).pack()

    else:
        Label(about_me, bg="azure").pack()
        Label(about_me, text="USERNAME", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, bg="white", borderwidth=2, relief="groove", width=20, height=1).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="FIRST NAME", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, bg="white", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="LAST NAME", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, bg="white", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="AGE", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, bg="white", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="COURSE", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, bg="white", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="MARKS", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, bg="white", borderwidth=2, relief="groove", width=20).pack()
        Label(about_me, bg="azure").pack()
        Label(about_me, text="AVERAGE MARK", font = "Verdana 10 bold", bg="azure", foreground = "DeepSkyBlue4", justify = "left").pack()
        Label(about_me, bg="white", borderwidth=2, relief="groove", width=20).pack()


    Label(about_me, bg="azure").pack()
    Label(about_me, bg="azure").pack()
    back_button = Button(about_me, command=lambda: about_me.destroy(), text = "Back", bg='light pink', fg='red4', activebackground='red4', activeforeground='light pink', width=10).pack()

    about_me.mainloop()

studomat_home_screen()
