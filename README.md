# News Aggregator
In this project, we have created a News Aggrgator in which users will be able to see tailored news feed based on their selected preferences.




#Features

Allow users to register so they can personalize their news feed. ​

Allow anonymous access to ‘public’ sections of the site. ​

Allow users to select their preferences from different news categories. ​

Allow users to bookmark content. ​

Allow users to access preference-analytics and activity-analytics dashboards. ​







The DB contains 4 tables. User, Article, Category, and User Preference. 



Data Dictionary:

![image](https://github.com/user-attachments/assets/feb933d6-dca3-4596-b84a-3933cc533f0b)
















An Entitiy Relationship Diagram can be found below:
![GA_ERD2](https://github.com/user-attachments/assets/7cd69ff8-81a9-4eb5-a53e-e7faab4d10fe)
Query 1 performs a join between the Category and Article tables.
Query 2 uses a parameterized input to select Article_ID = 1102.
Query 3 performs an aggregation, counting how many users prefer each category.
