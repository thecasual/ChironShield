import mysql.connector
import subprocess

# Get user input
username = input("Enter your username: ")
password = input("Enter your password: ")

cmd = "echo %s" % username
subprocess.Popen(cmd, shell=True)

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost", user="root", password="password", database="mydatabase"
)

# Create a cursor
mycursor = mydb.cursor()

# Execute the SQL query with user input
mycursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'")

# Fetch the results
myresult = mycursor.fetchall()

# Print the results
for x in myresult:
    print(x)
