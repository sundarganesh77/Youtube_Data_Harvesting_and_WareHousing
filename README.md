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
streamlit App consists of Main Page,Usename converter page,Single select Page,Multiselect Page in the sidebar of the streamlit app.
### Main Page
1. Main Page consists of the Architectural Daigram of the Project which is in the files, From https://draw.io website one can create architectural flow diagrams for free.
2. Architectural Flow:  Youtube API---->Python----->Mongodb------>SQL------->Streamlit
3. streamlit is the Interface for the flow.
### Username Converter Page
1. In the username converter page, one can extract the channel_id from the channel_name.
2. For channel_name, go to any youtube channel for example https://www.youtube.com/@AlexTheAnalyst, in this url AlexTheAnalyst is the channel_name which can be found out from the url of the page.
3. Copy the user_name from the url and paste it in the username converter page and enter then select for get channel_id this will fetch the channel_id for the username from the youtube API.
4. save the channel_id and move to the single select page.
### Single Select Page
1. From the obtained channel_id from the username converter page copy the channel_id and paste it and enter and click fetch channel data button which will fetch channel_id,playlist_id,video_name,description,likes_count,video_count etc as a Dataframe.
2. Maximum of 10 videos is considered for the dataframe
3. Based on the data obtained two plots are drawn for likes_count and subscription_count for the  respective channel using plotly. 


