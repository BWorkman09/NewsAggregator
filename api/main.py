
print("""
      
      
      
      Results of JOIN RELATIONSHIP Query 
      
      
      """)




#QUERY1 JOIN RELATIONSHIP
import sqlite3

# Set the name of the database file to be used for this exercise
db_file = r"data\News_Aggregator.db"

# Make a connection to the database
cnn = sqlite3.connect(db_file)

# Next make a cursor that can be used to run a query on the new connection
cur = cnn.cursor()

# get the first 10 records from the sales table
query = cur.execute('''SELECT article.Title AS "Title", 
category.Description AS "Category Description", 
category.Category AS "Category"
FROM Category
INNER JOIN Article ON Category.Category_ID = article.Category_ID 
LIMIT 10''' 
)

for row in query:
    print(row)  



# It's good practice to ensure that we close our connection to the database when we are done using it
cnn.close()


print("""
      
      
      
      Results of PARAMETERIZED Query 
      
      
      """)


#QUERY2 PARAMETERIZED


# Make a connection to the database
cnn = sqlite3.connect(db_file)

# Next make a cursor that can be used to run a query on the new connection
cur = cnn.cursor()


#use one of the following Categories RELIGION, SPORTS, TECH, or TRAVEL
print("Use one of the following, case sensitive, categores: RELIGION, SPORTS, TECH, or TRAVEL")
user_input = input('Enter a Category: ')
sql_query = f"SELECT * FROM article WHERE category = '{user_input}' LIMIT 10"
#sql_query = f"SELECT distinct category FROM article LIMIT 10"
query3 = cur.execute(sql_query)

for row in query3:
    print(row)  


cnn.close()







print("""
      
      
      
      Results of Aggregate Function Query 
      
      
      """)
#QUERY3 AGGREGATE FUNCTION

# Make a connection to the database
cnn = sqlite3.connect(db_file)

# Next make a cursor that can be used to run a query on the new connection
cur = cnn.cursor()

result= cur.execute("""
    SELECT Category, MAX(Date), MIN(Date) FROM Article GROUP BY Category""")
#use one of the following Categories RELIGION, SPORTS, TECH, or TRAVEL

for row in result:
    print(row)  


cnn.close()