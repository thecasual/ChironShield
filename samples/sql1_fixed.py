import mysql.connector

# Get user input
username = input("Enter your username: ")
password = input("Enter your password: ")

# Connect to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="mydatabase"
)

# Create a cursor
mycursor = mydb.cursor()

# Execute the SQL query with user input
mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))

# Fetch the results
myresult = mycursor.fetchall()

# Print the results
for x in myresult:
  print(x)