import os
import yt_dlp


# Function to download and convert audio to MP3 using yt-dlp and embed metadata
def download_audio(url, save_path, cookies_file=None):
    # yt-dlp options for downloading audio and embedding metadata automatically
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {
                "key": "FFmpegMetadata",  # Automatically embed metadata
            },
        ],
        "quiet": True,
        "cookiefile": cookies_file,  # Optional: use cookies if provided
    }

    # Download the audio and embed metadata automatically
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        if "premium" in str(e).lower():
            print(f"Skipping premium-only content: {url}")
        else:
            print(f"Error downloading {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Function to check if an MP3 already exists
def file_exists(title, save_path):
    mp3_file = os.path.join(save_path, f"{title}.mp3")
    return os.path.isfile(mp3_file)


# Function to download the playlist and automatically embed metadata for each video
def download_playlist(playlist_url, save_path, cookies_file=None):
    ydl_opts = {
        "quiet": True,
        "extract_flat": False,  # Extract full metadata for each video
        "cookiefile": cookies_file,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)

        print(f'Downloading playlist: {playlist_info["title"]}')

        # Create folder if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for video in playlist_info["entries"]:
            video_url = f'https://www.youtube.com/watch?v={video["id"]}'
            title = video["title"]

            # Check if the file already exists before downloading
            if file_exists(title, save_path):
                print(f"Skipping '{title}' - already exists.")
            else:
                print(f"Downloading: {title}")
                download_audio(video_url, save_path, cookies_file)

    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading playlist: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing playlist: {e}")


# Function to download a single video and automatically embed metadata
def download_single_video(video_url, save_path, cookies_file=None):
    ydl_opts = {
        "quiet": True,
        "cookiefile": cookies_file,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video_url, download=False)
            title = video_info["title"]

            # Check if the file already exists before downloading
            if file_exists(title, save_path):
                print(f"Skipping '{title}' - already exists.")
            else:
                print(f"Downloading: {title}")
                download_audio(video_url, save_path, cookies_file)

    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading video: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Function to determine if the URL is a playlist or a single video
def process_url(url, save_path, cookies_file=None):
    ydl_opts = {
        "quiet": True,
        "cookiefile": cookies_file,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if "entries" in info:  # If 'entries' exists, it's a playlist
                download_playlist(url, save_path, cookies_file)
            else:
                download_single_video(url, save_path, cookies_file)
    except yt_dlp.utils.DownloadError as e:
        print(f"Error processing URL {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing URL: {e}")


if __name__ == "__main__":
    # Add your URLs here (both playlists and single videos)
    urls = [
        "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID1",
        "https://www.youtube.com/watch?v=YOUR_VIDEO_ID1",
        # Add more playlists or videos if needed
    ]

    # Folder to save downloaded MP3s
    save_folder = "downloaded_songs"

    # Path to the exported cookies file (optional)
    cookies_file = None  # Set to 'cookies.txt' if you have a Premium account

    for url in urls:
        process_url(url, save_folder, cookies_file)
    print("Completed download of all songs!")
