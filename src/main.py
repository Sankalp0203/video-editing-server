from utils import load_config_file
from youtube_video_downloader import download_youtube_videos, get_channel_videos

class Main:

    def start_app():
        config = load_config_file()
        print(config)
        
        #load channel ids from config yaml
        channel_ids = config.get("youtube", {}).get("channel_ids")
        filtered_videos = []
        for channel_id in channel_ids:
            filtered_videos = get_channel_videos(channel_id)
        for video in filtered_videos:
            download_youtube_videos(video)
            
if __name__ == "__main__":
    Main.start_app()
