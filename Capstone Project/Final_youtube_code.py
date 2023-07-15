#Libraries to be imported

#[Visualization libraries]
import streamlit as st
import pandas as pd
import plotly.express as px

#[Youtube Python libraries]
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#[Library for importing image into streamlit]
from PIL import Image

#[Loading json data Library]
import json

#[MOngodb libraries]
from pymongo import MongoClient
from pymongo.server_api import ServerApi


#Getting data from data_exploration file
from Data_exploration import *

# Set up YouTube Data API credentials
API_KEY = 'your api_key'

# Create a YouTube Data API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

#streamlit page cinfiguration
st.set_page_config(layout='wide')

#Exmple channel_ids
#channel_ids = ['UCPxMZIFE856tbTfdkdjzTSQ', 'UCOw3uyJI7GgSSJWXDKh2azA', 'UC7cs8q-gJRlGwj4A8OmCmXg', 'UC1pfsmDBnMQB8sOuQvmTvRQ', 'UCCezIgC97PvUuR4_gbFUs5g', 'UCNU_lfiiWBdtULKOw6X0Dig', 'UCh9nVJoWXmFb7sLApWGcLPQ', 'UCBGcs9XTL5U34oaSn_AsHqw', 'UC81Q2wnuk5KqOFVgAbq4nUw', 'UCBwmMxybNva6P_5VmxjzwqA']

#function for getting channel_id from channel_name
def get_channel_id(search_query):
    try:
        
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        # Search for the channel using the search query
        search_response = youtube.search().list(
            q=search_query,
            part='id',
            type='channel',
            maxResults=1
        ).execute()

        # Extract the channel ID from the search results
        items = search_response.get('items', [])
        if items:
            channel_id = items[0]['id']['channelId']
            return channel_id
        else:
            error_message = 'No channel ID found for the channel name: {}'.format(search_query)
            return error_message

    except HttpError as e:
        st.error('An HTTP error occurred:')
        st.error(e)

    return None

#function for getting channel_details

def get_channel_status(_youtube,channel_ids):

    all_data = []

    for channel_id in channel_ids:
        try:
            channel_response = youtube.channels().list(
            id=channel_id,
            part='snippet,statistics,contentDetails,status').execute()
            
            channel_items = channel_response.get('items', [])
                
            if len(channel_items) == 0:
                    st.error(f"No channel found for ID: {channel_id}")
                    continue

            channel_data = channel_response['items'][0]['snippet']
            channel= channel_response['items'][0]
            channel_statistics = channel_response['items'][0]['statistics']
            channel_description = channel_data['description']
            playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            # Create channel information dictionary
            channel_info = {
                "Channel_Name": channel_data['title'],
                "Channel_Id": channel_id,
                "Subscription_Count": int(channel_statistics['subscriberCount']),
                "Video_Count": int(channel_statistics['videoCount']),
                "Channel_Views": int(channel_statistics['viewCount']),
                "Channel_Description": channel_description,
                "Channel_Status": channel['status']['privacyStatus'],
                "Playlist_Name": channel_data['title'] + " Playlist",
                "Playlist_Id": playlist_id,
                "Videos": []
            }

            video_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,  # Fetch a maximum of 50 videos
            ).execute()

            video_items = video_response['items']

            for index, video_item in enumerate(video_items):
                video_data = video_item['snippet']
                video_id = video_data['resourceId']['videoId']

                # Fetch video statistics
                video_stats_response = youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=video_id
                ).execute()

                video_stats_data = video_stats_response['items'][0]
                video_stats = video_stats_data['statistics']

                # Check if comments are disabled for the video
                if 'commentCount' not in video_stats or int(video_stats['commentCount']) == 0:
                    continue

                # Create video information dictionary
                video_info = {
                    f"Video_Id_{index+1}": video_id,
                    "Video_Name": video_data['title'],
                    "Video_Description": video_data['description'],
                    "PublishedAt": video_data['publishedAt'],
                    "View_Count": int(video_stats['viewCount']),
                    "Like_Count": int(video_stats.get('likeCount', 0)),
                    "Dislike_Count": int(video_stats.get('dislikeCount', 0)),
                    "Favorite_Count": int(video_stats.get('favoriteCount', 0)),
                    "Comment_Count": int(video_stats.get('commentCount', 0)),
                    "Duration": video_stats_data['contentDetails']['duration'],
                    "Thumbnail": video_data['thumbnails']['default']['url'],
                    "Caption_Status": video_stats_data['contentDetails']['caption'],
                    "Comments": {}
                }

                # Fetch comment information
                try:
                    comment_response = youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=2
                    ).execute()

                    comment_items = comment_response['items']
                    comments = {}

                    for index,comment_item in enumerate(comment_items, start=1):
                        comment_snippet = comment_item['snippet']['topLevelComment']['snippet']
                        comment_id = comment_item['snippet']['topLevelComment']['id']
                        comment_info = {
                            f"Comment_Id_{index}": comment_id,
                            "Comment_Text": comment_snippet['textDisplay'],
                            "Comment_Author": comment_snippet['authorDisplayName'],
                            "Comment_PublishedAt": comment_snippet['publishedAt']
                        }
                        comments[comment_id] = comment_info

                    video_info["Comments"] = comments

                except Exception as e:
                    continue

                # Append video information to the channel's videos list
                channel_info["Videos"].append(video_info)

            all_data.append(channel_info)
        except HttpError as e:
                if e.resp.status == 403:
                    st.error("Access to channel data is forbidden. Please check your API credentials.")
                else:
                    st.error(f"Error fetching channel data for ID: {channel_id}")
                    st.error(e)

    return all_data

# Get the channel IDs from session state or initialize an empty list
channel_ids = st.session_state.get('channel_ids', [])



# Create the main page
def main_page():
    # Comfiguring Streamlit GUI 
    st.title("Youtube Data Harvesting and Warehousing")
    st.subheader("Architectural Diagram of the Project")
    image = Image.open('Location of the image ') #keep your image location here
    st.image(image, caption='Architectural Daigram')



#streamlit page for converting username to channel_id
def Username_Converter():
    st.title('YouTube Channel ID Converter')
    st.subheader('Converts username to channel_ID')

    # Input channel name
    channel_name = st.text_input('Enter YouTube Channel Name')

    if st.button('Get Channel ID'):
        if channel_name:
            try:
                channel_id = get_channel_id(channel_name)

                if channel_id:
                    st.success(f'The channel ID for {channel_name} is: {channel_id}')
                else:
                    st.error(f'No channel ID found for the channel name: {channel_name}')
            except HttpError as e:
                if e.resp.status == 403:
                    st.error("Access to channel data is forbidden. Please check your API credentials.")
                else:
                    st.error(f"Error fetching channel data: {str(e)}")
        else:
            st.warning('Please enter a YouTube channel name.')



# Create the Single Select page
def single_select_page():
    st.title("Youtube Data Collection for Single Channel_ID")
    st.subheader("Enter a YouTube Channel ID")
    channel_id_single = st.text_input("Channel ID")
    
    if st.button("Fetch Channel Data"):
        if channel_id_single:
                if len(channel_id_single)>0:

                    channel_ids = [channel_id_single]
                    st.session_state['channel_ids'] = channel_ids
                    channel_data_single = get_channel_status(youtube, channel_ids)

                    # Create an empty dataframe
                    df = pd.DataFrame(columns=[
                        "Channel_Name",
                        "Subscription_Count",
                        "Video_Count",
                        "Playlist_Id",
                        "Video_Name",
                        "Video_Description",
                        "Like_Count"
                    ])

                    # Iterate over the channel data and populate the dataframe
                    for channel_info in channel_data_single:
                        for video_info in channel_info['Videos']:
                            video_df = pd.DataFrame([{
                                "Channel_Name": channel_info["Channel_Name"],
                                "Subscription_Count": channel_info["Subscription_Count"],
                                "Video_Count": channel_info["Video_Count"],
                                "Playlist_Id": channel_info["Playlist_Id"],
                                "Video_Name": video_info["Video_Name"],
                                "Video_Description": video_info["Video_Description"],
                                "Like_Count": video_info["Like_Count"]
                            }])
                            df = pd.concat([df, video_df], ignore_index=True)

                    if not df.empty:
                        # Display the dataframe
                        st.dataframe(df.iloc[0:10])
                                                
                        # Group the data by 'Channel_Name' and calculate the sum of 'Like_Count' and 'Dislike_Count'
                        grouped_df = df.groupby('Channel_Name')[['Like_Count', 'Subscription_Count']].sum().reset_index()

                        # Bar plot for 'Like_Count'
                        fig1 = px.bar(grouped_df, x='Channel_Name', y='Like_Count', color='Channel_Name',
                                    title='Likes Count by Channel')
                        fig1.update_layout(xaxis_tickangle=-45, xaxis_title='Channel Name', yaxis_title='Count')

                        # Bar plot for 'Dislike_Count'
                        fig2 = px.bar(grouped_df, x='Channel_Name', y='Subscription_Count', color='Channel_Name',
                                    title='Subscription Count by Channel')
                        fig2.update_layout(xaxis_tickangle=-45, xaxis_title='Channel Name', yaxis_title='Count')

                        # Display the plots in Streamlit
                        st.plotly_chart(fig1)
                        st.plotly_chart(fig2)
                    else:
                        st.warning('No data found for the provided channel ID.')

#Function for insering data into Mongodb atlas
def insert_data_to_mongodb(channel_data_multiselect):
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['strawberry']  # Replace 'strawberry' with the name of your MongoDB database
    collection = db['icecream']  # Replace 'icecream' with the name of your MongoDB collection
    channel_data_multiselect = get_channel_status(youtube, channel_ids)
    data = [d for d in channel_data_multiselect if isinstance(d, dict)]
    if data:
        collection.insert_many(data)
    client.close()

#Function for dropping the collection
def delete_collection():
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['strawberry']  # Replace 'strawberry' with the name of your MongoDB database
    collection_name = 'icecream'  # Replace 'icecream' with the name of your MongoDB collection

    # Check if the collection exists
    if collection_name in db.list_collection_names():
        # Drop the collection
        db[collection_name].drop()
        st.success("Collection '{}' has been deleted.".format(collection_name))
    else:
        st.info("Collection '{}' does not exist.".format(collection_name))

    client.close()


# Create the Multi Select page for selecting multple channel_ids
def multi_select_page():
    st.title("Data Upload to MongoDB")
    # Take channel_ids as input from the user
    channel_ids_multiselect = st.text_input("Enter Channel IDs (separated by comma)", value="")

    channel_data_multiselect = None  # Define the variable outside the if block

    
    col1,col2 = st.columns(2)

    with col1:

      if st.button('Fetch Youtube Data'):
        if channel_ids_multiselect:

            channel_ids = [channel_id.strip() for channel_id in channel_ids_multiselect.split(",")]

            st.session_state['channel_ids'] = channel_ids
            try:

                channel_data_multiselect = get_channel_status(youtube, channel_ids)
                if channel_data_multiselect:
                    st.session_state['channel_data_multiselect'] = channel_data_multiselect
                    st.success("YouTube data fetched successfully!")
            except Exception as e:
                    if "quota" in str(e):
                        st.warning("Request limit exceeded. Please try again tomorrow.")
                    else:
                        st.error(f"Error fetching YouTube data: {str(e)}")
        else:
            st.error("Please enter valid channel_ids")

    with col2:

        if st.button('Show YouTube Channel Data'):

            with st.expander('Youtube CHannel Data'):

                channel_data_multiselect = st.session_state.get('channel_data_multiselect')

                if 'channel_data_multiselect'!=None:

                    json_data = json.dumps(channel_data_multiselect)  # Convert to JSON-formatted string

                    # Display the JSON data
                    try:
                        parsed_json = json.loads(json_data)
                        st.json(parsed_json)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON data.")
                else:
                    st.info("No data found. Please check the provided channel ID(s).")
        
    st.title('Insert youtube Data into MongoDB')

    col3,col4 = st.columns(2)

    # Button to upload data
    with col3:
        if st.button("Upload Data to MongoDB"):

            channel_data_multiselect = st.session_state.get('channel_data_multiselect')

            if channel_data_multiselect:
        
            # Extract dictionaries from the list
                data = [d for d in channel_data_multiselect if isinstance(d, dict)]

                if data:

                    insert_data_to_mongodb(data)

            # Display success message
                    st.success("Data inserted into MongoDB successfully!")

                else:
                    st.warning("No data found. Please check the provided channel ID(s).")
            
    with col4:

        if st.button("Delete MongoDB Collection"):
          deleted = delete_collection()
          if deleted:
            st.success('Deleted MongoDB collection')
          else:
              st.warning('No Collection exists, you can Fetch the data from youtube')

    st.title('Upload Data SQL Database')

    if 'data_uploaded' not in st.session_state:
        st.session_state['data_uploaded'] = False

    if st.button('Insert Data into SQL'):
        update_data()
        st.session_state['data_uploaded'] = True
        st.success('Data inserted into SQL successfully!')
    
    # Question selection dropdown (visible only after data is uploaded)
    if st.session_state['data_uploaded']:
        conn = sqlite3.connect('data.db')  # Replace with your database path
        cursor = conn.cursor()

        # Dropdown to select question and display answer
        selected_question = st.selectbox('Select a question', options=[
                                                '1.What are the names of all the videos and their corresponding channels?', 
                                                '2.Which channels have the most number of videos, and how many videos do they have?', 
                                                '3.What are the top 10 most viewed videos and their respective channels?', 
                                                '4.How many comments were made on each video, and what are their corresponding video names?', 
                                                '5.Which videos have the highest number of likes, and what are their corresponding channel names?', 
                                                '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?', 
                                                '7.What is the total number of views for each channel, and what are their corresponding channel names?', 
                                                '8.What are the names of all the channels that have published videos in the year 2022?', 
                                                '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?', 
                                                '10.Which videos have the highest number of comments, and what are their corresponding channel names?'])

        # Query and display data based on the selected question
        if selected_question:
            result = execute_query(selected_question)
            if not result.empty:
                # result_df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
                st.table(result)
            else:
                st.write('No data available for the selected question.')

        conn.close()
                    

# Run the app
def main():
    # Create a sidebar with page selection
    page = st.sidebar.selectbox("Select a Page", ["Main Page","Username Converter", "Single Select","Multi Select"])

    # Render the selected page
    if page == "Main Page":
        main_page()
    elif page=='Username Converter':
        Username_Converter()
    elif page == "Single Select":
        single_select_page()
    elif page == "Multi Select":
        multi_select_page()

if __name__ == '__main__':
    main()
