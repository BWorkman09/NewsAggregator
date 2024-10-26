<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <h1>News Aggregator API Documentation</h1>
  <h2>Overview</h2>
  <p>This API allows users to interact with a news aggregator database to retrieve articles based on preferences, manage user preferences, and organize content by category. This API aims to provide a personalized news experience by using user-defined preferences and categories.</p>

  <h2>Database Structure</h2>
  <p>The API interacts with the following main tables:</p>
  <ol>
    <li><strong>User</strong>: Stores user-specific information, including user ID, name, email, and password hash.</li>
    <li><strong>User_Preference</strong>: Stores each user's preferences for news categories, allowing for personalized news aggregation.</li>
    <li><strong>Categories</strong>: Lists various categories or topics of news articles, such as 'Politics', 'Sports,' and ‘Tech.’</li>
    <li><strong>Article</strong>: Contains metadata for news articles, such as the title, category ID, and timestamp.</li>
  </ol>

  <h2>API Endpoints</h2>
  <h3>1. User Endpoints</h3>
  <ul>
    <li>
      <h4>GET /users/{user_id}</h4>
      <p><strong>Description:</strong> Retrieve information for a specific user by ID.</p>
      <p><strong>Path Parameters:</strong> `user_id` - unique identifier of the user.</p>
      <p><strong>Response:</strong> JSON object with user details.</p>
      <pre><code>{
  "user_id": 1,
  "name": "Vikram",
  "email": "vikram@example.com"
}</code></pre>
    </li>
    <li>
      <h4>POST /users</h4>
      <p><strong>Description:</strong> Create a new user.</p>
      <p><strong>Request Body:</strong> JSON object with `name` and `email`.</p>
      <p><strong>Response:</strong> Confirmation message with the new user's ID.</p>
    </li>
    <li>
      <h4>PUT /users/{user_id}</h4>
      <p><strong>Description:</strong> Update a user's information.</p>
      <p><strong>Path Parameters:</strong> `user_id` - unique identifier of the user.</p>
      <p><strong>Request Body:</strong> JSON object with updated `name` or `email`.</p>
      <p><strong>Response:</strong> Confirmation message.</p>
    </li>
    <li>
      <h4>DELETE /users/{user_id}</h4>
      <p><strong>Description:</strong> Remove a user from the database.</p>
      <p><strong>Path Parameters:</strong> `user_id` - unique identifier of the user.</p>
      <p><strong>Response:</strong> Confirmation message.</p>
    </li>
  </ul>

  <h3>2. Category Endpoints</h3>
  <ul>
    <li>
      <h4>GET /categories?limit={number}</h4>
      <p><strong>Description:</strong> Retrieve a list of available categories.</p>
      <p><strong>Query Parameters:</strong> `limit` - maximum number of categories to retrieve.</p>
      <p><strong>Response:</strong> JSON array of categories.</p>
    </li>
  </ul>

  <h3>3. Article Endpoints</h3>
  <ul>
    <li>
      <h4>GET /articles/{article_id}</h4>
      <p><strong>Description:</strong> Retrieve details of a specific article by ID.</p>
      <p><strong>Path Parameters:</strong> `article_id` - unique identifier of the article.</p>
      <p><strong>Response:</strong> JSON object with article details.</p>
      <pre><code>{
  "article_id": 101,
  "title": "Over 4 Million Americans Roll Up Sleeves For Omicron-Targeted COVID Boosters",
  "category_id": USN702,
  "date": "23-09-2023"
}</code></pre>
    </li>
  </ul>

  <h3>4. User Preference Endpoints</h3>
  <ul>
    <li>
      <h4>GET /users/{user_id}/preferences</h4>
      <p><strong>Description:</strong> Retrieve a user's news category preferences.</p>
      <p><strong>Path Parameters:</strong> `user_id` - unique identifier of the user.</p>
      <p><strong>Response:</strong> JSON array of preferred categories for the user.</p>
      <pre><code>[
  {
    "category_id": TEC502,
    "category_name": "Tech"
  },
  {
    "category_id": SPO402,
    "category_name": "Sports"
  }
]</code></pre>
    </li>
    <li>
      <h4>POST /users/{user_id}/preferences</h4>
      <p><strong>Description:</strong> Add a new preference for a user.</p>
      <p><strong>Path Parameters:</strong> `user_id` - unique identifier of the user.</p>
      <p><strong>Request Body:</strong> JSON object with `category_id`.</p>
      <p><strong>Response:</strong> Confirmation message.</p>
      <pre><code>{
  "message": "Preference added successfully"
}</code></pre>
    </li>
  </ul>

  <h2>Testing</h2>
  <p>For testing, use a tool like Postman to validate the endpoints, sending requests to check the data structure, response times, and accuracy.</p>
</body>
</html>
