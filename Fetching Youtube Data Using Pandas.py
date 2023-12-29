#Below Code Fetch 10 Youbube channels Data using Pandas
#In Channels data we get youtube ID,NAME,DESCRIPTION,VIDEO COUNT,VIEW COUNT,PLAYLIST ID.
#For Videos data, required to give input as index number of channel data to get video details of certain channel,we get TITLE,PUBLISHED DATE,VIEWS,LIKES,COMMENT.
#For Comments data, required to give input as index number of video data to get comment details of certain video,we get PERSON,DATE,COMMENTS

from googleapiclient.discovery import build
from pprint import pprint
import pandas as pd
api_key="AIzaSyChhMKO3CznRrrb9wjT8XS6Nwr426fR9Hc"
api_service_name="youtube"
api_version="v3"
channels_id="UCV8e2g4IWQqK71bbzGDEI4Q,UCh9nVJoWXmFb7sLApWGcLPQ,UCiT9RITQ9PW6BhXK0y2jaeg,UCoOae5nYA7VqaXzerajD0lg,UCwr-evhuzGZgDFrq_1pLt_A,UCJcCB-QYPIBcbKcBQOTwhiA,UCnz-ZXXER4jOvuED5trXfEA,UCmKaoNn0OvxVAe7f_8sXYNQ,UCXhbCCZAG4GlaBLm80ZL-iA,UCpNUYWW0kiqyh0j5Qy3aU7w"
youtube = build(
        api_service_name, api_version, developerKey=api_key)
# Chennal Details
def youtubedata(channels_id):
    data=[]
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channels_id
    )
    response = request.execute()
    for i in range(10):
        extracteddata=dict(id=response["items"][i]['id'],name=response["items"][i]["snippet"]["title"],description=response["items"][i]["snippet"]["description"],sub_count=response["items"][i]["statistics"]["subscriberCount"],video_count=response["items"][i]["statistics"]["videoCount"],view_count=response["items"][i]["statistics"]["viewCount"],playlist_id=response["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"])
        data.append(extracteddata)
    
    return data
datacombo=youtubedata(channels_id)
channels_data=pd.DataFrame(datacombo)
print("CHANNEL DATA")
print(channels_data)
#Funtion to get video ids
user_input = input("Enter playlist index: ")
user_input=int(user_input)
playlist_id=channels_data["playlist_id"][user_input]
#print(playlist_id)
def get_video_ids(youtube,playlist_id):
    request = youtube.playlistItems().list(
               part="snippet,contentDetails",
               playlistId=playlist_id,
               maxResults=50)
    response = request.execute()

    video_ids=[]

    for i in range(len(response["items"])):
        video_ids.append(response["items"][i]["contentDetails"]["videoId"])
    next_page_token=response.get("nextPageToken")
    more_pages=True
    while more_pages:
        if next_page_token is None:
            more_pages=False
        else:
            request = youtube.playlistItems().list(
               part="snippet,contentDetails",
               playlistId=playlist_id,
               maxResults=50,
               pageToken=next_page_token)
            response = request.execute()
            for i in range(len(response["items"])):
                video_ids.append(response["items"][i]["contentDetails"]["videoId"])
            next_page_token=response.get("nextPageToken")
    return video_ids
video_ids=get_video_ids(youtube,playlist_id)
#print(video_ids)
#Function to get video details
def get_video_details(youtube,video_ids):
    all_video_status=[]
    for i in range(0,len(video_ids),50):
        request=youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids[i:i+50]))
        response=request.execute()
        for video in response["items"]:
            video_status=dict(Title=video["snippet"]["title"],Published_date=video["snippet"]["publishedAt"],Views=video["statistics"]["viewCount"],Likes=video["statistics"]["likeCount"],Comments=video["statistics"]["commentCount"])
            all_video_status.append(video_status)
    return all_video_status
    
video_details=get_video_details(youtube,video_ids)
video_data=pd.DataFrame(video_details)
print("VIDEO DATA")
print(video_data)
#Function to get comment details
user_input = input("Enter comment index: ")
user_input=int(user_input)
video_ids=video_ids[user_input]
#print(video_ids)
all_video_comments=[]
request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_ids,
        maxResults=100)
response = request.execute()
for i in range(len(response["items"])):
  video_comments=dict(Person=response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],Date=response["items"][i]["snippet"]["topLevelComment"]["snippet"]["publishedAt"],Comments=response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
  all_video_comments.append(video_comments)  
comment_details=pd.DataFrame(all_video_comments)    
print("COMMENT DATA")
print(comment_details)








