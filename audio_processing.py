import yt_dlp
import subprocess
import os

def get_audio_from_youtube(url, output_path="temp_audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'noplaylist': True,
        'extractaudio': True,
        'audioformat': 'mp3',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        print("Failed to download YouTube video:", e)
        return None

def get_audio_from_file(file):
    temp_input = file.name
    with open(temp_input, "wb") as f:
        f.write(file.read())

    audio_path = "temp_audio_from_file.mp3"
    try:
        # Use ffmpeg to extract audio
        cmd = [
            "ffmpeg",
            "-y",  # overwrite
            "-i", temp_input,
            "-vn",  # no video
            "-acodec", "mp3",
            audio_path
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove(temp_input)
        return audio_path
    except Exception as e:
        print("Failed to extract audio:", e)
        return None