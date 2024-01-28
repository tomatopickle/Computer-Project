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

# pywinstyles is used to apply specific styles to PyQt windows
import pywinstyles

# qdarktheme is a custom theme module for PyQt applications
import qdarktheme

# mysql.connector is a module for connecting to MySQL databases
import mysql.connector as sql

# Define a function to show the History window
def showHistoryWindow():
    # Define additional style for the History window using a CSS-like syntax.
    qss = """
    QMenuBar *{font-size: 12pt;}
    QListWidget {font-size:10pt;}
    """

    # Establish a connection to a MySQL database running on localhost with the user "root", password "mysqls",
    # and the database named "browser".
    sql_connection = sql.connect(
        host="localhost", user="root", passwd="mysqls", database="browser"
    )

    # Check if the connection is successful

    # If the MySQL connection is successful, print a message indicating that the connection is established.
    if sql_connection.is_connected:
        print("Connected to Server")

    # Set up a dark theme for the History window using the qdarktheme module.
    qdarktheme.setup_theme(additional_qss=qss)

    # Create a QDialog (dialog window) for displaying History.
    window = QDialog()

    # Create a vertical layout to organize widgets in a top-down fashion.
    layout = QVBoxLayout()

    # Create a menu bar for additional options.
    navbar = QMenuBar()

    # Create a QListWidget to display the browsing history.
    listwidget = QListWidget()

    # Define a function to clear all browsing history.
    def clearHistory():
        # Create a cursor to execute SQL queries.
        cursor = sql_connection.cursor()

        # Execute a DELETE query to remove all entries from the "history" table.
        cursor.execute("delete from history")

        # Commit the changes to the database.
        sql_connection.commit()

        # Clear the items in the QListWidget.
        listwidget.clear()

    # Create a QLabel for the History label in the menu bar.
    historyLabel = QLabel("History", navbar)

    # Set the History label in the top-left corner of the menu bar.
    navbar.setCornerWidget(historyLabel, Qt.TopLeftCorner)

    # Create a QPushButton for clearing history in the menu bar.
    clearHistoryButton = QPushButton("Clear History", navbar)

    # Set the Clear History button in the top-right corner of the menu bar.
    navbar.setCornerWidget(clearHistoryButton, Qt.TopRightCorner)

    # Connect the button's clicked signal to the clearHistory function.
    clearHistoryButton.clicked.connect(clearHistory)

    # Create a cursor to execute SQL queries.
    cursor = sql_connection.cursor()

    # Execute a SELECT query to fetch all records from the "history" table, ordered by time in descending order.
    cursor.execute("select * from history order by time desc;")

    # Fetch all the results from the executed query and store them in the "history" variable.
    history = cursor.fetchall()

    # Close the cursor to free up resources.
    cursor.close()

    # Populate the QListWidget with browsing history entries.
    i = 0
    for site in history:
        print(site)
        listwidget.insertItem(i, f"{site[0]}   {site[1]}")
        i += 1

    # Add widgets to the layout.
    layout.addWidget(navbar)
    layout.addWidget(listwidget)

    # Resize the window.
    window.resize(750, 500)

    # Set the layout for the window.
    window.setLayout(layout)

    # Apply a specific style to the History window using the pywinstyles module.
    pywinstyles.apply_style(window, "mica")

    # Return the History window.
    return window

# Note: The showHistoryWindow function is defined, but it needs to be executed (e.g., using the exec_() method) to display the window.
