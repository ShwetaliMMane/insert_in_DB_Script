# ------------video in english-------------

import pandas as pd
from youtubesearchpython import VideosSearch
import numpy

def recipe_video(query):
    try:
        search = VideosSearch(query, limit=1)  
        result = search.result()

        
        if len(result['result']) > 0:
            video = result['result'][0]
            return video['title'], video['link']
        else:
            return None, None
    except Exception as e:
        print(e)
        print("error occurred")
        return None, None


try:
    df = pd.read_csv("C:\\Users\\shwet\\Downloads\\com_not_found_On_website.csv",encoding='ISO-8859-1')  
    df=df.iloc[:2]
except Exception as e:
        print(e)
        print("error occurred")


urls = []


for recipe_name in df['recipe_name']:  
    print(f"Fetching video for: {recipe_name}")
    try:
        title, url = recipe_video(recipe_name)
        
      
        urls.append(url)
    except Exception as e:
        print(e)
        print("error occurred")
        urls.append(None)



df['Video URL'] = urls


try:
    df.to_csv('C:\\Users\\shwet\\Downloads\\oct_month_video.csv', index=False)
    print("Videos saved successfully!")
except Exception as e:
        print(e)
        print("error occurred")



# import pandas as pd
# import requests
# import numpy as np

# def recipe_video(api_key, query):
#     try:
#         search_query = f"how to make {query} recipe in English"
#         url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&key={api_key}&maxResults=5"
        
#         response = requests.get(url)
#         data = response.json()

#         # Check for results
#         if 'items' in data and len(data['items']) > 0:
#             for item in data['items']:
#                 title = item['snippet']['title']
#                 video_id = item['id'].get('videoId')
#                 if video_id:  # Make sure it's a video
#                     return title, f"https://www.youtube.com/watch?v={video_id}"
#         return None, None
#     except Exception as e:
#         print(f"Error occurred while fetching video for '{query}':", e)
#         return None, None

# # Your API Key
# API_KEY = 'AIzaSyDUX_qvSdAB_UO5P3Y3Mh-YJ__mNEKIjBU'

# try:
#     df = pd.read_csv("C:\\any\\db\\UK_rearrange_matched_data.csv",encoding='ISO-8859-1')  
#     df = df.iloc[:3]  # Limiting to the first 10 recipes for testing
# except Exception as e:
#     print(e)
#     print("Error occurred while reading the CSV file")

# urls = []

# for recipe in df['name']:  
#     print(f"Fetching video for: {recipe}")
#     try:
#         title, url = recipe_video(API_KEY, recipe)
#         urls.append(url)
#     except Exception as e:
#         print(f"Error occurred during video fetch for '{recipe}':", e)
#         urls.append(None)
#         print(urls)

# # Add the video URLs to the DataFrame
# df['Video URL'] = urls

# try:
#     df.to_csv("C:\\Users\\shwet\\Downloads\\UK_not_matched_recipes1.csv", index=False)
#     print("Videos saved successfully!")
# except Exception as e:
#     print(e)
#     print("Error occurred while saving the CSV file")


