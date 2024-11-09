# News Aggregator
In this project, we have created a News Aggregator in which users will be able to see a tailored news feed based on their selected preferences.




# Features

Allow users to register so they can personalize their news feed. ​

Allow anonymous access to ‘public’ sections of the site. ​

Allow users to select their preferences from different news categories. ​

Allow users to bookmark content. ​

Allow users to access preference-analytics and activity-analytics dashboards. ​



# Base URL
The base URL for all the routes is /api. Here's a Markdown version of your OpenAPI specification:


# Using the API Endpoints

# Home Endpoint
*URL: /
*Method: GET
*Summary: Displays a welcome message for the API.
*Response:

    200 OK: Welcome message

# Article
http://localhost:5000/api/articles - Lookup All Articles
http://localhost:5000/api/articles?limit=10 - Lookup Limited # of user Articles
http://localhost:5000/api/articles/by-category-name?category=ARTS%20%26%20CULTURE - Lookup Articles by Category
http://localhost:5000/api/articles/by-category-name?category=ARTS%20%26%20CULTURE&limit=1 - Lookup Articles by Category with Limits

# Categories
http://localhost:5000/api/categories - Lookup All Categories
http://localhost:5000/api/categories?limit=10 - Lookup Limited # of Categories

# UserP
http://localhost:5000/api/user_preferences - Lookup User Preferences
http://localhost:5000/api/user_preferences?limit=10 - Lookup Limited # of user Preferences

# User
http://localhost:5000/api/users - Lookup All Users
http://localhost:5000/api/users?limit=10 Lookup Limited # of Users
http://localhost:5000/api/users?name=Ricky Lookup Users by Name




