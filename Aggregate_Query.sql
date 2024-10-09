SELECT Category_ID, COUNT(User_ID) AS Users_opting_for_this_category
FROM User_Preference
GROUP BY Category_ID;
