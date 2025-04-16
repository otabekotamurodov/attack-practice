# utils.py
import aiohttp
import asyncio
import os
import subprocess

SAVE_DIR = 'saved_videos'
os.makedirs(SAVE_DIR, exist_ok=True)


async def download_file(url, filename, filetype, update_progress):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    total = int(resp.headers.get('Content-Length', 0))
                    downloaded = 0
                    chunk_size = 1024 * 32  # 32KB

                    with open(filename, 'wb') as f:
                        while True:
                            chunk = await resp.content.read(chunk_size)
                            if not chunk:
                                break
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = int(downloaded / total * 100)
                            await update_progress(filetype, percent)
                    return True
    except Exception as e:
        print(f"[XATO] {filetype}: {e}")
    return False


async def download_and_merge(video_url, audio_url, output_name, progress_callback=None):
    video_path = os.path.join(SAVE_DIR, 'temp_video.mp4')
    audio_path = os.path.join(SAVE_DIR, 'temp_audio.mp4')
    output_path = os.path.join(SAVE_DIR, output_name)

    async def update_progress(filetype, percent):
        log_msg = f"{filetype.upper()} yuklanmoqda: {percent}%"
        print(log_msg)
        if progress_callback:
            await progress_callback(log_msg)

    v_ok = await download_file(video_url, video_path, 'video', update_progress)
    a_ok = await download_file(audio_url, audio_path, 'audio', update_progress)

    if not (v_ok and a_ok):
        return False

    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c', 'copy',
        output_path
    ]
    print("[FFMPEG] Bajariladigan komanda:")
    print(' '.join(cmd))

    if progress_callback:
        await progress_callback(f"<b>[FFMPEG]</b> Bajariladigan komanda:\n<code>{' '.join(cmd)}</code>")

    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(video_path)
        os.remove(audio_path)
        return True
    except Exception as e:
        print(f"[FFMPEG XATO] {e}")
        return False


async def check_if_segment(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as resp:
                headers = dict(resp.headers)
                # Agar bu HEAD so'rovni ko'tarmasa, GET bilan fallback
                if resp.status >= 400:
                    async with session.get(url, headers={'Range': 'bytes=0-10'}) as alt_resp:
                        headers = dict(alt_resp.headers)
                if 'Content-Range' in headers:
                    return True
    except Exception as e:
        print(f"[HEADER TEKSHIRISH XATO] {e}")
    return False
