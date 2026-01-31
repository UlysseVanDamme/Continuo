"""
This script listens to a specified MIDI input port, records incoming MIDI messages,
and saves them to a MIDI file after a period of inactivity (default set to 15 seconds). 
The saved MIDI files are uploaded to an AWS S3 bucket using credentials stored in environment.
"""

import mido
import time
import os
import threading
import boto3
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

PORT_NAME = os.getenv("PORT_NAME")
SAVE_DIR = "midi-files"
BUCKET_NAME = os.getenv("BUCKET_NAME")
SILENCE_THRESHOLD = 15.0
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
REGION = os.getenv("AWS_REGION")

os.makedirs(SAVE_DIR, exist_ok=True)

# Initializes AWS S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)


def upload_to_s3(filepath):
    """
    Uploads local file to AWS S3 bucket using filepath.
    """
    filename = os.path.basename(filepath)
    try:
        s3_client.upload_file(filepath, BUCKET_NAME, filename)
        print(f"Uploaded to AWS")
    except Exception as e:
        print(f"Uploading Error: {e}")


def save_midi(buffer, start_time):
    """
    Safes the recorded MIDI data from the buffer to a MIDI file. 
    Filename is based on the time of recording. 
    After saving, it uploads to S3 using the upload_to_s3 function. 
    """
    if not buffer: return
    timestamp = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d_%H-%M-%S')
    filepath = os.path.join(SAVE_DIR, f"{timestamp}.mid")

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    ticks_per_sec = 960
    last_time = start_time
    for msg, msg_time in buffer:
        delta = int((msg_time - last_time) * ticks_per_sec)
        msg.time = delta
        track.append(msg)
        last_time = msg_time

    mid.save(filepath)
    # Threaded so recording isn't blocked by upload
    threading.Thread(target=upload_to_s3, args=(filepath,), daemon=True).start()


def main():
    """
    Main loop that listens to MIDI input based on PORT_NAME.
    After SILENCE_THRESHOLD (default 15 seconds) seconds of inactivity, it saves the recorded MIDI messages.
    """
    try:
        with mido.open_input(PORT_NAME) as inport:
            buffer, recording, last_activity, session_start = [], False, time.time(), 0
            while True:
                msg = inport.receive(block=False)
                now = time.time()
                if msg:
                    if msg.type == 'active_sensing': continue
                    if not recording:
                        recording, session_start = True, now
                    buffer.append((msg, now))
                    last_activity = now
                elif recording and (now - last_activity > SILENCE_THRESHOLD):
                    save_midi(buffer, session_start)
                    buffer, recording = [], False
                time.sleep(0.001)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
