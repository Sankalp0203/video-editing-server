import os
from pytube import YouTube
import yaml

from googleapiclient.discovery import build
from datetime import datetime
import json
from pytube import YouTube
import os

from video_wizard_server.utils import load_config_file

class Youtube:

    def __init__(self) -> None:
        self.config = load_config_file()
        self.api_key = self.config.get("youtube", {}).get("api", {}).get("key")
        self.api_version = self.config.get("youtube", {}).get("api", {}).get("version")
        self.api_service_name = self.config.get("youtube", {}).get("api", {}).get("service_name")
        self.output_dir = self.config.get("youtube", {}).get("output_dir")

    # Function to fetch videos from a channel
    def get_channel_videos(self, channel_id):
        youtube = build(self.api_service_name, self.api_version, developerKey=self.api_key)

        # Retrieve the uploads playlist ID for the given channel
        channels_response = youtube.channels().list(part='contentDetails', id=channel_id).execute()
        playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Retrieve the videos from the uploads playlist
        playlist_items = youtube.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=50).execute()

        videos = []
        for item in playlist_items['items']:
            video_id = item['snippet']['resourceId']['videoId']
            videos.append(video_id)

        return videos

    def download_youtube_videos(self, url):
        try:
            yt = YouTube(url)
            video_id = yt.video_id
            stream = yt.streams.get_highest_resolution()
            output_path = os.path.join(self.output_dir, f"{video_id}.mp4")
            stream.download(output_path)
            print(f"Downloaded video: {yt.title}")
            return video_id, output_path
        except Exception as e:
            print(f"Error: {str(e)}")
            return None, None
        


    # Function to get videos from a channel created after a certain date
    def get_videos_after_date(self, channel_id, date):
        all_videos = self.get_channel_videos(channel_id)
        filtered_videos = []

        for video_id in all_videos:
            video_info = YouTube(f'https://www.youtube.com/watch?v={video_id}')
            video_date = datetime.strptime(video_info.publish_date, "%Y-%m-%d")
            if video_date > date:
                filtered_videos.append(video_id)

        return filtered_videos
