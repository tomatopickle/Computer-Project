# Import necessary modules

# sys module provides access to some variables used or maintained by the Python interpreter
import sys

# PyQt5.QtCore contains the core non-GUI functionality of PyQt5 including signals and slots
from PyQt5.QtCore import *

# PyQt5.QtWidgets contains classes for creating desktop applications
from PyQt5.QtWidgets import *

# PyQt5.QtWebEngineWidgets provides a web engine component for rendering HTML content
from PyQt5.QtWebEngineWidgets import *

# PyQt5.QtGui contains classes for creating graphical user interfaces
from PyQt5.QtGui import QIcon

# qdarktheme is a custom theme module for PyQt applications
import qdarktheme

# pywinstyles is used to apply specific styles to PyQt windows
import pywinstyles

# mysql.connector is a module for connecting to MySQL databases
import mysql.connector as sql

# datetime provides classes for working with dates and times
import datetime

# historyWindow and bookMarksWindow are modules for displaying history and bookmarks windows
import historyWindow
import bookMarksWindow

# Establish MySQL connection

# Establish a connection to a MySQL database running on localhost with the user "root", password "mysqls",
# and the database named "browser".
sql_connection = sql.connect(
    host="localhost", user="root", passwd="mysqls", database="browser"
)

# Check if the connection is successful

# If the MySQL connection is successful, print a message indicating that the connection is established.
if sql_connection.is_connected:
    print("Connected to Server")

# Additional style for QToolBar

# Define additional style for QToolBar using a CSS-like syntax.
qss = """
QToolBar *{font-size: 12pt;}
"""

# Execute SQL query to fetch bookmarks

# Create a cursor object to execute SQL queries on the MySQL database.
cursor = sql_connection.cursor()

# Execute a SELECT query to fetch all records from the "bookmarks" table, ordered by time in descending order.
cursor.execute("SELECT * FROM bookmarks ORDER BY time DESC;")

# Fetch all the results from the executed query and store them in the "bookmarks" variable.
bookmarks = cursor.fetchall()

# Close the cursor to free up resources.
cursor.close()

# Initialize the PyQt application

# Create an instance of the QApplication class, which is required for any PyQt application.
app = QApplication(sys.argv)

# Set up a dark theme for the application using the qdarktheme module.
qdarktheme.setup_theme(additional_qss=qss)

# Initialize the browser view

# Create an instance of QWebEngineView, which provides a web engine component for rendering HTML content.
browser = QWebEngineView()

# Set the initial URL of the browser to "http://google.com".
browser.setUrl(QUrl("http://google.com"))

# Set the application name to "Browser".
app.setApplicationName("Browser")

# Automatically set up a dark theme based on the system settings.
qdarktheme.setup_theme("auto")

# Create the main window

# Create an instance of QMainWindow, which is the main window of the application.
main_window = QMainWindow()

# Navbar

# Create a toolbar (navbar) to hold navigation buttons, URL bar, and other controls.
navbar = QToolBar()

# Function to navigate to the home page

# Define a function that sets the URL of the browser to the home page (Google).
def navigate_home():
    browser.setUrl(QUrl("https://www.google.com"))

# Function to navigate to the entered URL

# Define a function that retrieves the entered URL from the URL bar and sets it as the new URL for the browser.
def navigate_to_url():
    # Get the entered URL from the URL bar.
    url = url_bar.text()

    # Check if "http" is not in the URL, then construct a search URL using Google.
    if "http" not in url:
        url = f"https://www.google.com/search?q={url}"

    # Set the URL of the browser.
    browser.setUrl(QUrl(url))

# Function to add a history entry for the visited URL

# Define a function that adds a history entry for the visited URL to the MySQL database.
def add_history(url):
    try:
        # Get the current time in UTC format.
        visited_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # Create a tuple containing the visited time and the URL.
        history_info = (visited_time, url)

        # Print the history information.
        print(history_info)

        # Create a cursor to execute SQL queries.
        cursor = sql_connection.cursor()

        # Execute an INSERT query to add the history entry to the "history" table.
        cursor.execute("INSERT INTO history VALUES " + str(history_info))

        # Close the cursor.
        cursor.close()

        # Commit the changes to the database.
        sql_connection.commit()

        # Check if the page is bookmarked.
        check_bookmark(url)

    except:
        return

# Button to toggle bookmarks

# Create a QPushButton with a star (☆) symbol to toggle bookmarking for the current page.
bookmark_btn = QPushButton("☆", browser)

# Function to check if the current page is bookmarked

# Define a function that checks if the current page is bookmarked and updates the bookmark button accordingly.
def check_bookmark(url):
    is_bookmark = False

    # Iterate through each bookmark in the bookmarks list.
    for bookmark in bookmarks:
        # If the bookmark URL matches the current page URL, set the bookmark button text to a filled star (★).
        if bookmark[0] == url:
            bookmark_btn.setText("★")
            is_bookmark = True

    # If the current page is not bookmarked, set the bookmark button text to an empty star (☆).
    if not is_bookmark:
        bookmark_btn.setText("☆")

# Function to handle page loading start

# Define a function that sets the window title to indicate that the browser is currently loading a page.
def loading_started():
    main_window.setWindowTitle("Browser: Loading")

# Function to update the URL bar

# Define a function that updates the URL bar, adds a history entry, and checks for bookmarks when the URL changes.
def update_url(q):
    # Get the current URL from the QUrl object.
    url = q.toString()

    # Set the text of the URL bar to the current URL.
    url_bar.setText(url)

    # Add a history entry for the current URL.
    add_history(url)

    # Check if the page is bookmarked.
    check_bookmark(url)

# Function to update the window title

# Define a function that updates the window title with the current page's title.
def update_title():
    main_window.setWindowTitle(f"Browser: {browser.title()}")

# Function to show the browsing history window

# Define a function that opens a window to display the browsing history.
def show_history():
    # Use the showHistoryWindow function from historyWindow module and execute the window.
    historyWindow.showHistoryWindow().exec()

# Function to show the bookmarks window

# Define a function that opens a window to display the bookmarks.
def bookmark_page():
    # Use the showBookMarksWindow function from bookMarksWindow module and execute the window.
    bookMarksWindow.showBookMarksWindow().exec()

# URL bar

# Create a QLineEdit widget for entering URLs.
url_bar = QLineEdit(browser)

# Connect the "returnPressed" signal of the URL bar to the "navigate_to_url" function.
url_bar.returnPressed.connect(navigate_to_url)

# Add the URL bar to the navbar.
navbar.addWidget(url_bar)

# Function to set or remove bookmarks

# Define a function that sets or removes bookmarks based on the state of the bookmark button.
def set_bookmark():
    # Get the current URL of the browser.
    current_url = browser.url().toString()

    # If the bookmark button text is a filled star (★), remove the bookmark.
    if bookmark_btn.text() == "★":
        # Create a cursor to execute SQL queries.
        cursor = sql_connection.cursor()

        # Execute a DELETE query to remove the bookmark from the "bookmarks" table.
        cursor.execute(f"DELETE FROM bookmarks WHERE url = '{current_url}'")

        # Close the cursor.
        cursor.close()

        # Commit the changes to the database.
        sql_connection.commit()

        # Set the bookmark button text to an empty star (☆).
        bookmark_btn.setText("☆")

        # Update the bookmarks list to exclude the removed bookmark.
        global bookmarks
        bookmarks = [bookmark for bookmark in bookmarks if bookmark[0] != current_url]

    # If the bookmark button text is an empty star (☆), add a bookmark.
    else:
        # Get the current time in UTC format.
        time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # Create a tuple containing the current URL and the timestamp.
        bookmark_info = (current_url, time)

        # Print the bookmark information.
        print(bookmark_info)

        # Create a cursor to execute SQL queries.
        cursor = sql_connection.cursor()

        # Execute an INSERT query to add the bookmark to the "bookmarks" table.
        cursor.execute("INSERT INTO bookmarks VALUES " + str(bookmark_info))

        # Close the cursor.
        cursor.close()

        # Commit the changes to the database.
        sql_connection.commit()

        # Add the new bookmark to the bookmarks list.
        bookmarks.append(bookmark_info)

        # Set the bookmark button text to a filled star (★).
        bookmark_btn.setText("★")

# Connect the "pressed" signal of the bookmark button to the "set_bookmark" function.
bookmark_btn.pressed.connect(set_bookmark)

# QAction for additional buttons

# Create a QAction for the "Bookmarks" button.
all_bookmarks_action = QAction("Bookmarks", browser)

# Connect the "triggered" signal of the "Bookmarks" button to the "bookmark_page" function.
all_bookmarks_action.triggered.connect(bookmark_page)

# Create a QAction for the "History" button.
history_btn = QAction("History", browser)

# Connect the "triggered" signal of the "History" button to the "show_history" function.
history_btn.triggered.connect(show_history)

# Add the "Bookmarks" and "History" buttons to the navbar.
navbar.addAction(all_bookmarks_action)
navbar.addAction(history_btn)

# Connect signals to functions

# Connect various signals of the browser to their corresponding functions.
browser.urlChanged.connect(update_url)
browser.urlChanged.connect(loading_started)
browser.titleChanged.connect(update_title)
browser.loadFinished.connect(update_title)

# Set up the main window

# Set the central widget of the main window to be the browser.
main_window.setCentralWidget(browser)

# Add the navbar (toolbar) to the main window.
main_window.addToolBar(navbar)

# Show the main window in maximized mode.
main_window.showMaximized()

# Apply styles

# Apply specific styles to the main window and browser using the pywinstyles module.
pywinstyles.apply_style(main_window, "mica")
pywinstyles.apply_style(browser, "mica")

# Run the application

# Start the event loop of the application.
sys.exit(app.exec_())
