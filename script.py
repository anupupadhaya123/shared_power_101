import sqlite3
from tkinter import *
conn = sqlite3.connect('shared_power.db')
c = conn.cursor()

try:
    c.execute("""
                CREATE TABLE users(
                    username text,
                    email text,
                    fullname text,
                    password text,
                    address text,
                    phoneno integer
                )
            """)
except Exception as e:
    pass

try:
    c.execute("""
                CREATE TABLE tools(
                    tool_name text,
                    description text,
                    half_day_rate integer,
                    full_day_rate integer
                )
              """)
except Exception as e:
    pass

try:
    c.execute("""
                CREATE TABLE invoice(
                    description text,
                    quantity integer,
                    price integer,
                    total integer
                )
            """)
except Exception as e:
    pass

def check_user(username):
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if len(c.fetchall()) == 0:
        return True

def validate(username, password):
    c.execute("SELECT * FROM users WHERE username = ? ", (username, ))
    print(username)
    s = c.fetchall()
    print(s)
    if s[0][3] == password:
        return True

def register(username, email , password, fullname, address , phoneno, window):
    if username != '' and email != '' and password != '' and fullname != '' and address != '' and phoneno != 0:
        if check_user(username):
            c.execute("INSERT INTO users VALUES (?, ? , ? , ? , ?, ?)", (username, email, fullname, password, address, phoneno))
            print("registered")
            conn.commit()
            window.destroy()
            loginpage()
        else:
            print("User exists with this name")
    print("Empty fields")

def login(username, password,window):
    if username != '' and password != '':
        if validate(username, password):
            print('login')
            window.destroy()
            dashboard()
        else:
            print("Wrong password")




def loginpage():
    l = Login()

def register_page(window):
    window.destroy()
    b = HomePage()

def addtool(window):
    window.destroy()
    c = AddTool()

class HomePage:

    def __init__(self):
        window = Tk()
        window.geometry("300x500")
        username_label = Label(window, text="Username")
        username_label.pack()
        username_entry= Entry(window, text="Username")
        username_entry.pack()
        email_label = Label(window, text="Email")
        email_label.pack()
        email_entry = Entry(window)
        email_entry.pack()
        password_label = Label(window, text="Password")
        password_label.pack()
        password_entry = Entry(window, show="*")
        password_entry.pack()
        fullname_label = Label(window, text="Fullname")
        fullname_label.pack()
        fullname_entry = Entry(window)
        fullname_entry.pack()
        address_label=Label(window,text="Address")
        address_label.pack()
        address_entry=Entry(window)
        address_entry.pack()
        phoneno_label=Label(window,text="Phoneno")
        phoneno_label.pack()
        phoneno_entry=Entry(window)
        phoneno_entry.pack()
        register_button=Button(window,text="Register", command=lambda:register(username_entry.get(),
                                                                               email_entry.get(),
                                                                               password_entry.get(),
                                                                               fullname_entry.get(),
                                                                               address_entry.get(),
                                                                               phoneno_entry.get(),
                                                                               window))
        register_button.pack()
        window.mainloop()

class Login:

    def __init__(self):
        window = Tk()
        window.geometry("300x500")
        username_label = Label(window, text="Username")
        username_label.pack()
        username_entry= Entry(window, text="Username")
        username_entry.pack()
        password_label = Label(window, text="Password")
        password_label.pack()
        password_entry = Entry(window, show="*")
        password_entry.pack()
        login_button = Button(window, text="Login", command=lambda : login(username_entry.get(), password_entry.get(), window))
        login_button.pack()
        power = Button(window, text="Not registered , register here", command=lambda: register_page(window))
        power.pack()
        window.mainloop()

class Dashboard:

    def __init__(self):
        window = Tk()
        window.geometry('300x500')
        title = Label(window, text="Welcome to dashboard")
        button = Button(window, text="Add Tool" , command=lambda: addtool(window))
        button.pack()
        window.mainloop()

class AddTool:

    def __init__(self):
        window = Tk()
        window.geometry('300x500')
        tool_name_label = Label(window, text="tool's name")
        tool_name_label.pack()
        tool_name_entry = Entry(window)
        tool_name_entry.pack()
        description_label = Label(window, text="description")
        description_label.pack()
        description_entry = Entry(window)
        description_entry.pack()
        half_day_rate_label = Label(window , text="half day rate ")
        half_day_rate_label.pack()
        half_day_rate_entry = Entry(window)
        half_day_rate_entry.pack()
        full_day_rate_label = Label(window , text="Full day rate")
        full_day_rate_label.pack()
        full_day_rate_entry = Entry(window)
        full_day_rate_entry.pack()
        submit_button = Button(window , text="Submit", command=lambda: print("dsdsds"))
        submit_button.pack()


def dashboard():
    d = Dashboard()
loginpage()