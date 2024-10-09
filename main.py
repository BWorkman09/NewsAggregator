
import sqlite3

# Set the name of the database file to be used for this exercise
db_file = r"C:\Users\brett\Documents\GitHub\Group-Assigment-2\data\News_Aggregator.db"

# Make a connection to the database
cnn = sqlite3.connect(db_file)

# Next make a cursor that can be used to run a query on the new connection
cur = cnn.cursor()

# get the first 10 records from the sales table
result = cur.execute('''SELECT article.Title AS "Title", 
category.Description AS "Category Description", 
category.Category AS "Category"
FROM Category
INNER JOIN Article ON Category.Category_ID = article.Category_ID 
LIMIT 10''' 
)


#data = pd.read_sql_query("""
#SELECT artists.Name AS 'Artist Name', albums.Title AS 'Album Title', tracks.Name AS 'Track Name', genres.Name AS 'Genre Name'
#FROM artists
#INNER JOIN albums ON artists.ArtistId = albums.ArtistId
#INNER JOIN tracks ON albums.AlbumId = tracks.AlbumId
#INNER JOIN genres ON tracks.GenreID = genres.GenreId
#LIMIT 10
#""", cnn)



# Print the first 10 records
for row in result:
    print(row)  

# It's good practice to ensure that we close our connection to the database when we are done using it
cnn.close()


