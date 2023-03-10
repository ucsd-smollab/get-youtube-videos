# get-youtube-videos

## Overview
This program was designed to retrieve Youtube videos from select companies fitting a certain criteria of content. It is to be utilized for research and analyzing the promotion of privacy within tech companies.

## Functionality
This program gathers data from six companies (Apple, WhatsApp, DuckDuckGo, Google, Brave, and NordVPN) and retrieves videos with either the title or description containing the words "privacy" or "private."

Five files are created, outlined below:

### 1. channel_id_mapping.pickle

    Map[Channel Name] -> Channel ID

This file contains a dictionary data structure mapping the company/channel name to the Youtube channel ID.

### 2. channel_query.pickle

    Keys: channel names
        Keys: 
          - title = [title1. , title2  ]
          - id    = [videoId1, videoId2]
          - year  = [year1   , year2   ]
      
This file contains a data structure mapping each channel name to another dictionary of lists, containing information about all desired videos within a channel. Elements of the same index within each list all correspond to the same video.
      
### 3. video_query.pickle

    Keys: video IDs
        Keys: 
          - title        = [title]
          - description  = [desc]
          - tags         = [tag1, tag2, ... ]
          - viewCount    = [views]
          - likeCount    = [likes]
      
This file contains a data structure mapping each video's ID to another dictionary of lists, containing information about the desired video. Each key video ID corresponds to another dictionary holding the video's details, including title, description, tags, number of views, and number of likes.
      
### 4. transcript_query.pickle

    Map[Video ID] -> Transcript

This file contains a dictionary data structure mapping each video's ID to a string of the video's transcript. This function utilizes user jdepoix's [Youtube Transcript API](https://github.com/jdepoix/youtube-transcript-api).

### 5. yt_privacy_videos.csv

This csv file contains a summary of each collected video and relevant information, including video ID, title, description, tags, number of views, and number of likes.

## To Run
`python youtube_test.py`

## Notes
To view any of the collected videos, use the video URL by the format ```youtu.be/[videoID]```.
