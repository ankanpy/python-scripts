import yt_dlp
from tqdm import tqdm

def download_instagram_reel(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download best video and best audio and merge them
        'progress_hooks': [tqdm_hook],
        'merge_output_format': 'mp4',  # Ensure output is merged into mp4
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Convert to mp4 if necessary
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print("Available formats:")
        for fmt in info['formats']:
            resolution = fmt.get('format_note', fmt.get('resolution', 'Unknown resolution'))
            ext = fmt.get('ext', 'Unknown extension')
            format_id = fmt.get('format_id', 'Unknown format ID')

            print(f"Resolution: {resolution}, Extension: {ext}, Format ID: {format_id}")
        
        # Ask user to select the format
        format_id = input("Enter the Format ID of the resolution you want to download: ")
        
        # Set selected format for video + audio merge
        ydl_opts['format'] = f'{format_id}+bestaudio/best'

        # Download the reel and merge video + audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def tqdm_hook(d):
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes', 0)
        downloaded_size = d.get('downloaded_bytes', 0)
        if total_size > 0:
            with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                pbar.update(downloaded_size)

if __name__ == "__main__":
    reel_url = input("Enter the Instagram reel URL: ")
    download_instagram_reel(reel_url)