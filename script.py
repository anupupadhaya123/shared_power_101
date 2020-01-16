import sqlite3
from tkinter import *
conn = sqlite3.connect('shared_power.db')
c = conn.cursor()
CURRENT = []
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
                CREATE TABLE tools (
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
                    total integer,
                    username text,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            """)
except Exception as e:
    pass

try :
    c.execute("""
        CREATE TABLE BOOKS(
            username text,
            tool_name text,
            quantity integer,
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (tool_name) REFERENCES tools(tool_name),
            FOREIGN KEY(tool_quantity) REFERENCES tools(quantity)
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
            SESSION.append(username)
            window.destroy()
            dashboard()
        else:
            print("Wrong password")

def add_tool(tool_name , description, half_day_rate, full_day_rate, window):
    c.execute("""
                INSERT INTO tools VALUES(?, ? , ?, ?)
            """, (tool_name , description, half_day_rate, full_day_rate))
    conn.commit()
    window.destroy()
    dashboard()


def hire(username, tool_name, quantity=1,window):
    c.execute("""INSERT INTO books VALUES(?,?,?)""", (tools_name, quantity, username))
    conn.commit()
    print("{} is hired".format(tools_name))

    window.destroy()
    dashboard()

def register_page(window):
    window.destroy()
    b = HomePage()

def searchtool(tool_name, window):
    if tool_name is not None:
        c.execute("""SELECT * FROM tools WHERE tool_name=?""", (tool_name, ))
        a = c.fetchall()
        window.destroy()
        viewpage(a)

def return_tool(tool_name, window):
    c.execute("""SELECT * FROM books WHERE tool_name=?""", (tool_name, ))
    a = c.fetchall()
    c.execute("""SELECT * FROM tools WHERE tool_name=?""", (tool_name, ))
    b = c.fetchall()
    if len(a) == 1 and len(b) == 1:
        c.execute("""INSERT INTO invoice VALUES(? , ? , ? , ? )""", (tool_name, a[0][2], b[0][3], a[0][2] * b[0][3], CURRENT[0]))
        conn.commit()
        c.execute("""SELECT * FROM books WHERE tool_name=?""", (tool_name, ))
        c.delete()
        conn.commit()
    window.destroy()
    show_invoice()



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
        search_label = Entry(window)
        search_label.insert(0, 'SEARCH ITEM')
        search_label.pack()
        button1=Button(window,text='Search Tool',command=lambda: searchtool(search_label.get(),window))
        button1.pack()
        button2 = Button(window, text='Hired Tools' , command=lambda: hiretoolpage(window))
        gap = Label(window)
        gap.pack(pady=15)
        c.execute("""SELECT * FROM tools""")
        for i in c.fetchall():
            for k in i:
                label = Label(window, text=k)
                label.pack()
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
        submit_button = Button(window , text="Submit", command=lambda:add_tool(tool_name_entry.get(), description_entry.get(), 
                                                                                half_day_rate_entry.get(), full_day_rate_entry.get(), window)) 
        submit_button.pack()

class BookTool:

    def __init__(self):
        window=Tk()
        window.geometry('300x500')

class ViewPage:

    def __init__(self, data):
        window = Tk()
        window.geometry("300x500")
        for i in data:
            for k in i:
                label = Label(window, text=k)
                label.pack()
        hire_button = Button(window, text="Hire", command=lambda : hire(CURRENT[0], i[0][0]))

class HiredToolPage:

    def __init__(self):
        window = Tk()
        window.geometry('300x500')
        c.execute("""SELECT * FROM books WHERE username=?""", (SESSION[0], ))
        a = c.fetchall()
        for i in a:
            label = Label(window, text=i[1])
            label.pack()
            button = Button(window, text="Return" , command=lambda : return_tool(i[1], window))
            button.pack()

class Invoice:

    def __init__(self):
        window = Tk()
        window.geometry("300x500")
        c.execute("""SELECT * FROM invoice WHERE username=?""", (CURRENT[0], ))
        a = c.fetchall()
        for i in a :
            for k in i:
                label = Label(window, text=k)
                label.pack()

        button = Button(window, text="Clear", command=lambda: dashboard_(window))
        window.mainloop()


def loginpage():
    print('dssd')
    l = Login()

def viewpage(a):
    v = ViewPage(a)

def addtool(window):
    window.destroy()
    a = AddTool()

def dashboard():
    d = Dashboard()

def dashboard_(window):
    window.destroy()
    d = Dashboard()

def hiretoolpage(window):
    window.destroy()
    h = HiredToolPage()
def show_invoice():
    i = Invoice()

loginpage()
