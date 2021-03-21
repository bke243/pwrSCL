from tkinter import *
import urllib.request
import json
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global  variables
MAIN_APP_SIZE = "700x700"
WIDTH = 1000
HEIGHT = 700
TABLE_NAME = "project"
MAIN_STATUS = "No operation perfomed"
BG_COLOR = "blue"
DATA_LOACTION = "https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json"
DATA_INSERTION = "INSERT INTO project(title, year, cast, genre) VALUES (:title, :year, :cast, :genre)"

# End global variables

# DB Operations

# db connection pool
conn = sqlite3.connect("project.db")
# make sure that the table is there
db = conn.cursor()
db.execute("""
    CREATE TABLE IF NOT EXISTS project (
      id INTEGER  PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      year INTEGER NOT NULL,
      cast VARCHAR(255) ,
      genre VARCHAR(255));""")


def get_json_data():
    """Download the data from internet and save them inside the db"""
    global DATA_LOACTION
    global DATA_INSERTION
    try:
        db_is_empty = is_database_empty()
        if(db_is_empty):
            with urllib.request.urlopen(DATA_LOACTION) as url:
                movies = json.loads(url.read().decode())
                count = 0
                for movie in movies:
                    count += 1
                    str1 = " "
                    title = movie.get("title")
                    year = movie.get("year")
                    cast = str1.join(movie.get("cast"))
                    genre = str1.join(movie.get("genres"))
                    db.execute(DATA_INSERTION,
                               {"title": title, "year": year,
                                "cast": cast, "genre": genre})
                    # commit after every 1000
                    if(count % 1000 == 0):
                        conn.commit()
                count = 0
            # final commit
            conn.commit()
            notify_user_frame("The data were donwload", "Success")
        else:
            notify_user_frame("The data were already donwload", "Success")
    # no need to catch a specific exception
    except Exception as error:
        notify_user_frame("Could not download data", "Failure")


def clear_database():
    """clear the database data"""
    try:
        db.execute("DELETE FROM project")
        conn.commit()
        notify_user_frame("The data were cleared", "Success")
    except Exception as error:
        notify_user_frame("Could not delete data", "Failure")


def is_database_empty():
    """check if the database has data"""
    db.execute("SELECT COUNT(*) FROM project WHERE year=2018")
    result = db.fetchall()
    if(result[0][0] == 0):
        return True
    else:
        False


def get_database_agragate():
    """total numbr of movies"""
    db.execute("SELECT COUNT(*) FROM project")
    rows = db.fetchall()
    return rows[0][0]


def get_database_chart_data():
    """ get the data for ploting the chart"""
    db.execute("SELECT year,COUNT(*) FROM project GROUP BY year")
    rows = db.fetchall()
    x = list()
    y = list()

    for row in rows:
        x.append(row[0])
        y.append(row[1])

    data = (x, y)
    return data


# end DB operations

main_screen = Tk()

main_screen.title("American Movie Analizer By Peter")
main_screen.geometry(MAIN_APP_SIZE)
# menu bar
menu_bar = Menu(main_screen)
main_screen.config(menu=menu_bar)

# Man App


# go to sttings data
def set_red():
    """set the background to red"""
    global BG_COLOR
    hide_all_frames()
    BG_COLOR = "red"
    display_main_frame()


def set_green():
    """set the background tp green"""
    global BG_COLOR
    hide_all_frames()
    BG_COLOR = "green"
    display_main_frame()


# display main frame
def display_main_frame():
    """display the main frame"""
    hide_all_frames()
    main_frame.pack(fill="both", expand=1)
    label1 = Label(main_frame, text="Main Window", bg=BG_COLOR, width="300",
                   height="2", font=("Calibri", 13)).pack()
    label2 = Label(main_frame, text="").pack()
    button1 = Button(main_frame, text="Agregate Result", height="2",
                     width="30", command=display_agragate_frame).pack()
    label3 = Label(main_frame, text="").pack()
    button2 = Button(main_frame, text="Display Chart", height="2", width="30",
                     command=diplay_chart_frame).pack()
    label3 = Label(main_frame, text="Previous Operation status : {}"
                   .format(MAIN_STATUS), bg=BG_COLOR, width="300", height="2",
                   font=("Calibri", 13)).pack(side="bottom")


# clear the database frame
def clear_database_frame():
    """display the clear database frame"""
    hide_all_frames()
    # fit the screen
    clear_data_frame.pack(fill="both", expand=1)
    title = Label(clear_data_frame, text="Do you want to clear the database ? "
                  ).pack(fill="none", expand=True)
    confirm = Button(clear_data_frame, text="Confirm ", height="2", width="20",
                     command=clear_database).pack(fill="none", expand=True)
    cancel = Button(clear_data_frame, text="Cancel", height="2", width="20",
                    command=display_main_frame).pack(fill="none", expand=True)


def download_frame():
    """display the download frame"""
    hide_all_frames()
    # fit the screen
    download_data_frame.pack(fill="both", expand=1)
    title = Label(download_data_frame, text="Do you want to donwload data ? "
                  ).pack(fill="none", expand=True)
    confirm = Button(download_data_frame, text="Confirm ", height="2",
                     width="20", command=get_json_data
                     ).pack(fill="none", expand=True)
    cancel = Button(download_data_frame, text="Cancel", height="2", width="20",
                    command=display_main_frame).pack(fill="none", expand=True)


def display_agragate_frame():
    """display the agregate form"""
    hide_all_frames()
    # fit the screen
    try:
        message = str()
        if(is_database_empty()):
            message = "The dabase is empty and not sum can be calculated"
        else:
            number = get_database_agragate()
            message = "The total  movies information downloaded is {}".format(
                number)
        agragate_frame.pack(fill="both", expand=1)
        Label(agragate_frame, text="").pack()
        label = Label(agragate_frame, text=message, width="300", height="2",
                      font=("Calibri", 13)).pack()
        cancel = Button(agragate_frame, text="Ok", height="2", width="20",
                        command=display_main_frame).pack(
                            fill="none", expand=True)
    except Exception as int:
        notify_user_frame("Could not agragate data", "Failure")


def diplay_chart_frame():
    """DISPLAY THE CHART FRAME"""
    hide_all_frames()
    try:
        chart_frame.pack(fill="both", expand=1)
        message = str()
        data = None
        has_data = is_database_empty()
        if(has_data):
            message = "please download the data first"
            Label(chart_frame, text="").pack()
            label = Label(chart_frame, text=message, width="300", height="2",
                          font=("Calibri", 13)).pack()
            cancel = Button(chart_frame, text="Ok", height="2", width="20",
                            command=display_main_frame).pack(
                                fill="none", expand=True)
        else:
            message = "Movies per year"
            data = get_database_chart_data()
            x, y = data
            label = Label(chart_frame, text=message, width="300", height="2",
                          font=("Calibri", 13)).pack()
            # the figure that will contain the plot
            fig = Figure(figsize=(17.5, 5), dpi=100)
            plot1 = fig.add_subplot(111)
            # plotting the chart
            plot1.plot(x, y, '--bo')
            plot1.set_xlabel('Year')
            plot1.set_ylabel('Number of movies')
            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().pack()
            # placing the toolbar on the Tkinter window
            canvas.get_tk_widget().pack()
            cancel = Button(chart_frame, text="Ok", height="2", width="20",
                            command=display_main_frame).pack(
                                fill="none", expand=True)
    except Exception as int:
        notify_user_frame("Could not agragate data", "Failure")


# notification frame
def notify_user_frame(message, status):
    """ global utility notification frame"""
    hide_all_frames()
    global MAIN_STATUS
    MAIN_STATUS = status
    notify_frame.pack(fill="both", expand=1)
    Label(notify_frame, text="").pack()
    label = Label(notify_frame, text=status, width="300", height="2", font=(
            "Calibri", 13)).pack()
    Label(notify_frame, text="").pack()
    label2 = Label(notify_frame, text=message, width="300", height="2",
                   font=("Calibri", 13)).pack()
    Label(notify_frame, text="").pack()
    button = Button(notify_frame, text="OK", height="2", width="20",
                    command=display_main_frame).pack()


def clearFrame(frame):
    """clear all frame before displaying the others"""
    # destroy all widgets from frame
    for widget in frame.winfo_children():
        widget.destroy()
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    frame.pack_forget()


def hide_all_frames():
    """hide all frame utility """
    clearFrame(main_frame)
    clearFrame(download_data_frame)
    clearFrame(clear_data_frame)
    clearFrame(notify_frame)
    clearFrame(agragate_frame)
    clearFrame(chart_frame)

# menu items


# exit place
file_menu_item = Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu_item)
file_menu_item.add_command(label="Exit", command=main_screen.quit)

# db manage menu item
manage_db = Menu(menu_bar)
menu_bar.add_cascade(label="Local DB Manage ", menu=manage_db)
manage_db.add_command(label="Dowloand DB", command=download_frame)
manage_db.add_separator()
manage_db.add_command(label="Clear  DB", command=clear_database_frame)

# options
settings = Menu(menu_bar)
menu_bar.add_cascade(label="Settings", menu=settings)
settings.add_command(label="Red Mode", command=set_red)
settings.add_separator()
settings.add_command(label="Greend mode", command=set_green)

# frames makes display in the same window
# main frame
main_frame = Frame(main_screen, width=WIDTH, height=HEIGHT)
# download data frame
download_data_frame = Frame(main_screen, width=WIDTH, height=HEIGHT, bg="red")
# clear db frame
clear_data_frame = Frame(main_screen, width=WIDTH, height=HEIGHT, bg="yellow")
# agregate_frame
agragate_frame = Frame(main_screen, width=WIDTH, height=HEIGHT)
# plot frame
chart_frame = Frame(main_screen, width=WIDTH, height=HEIGHT)
# notification frame
notify_frame = Frame(main_screen, width=WIDTH, height=HEIGHT)


# display main frame as default entry
display_main_frame()
main_screen.mainloop()
