import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect(r'C:\Users\Aishu\OneDrive\Desktop\MABA\Assignments\Fall\Advanced Data Prep\Group Assignment\Group-Assigment-2\data\News_Aggregator.db')

# Query 1: Join Category and Article tables
query1 = """
SELECT Article.Article_ID, Article.Category_ID, Category.Description 
FROM Category 
JOIN Article ON Category.category_id = article.category_id;
"""
df1 = pd.read_sql_query(query1, conn)
print("Result of Query 1:")
print(df1)

# Query 2: Select a specific article by article_id
query2 = "SELECT * FROM Article WHERE article_id = ?"
article_id = 1102  # Parameterized input
df2 = pd.read_sql_query(query2, conn, params=(article_id,))
print("\nResult of Query 2:")
print(df2)

# Query 3: Aggregated count of users preferring each category
query3 = """
SELECT Category_ID, COUNT(user_id) AS Users_preferring_this_category 
FROM User_Preference 
GROUP BY Category_ID;
"""
df3 = pd.read_sql_query(query3, conn)
print("\nResult of Query 3:")
print(df3)

# Close the database connection
conn.close()
