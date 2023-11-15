import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon
import qdarktheme
import pywinstyles
import mysql.connector as sql
import datetime
import historyWindow
import bookMarksWindow

# Establish MySQL connection
sql_connection = sql.connect(
    host="localhost", user="root", passwd="mysqls", database="browser"
)

# Check if the connection is successful
if sql_connection.is_connected:
    print("Connected to Server")

# Additional style for QToolBar
qss = """
QToolBar *{font-size: 12pt;}
"""

# Execute SQL query to fetch bookmarks
cursor = sql_connection.cursor()
cursor.execute("SELECT * FROM bookmarks ORDER BY time DESC;")
bookmarks = cursor.fetchall()
cursor.close()

# Initialize the PyQt application
app = QApplication(sys.argv)
qdarktheme.setup_theme(additional_qss=qss)

# Initialize the browser view
browser = QWebEngineView()
browser.setUrl(QUrl("http://google.com"))
app.setApplicationName("Browser")
qdarktheme.setup_theme("auto")

# Create the main window
main_window = QMainWindow()

# Navbar
navbar = QToolBar()

# Function to navigate to the home page
def navigate_home():
    browser.setUrl(QUrl("https://www.google.com"))

# Function to navigate to the entered URL
def navigate_to_url():
    url = url_bar.text()
    if "http" not in url:
        url = f"https://www.google.com/search?q={url}"
    browser.setUrl(QUrl(url))

# Function to add history entry
def add_history(url):
    try:
        visited_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        history_info = (visited_time, url)
        print(history_info)
        cursor = sql_connection.cursor()
        cursor.execute("INSERT INTO history VALUES " + str(history_info))
        cursor.close()
        sql_connection.commit()
        check_bookmark(url)
    except:
        return

# Button to toggle bookmarks
bookmark_btn = QPushButton("☆", browser)

# Function to check if the current page is bookmarked
def check_bookmark(url):
    is_bookmark = False
    for bookmark in bookmarks:
        if bookmark[0] == url:
            bookmark_btn.setText("★")
            is_bookmark = True
    if not is_bookmark:
        bookmark_btn.setText("☆")

# Function to handle page loading start
def loading_started():
    main_window.setWindowTitle("Browser: Loading")

# Function to update the URL bar
def update_url(q):
    url = q.toString()
    url_bar.setText(url)
    add_history(url)
    check_bookmark(url)

# Function to update the window title
def update_title():
    main_window.setWindowTitle(f"Browser: {browser.title()}")

# Function to show the browsing history window
def show_history():
    historyWindow.showHistoryWindow().exec()

# Function to show the bookmarks window
def bookmark_page():
    bookMarksWindow.showBookMarksWindow().exec()

# QAction for navigation buttons
back_btn = QAction(QIcon(QApplication.style().standardIcon(QStyle.SP_ArrowLeft)), "Back", browser)
back_btn.triggered.connect(browser.back)
navbar.addAction(back_btn)

forward_btn = QAction(QIcon(QApplication.style().standardIcon(QStyle.SP_ArrowRight)), "Forward", browser)
forward_btn.triggered.connect(browser.forward)
navbar.addAction(forward_btn)

reload_btn = QAction(QIcon(QApplication.style().standardIcon(QStyle.SP_BrowserReload)), "Reload", browser)
reload_btn.triggered.connect(browser.reload)
navbar.addAction(reload_btn)

home_btn = QAction(QIcon(QApplication.style().standardIcon(QStyle.SP_DirHomeIcon)), "Home", browser)
home_btn.triggered.connect(navigate_home)
navbar.addAction(home_btn)

# URL bar
url_bar = QLineEdit(browser)
url_bar.returnPressed.connect(navigate_to_url)
navbar.addWidget(url_bar)

# Function to set or remove bookmarks
def set_bookmark():
    current_url = browser.url().toString()
    if bookmark_btn.text() == "★":
        # Removing bookmark
        cursor = sql_connection.cursor()
        cursor.execute(f"DELETE FROM bookmarks WHERE url = '{current_url}'")
        cursor.close()
        sql_connection.commit()
        bookmark_btn.setText("☆")
        global bookmarks
        bookmarks = [bookmark for bookmark in bookmarks if bookmark[0] != current_url]
    else:
        # Adding bookmark
        time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        bookmark_info = (current_url, time)
        print(bookmark_info)
        cursor = sql_connection.cursor()
        cursor.execute("INSERT INTO bookmarks VALUES " + str(bookmark_info))
        cursor.close()
        sql_connection.commit()
        bookmarks.append(bookmark_info)
        bookmark_btn.setText("★")

bookmark_btn.pressed.connect(set_bookmark)

# QAction for additional buttons
all_bookmarks_action = QAction("Bookmarks", browser)
all_bookmarks_action.triggered.connect(bookmark_page)

history_btn = QAction("History", browser)
history_btn.triggered.connect(show_history)

# Add buttons to the navbar
navbar.addWidget(bookmark_btn)
navbar.addAction(history_btn)
navbar.addAction(all_bookmarks_action)

# Connect signals to functions
browser.urlChanged.connect(update_url)
browser.urlChanged.connect(loading_started)
browser.titleChanged.connect(update_title)
browser.loadFinished.connect(update_title)
browser.setZoomFactor(1.3)

# Set up the main window
main_window.setCentralWidget(browser)
main_window.addToolBar(navbar)
main_window.showMaximized()

# Apply styles
pywinstyles.apply_style(main_window, "mica")
pywinstyles.apply_style(browser, "mica")

# Run the application
sys.exit(app.exec_())
