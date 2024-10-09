SELECT Article.Article_ID, Article.Category_ID, Category.Description
FROM Category
JOIN Article ON Category.Category_ID = Article.Category_ID;
