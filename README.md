# get-youtube-videos

## To run:
`python youtube_test.py`

**channel_id_mapping.pickle**

    Map[Channel Name] -> Channel ID

**channel_query.pickle**

    Keys: channel names

        Keys: 
    
          - title = [title1, title2]
          - id    = [id1   , id2   ]
          - year  = [year1 , year2 ]
      
**video_query.pickle**

    Keys: video IDs

        Keys: 
          - title        = [title]
          - description  = [desc]
          - tags         = [tag1, tag2, ... ]
          - viewCount    = [views]
          - likeCount    = [likes]
      
**transcript_query.pickle**

    Map[Video ID] -> Transcript
