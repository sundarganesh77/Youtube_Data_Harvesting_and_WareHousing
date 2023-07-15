# Youtube_Data_Harvesting_and_WareHousing
Extracting Data from the Youtube API which is in json format inserting data into Mongodb(No SQL Database) and FInally inserting Data into SQL database. Streamlit app is used for Visualizing the Data.

## Problem statement
The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels.
### Features Needed
1. Ability to input a YouTube channel ID and retrieve all the relevant data(Channel name, subscribers, total video count, playlist ID, video ID, likes,dislikes, comments of each video) using Google API.
2. Option to store the data in a MongoDB database as a data lake.
3. Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
4. Option to select a channel name and migrate its data from the data lake to a SQL database as tables.
5. Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

## Streamlit App Interface
streamlit App consists of Main Page,Username converter page,Single select Page,Multiselect Page in the sidebar of the streamlit app.
### Main Page
1. Main Page consists of the Architectural Daigram of the Project which is in the files, From https://draw.io website one can create architectural flow diagrams for free.
2. Architectural Flow:  Youtube API---->Python----->Mongodb------>SQL------->Streamlit
3. streamlit is the Interface for the flow.
### Username Converter Page
1. In the username converter page, one can extract the channel_id from the channel_name.
2. For channel_name, go to any youtube channel for example https://www.youtube.com/@AlexTheAnalyst, in this url AlexTheAnalyst is the channel_name which can be found out from the url of the page.
3. Copy the user_name from the url and paste it in the username converter page and enter then select for get channel_id this will fetch the channel_id for the username from the youtube API.
4. save the channel_id and move to the single select page.
5. Example channel_id = UCOw3uyJI7GgSSJWXDKh2azA - This is how the channel_id looks like.
### Single Select Page
1. From the obtained channel_id from the username converter page copy the channel_id and paste it and enter and click fetch channel data button which will fetch channel_id,playlist_id,video_name,description,likes_count,video_count etc as a Dataframe.
2. Maximum of 10 videos is considered for the dataframe.
3. Based on the data obtained, Two visualization plots are drawn one for likes_count and another for subscription_count for their respective channels using plotly.
### Multiselect Page 
1. From the username converter page one can extract as many channel_ids as they want.
2. Paste the channel_ids it can single or multiple channel_ids in the channe_id section which is separated by commas and click Fetch youtube data button.
3. when data is fetched it shows data is fetched successfully and then click on the show youtube channel data button, it shows an expander show channel data button when clicked on it data is shown which is fetched for the respective channel_ids.
4. Mongodb Atlas is used here, Based on the uri one can connect to Mongodb by installing pymongo and create a collection and the insert the data.
5. For the data to upload into Mongodb, click on the button upload data to mongodb when successful it shows data inserted into into Mongodb successfully.
6. Delete Mongodb collection is created for dropping the entire collection.
7. Next click upload data into SQL button, when successful it shows the data is inserted into the SQl.
8. In SQL database, data is stored in the form of tables, so four tables are created in the SQL schema which are Channel,Playlist,Comment,Video and their schema is given above.
9. once the data got inserted into the sql a dropdown appears which consists of 10 question based on the selection one can observe the data for the channel_ids in the table in streamlit for their respective question asked.

## summary
using this streamlit app one can extract channel_id from the channel_username, upon extraction of channel_ids on can fetch the data of the youtube channel_ids in single select and visualize from the data also.In the Multiselect page once can select onr or more than one channel_ids and can fetch the youtubbe data and see the data in show youtube data button. using upload data into mongodb one can upload the data into mongodb(No SQL database) collection which is in the form of dictionaries.finally to convert the data into structured format data is inserted into SQL database in the form of tables. Answers for the question is queried from the SQL database.




