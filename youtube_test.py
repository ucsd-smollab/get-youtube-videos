# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import io
import csv
import pickle
from pathlib import Path
from collections import defaultdict
from googleapiclient.http import MediaIoBaseDownload
from youtube_transcript_api import YouTubeTranscriptApi

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl", "https://www.googleapis.com/auth/youtubepartner"]
MAX_RESULTS = 50

def dd():
    return defaultdict(list)

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "../client_secret_675983259930-v8nltr8b398b85mp4dbafueul7ub7s6f.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    ######################################################

    # ----------------------- Search Query -----------------------
    path = Path('./channel_id_mapping.pickle')
    if not path.is_file():
        target_channels = ["Apple", "WhatsApp", "@duckduckgo2597", "@Google", "@BraveSoftware", "@Nordvpn"]

        channel_id_mapping = defaultdict(str)

        for c in target_channels:
            # Execute the request
            request = youtube.search().list(
                part = "snippet",
                type = "channel",
                q = c
            )
            response = request.execute()

            print(response)

            # Add channel IDs to our dict if the first result matches our query
            
            # if response["items"][0]["snippet"]["channelTitle"] == c:
            
            # adds in first channel search result to channel_id_mapping
            channel_id_mapping[c] = response["items"][0]["snippet"]["channelId"]

        file = open("channel_id_mapping.pickle", "wb")
        pickle.dump(channel_id_mapping, file)
        file.close()
    else:
        file = open("channel_id_mapping.pickle", "rb")
        channel_id_mapping = pickle.load(file)
        print("loaded channel_id_mapping!")
        file.close()
        
    print(channel_id_mapping)

    # ----------------------- Channel Query -----------------------

    # Keys: channel names
    #     -> Keys: 
    #             - title = [title1, title2]
    #             - id    = [id1   , id2   ]
    #             - year  = [year1 , year2 ]
    
    path = Path('./channel_query.pickle')
    if not path.is_file():
        channel_query = defaultdict(dd)

        for company, channel_id in channel_id_mapping.items():
            # Execute the request
            request = youtube.search().list(
                part = "snippet",
                type = "video",
                q = "privacy",
                channelId = channel_id,
                maxResults = 50
            )
            response = request.execute()
            for i in range(len(response["items"])):
                video = response["items"][i]
                title = video["snippet"]["title"]
                description = video["snippet"]["description"] ####
                privacy_title = "privacy" in set(title.lower().split(' '))
                private_title = "private" in set(title.lower().split(' '))
                privacy_descr = "privacy" in set(description.lower().split(' '))
                private_descr = "private" in set(description.lower().split(' '))
                if privacy_title or private_title or privacy_descr or private_descr:
                    video_id = video["id"]["videoId"]
                    year = video["snippet"]["publishedAt"][:4]
                    channel_query[company]["title"].append(title)
                    channel_query[company]["id"].append(video_id)
                    channel_query[company]["year"].append(year)
        file = open("channel_query.pickle", "wb")
        pickle.dump(channel_query, file)
        file.close()
    else:
        file = open("channel_query.pickle", "rb")
        channel_query = pickle.load(file)
        print("loaded channel_query!")
        file.close()

    # Keys:   company names
    # Values: list of video ids
    privacy_videos = defaultdict(list)

    # print num vids for each company
    count = 0
    for k, v in channel_query.items():
        c_name = k
        for i in v["id"]:
            privacy_videos[c_name].append(i)
            count += 1
    
    for k, v in privacy_videos.items(): 
        print(k) # company name
        print(len(v)) # number of videos per company

    print("Total number of privacy videos retrieved:", count)
    
    # video_query
    # Keys: video IDs
    #     -> Keys: 
    #             - title        = [title]
    #             - description  = [desc]
    #             - tags         = [tag1, tag2, ... ]
    #             - viewCount    = [views]
    #             - likeCount    = [likes]
    
    # ----------------------- Video Query -----------------------
    path = Path('./video_query.pickle')
    if not path.is_file():
        video_query = defaultdict(dd)
        for company, video_list in privacy_videos.items():
            for v in video_list:
                # Execute the request
                request = youtube.videos().list(
                    part = "snippet, statistics",
                    id = v
                )
                response = request.execute()
                video_query[v]["title"].append(response["items"][0]["snippet"]["title"])
                video_query[v]["description"].append(response["items"][0]["snippet"]["description"])
                try:
                    video_query[v]["tags"].append(response["items"][0]["snippet"]["tags"])
                except KeyError:
                    print("video", v, "has no tags")
                video_query[v]["viewCount"].append(response["items"][0]["statistics"]["viewCount"])
                try:
                    video_query[v]["likeCount"].append(response["items"][0]["statistics"]["likeCount"])
                except KeyError:
                    print("video", v, "has no viewCount")
        file = open("video_query.pickle", "wb")
        pickle.dump(video_query, file)
        file.close()
    else:
        file = open("video_query.pickle", "rb")
        video_query = pickle.load(file)
        print("loaded video_query!")
        file.close()


    # ----------------------- Transcript Query -----------------------
    subtract_videos = {"BBKOj7E9SfI", "vT0QRd937KM","X4K4JsBXWP8", "lWs3I8zieds", "fiXaHv_9rmQ"}
    for k, v in privacy_videos.items():
        privacy_videos[k] = list(set(privacy_videos[k]) - subtract_videos)
    

    path = Path('./transcript_query.pickle')
    if not path.is_file():
        transcript_query = defaultdict(str)
        for _, video_list in privacy_videos.items():
            for v in video_list:
                t_dict = YouTubeTranscriptApi.get_transcript(v, languages=['en'])
                words = []
                for d in t_dict:
                    words.append(d["text"])
                full_transcript = ' '.join(words)
                formatted = full_transcript.replace('\n', ' ').replace("\'", "'").replace("\xa0", "")
                transcript_query[v] = formatted
        file = open("transcript_query.pickle", "wb")
        pickle.dump(transcript_query, file)
        file.close()
    else:
        file = open("transcript_query.pickle", "rb")
        transcript_query = pickle.load(file)
        print("loaded transcript_query!")
        file.close()
        
    # video_query
    # Keys: video IDs
    #     -> Keys: 
    #             - title        = [title]
    #             - description  = [desc]
    #             - tags         = [tag1, tag2, ... ]
    #             - viewCount    = [views]
    #             - likeCount    = [likes]
    
    # ------------------ CSV ------------------

    # open the file in the write mode
    file = open('yt_privacy_videos', 'w')
    
    header = ["Video ID", "Title", "Description", "Tags", "Views", "Likes"]

    # create the csv writer
    writer = csv.writer(file)

    # write a header to the csv file
    writer.writerow(header)
    
    # Logic for looping and writing video id rows
    for v_id, d in video_query.items():
        row_data = [v_id]
        for k, v in d.items():
            row_data.append(v)
        writer.writerow(row_data)
        
    # close the file
    file.close()

if __name__ == "__main__":
    main()