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

    *200 OK: Welcome message

# User Endpoints

## Lookup All Users
- **URL**: `/users`
- **Method**: `GET`
  
### Parameters
- `/users?limit=10` - Retrieve a limited number of users (e.g., 10 users).
- `/users?name=Ricky` - Retrieve users by a specific name (e.g., "Ricky").

## Update User by ID

- **URL**: `/users/{user_id}`
- **Method**: `PUT`
- **Summary**: Update an existing user.
- **Parameters**:
  - `user_id`: The unique identifier of the user.
- **Request Body**:
  - `name`: User's new name.
- **Response**:
  - `200 OK`: User updated successfully.

## Delete User by ID

- **URL**: `/users/{user_id}`
- **Method**: `DELETE`
- **Summary**: Remove a user by their ID.
- **Parameters**:
  - `user_id`: The unique identifier of the user.
- **Response**:
  - `200 OK`: User deleted successfully.


# Article Endpoints

## Lookup All Articles
- **URL**: `/articles`
- **Method**: `GET`

### Parameters
- `/articles` - Retrieve all articles.
- `/articles?limit=10` - Retrieve a limited number of articles (e.g., 10 articles).
- `/articles/by-category-name?category=ARTS%20%26%20CULTURE` - Retrieve articles by category (e.g., "Arts & Culture").
- `/articles/by-category-name?category=ARTS%20%26%20CULTURE&limit=1` - Retrieve a limited number of articles by category (e.g., 1 article from "Arts & Culture").

### Response Codes
- `200 OK`: Articles found.
- `404 Not Found`: Articles not found.

# Category Endpoints

## Lookup All Categories
- **URL**: `/categories`
- **Method**: `GET`

### Parameters
- `/categories` - Retrieve all categories.
- `/categories?limit=10` - Retrieve a limited number of categories (e.g., 10 categories).

### Response Codes
- `200 OK`: Categories found.
- `404 Not Found`: Categories not found.

# User Preferences Endpoints

## Lookup User Preferences
- **URL**: `/user_preferences`
- **Method**: `GET`

### Parameters
- `/user_preferences` - Retrieve all user preferences.
- `/user_preferences?limit=10` - Retrieve a limited number of user preferences (e.g., 10 preferences).

### Response Codes
- `200 OK`: User preferences found.
- `404 Not Found`: User preferences not found.







