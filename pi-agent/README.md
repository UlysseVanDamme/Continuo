# Automatic MIDI Recorder

The goal of this script is to record MIDI data from a digital piano and
automatically upload it to an S3 bucket.

It is recommended to run this script as a daemon, so there is no need to
manually start or stop it. I personally run it on a Raspberry Pi that is
always powered on and connected to my digital piano.


### 1. Install Python and dependencies

Ensure Python 3.9 or newer is installed.

Install required Python packages:

```bash
pip install mido boto3 python-dotenv
```

### 2. Create a .env file:

Make sure the script has access to the following environment variables:
```
PORT_NAME=Your MIDI Device Name
BUCKET_NAME=your-s3-bucket
AWS_ACCESS_KEY=your-access-key
AWS_SECRET_KEY=your-secret-key
AWS_REGION=us-east-1
```

To find your MIDI piano name, you can run this command in a python script:

```python
import mido
print(mido.get_input_names())
```

Or run this in a Linux terminal and look for the appropriate device: 

```bash
aconnect -l
```

## Run the script normally
You can run the script normally using: 
```bash
python auto-recorder.py
```

## Run as daemon

It is recommended to run it as a daemon on a device that's always connected to the digital piano, so there is no need to start/stop the script manually.

### 1. Create a systemd file:

```bash
sudo nano /etc/systemd/system/midi-recorder.service
```

Paste this code inside and adjust paths as needed

```ini
[Unit]
Description=Automatic MIDI Recorder
After=network.target

[Service]
ExecStart=/usr/bin/python /home/pi/path/to/auto-recorder.py
WorkingDirectory=/home/pi/path/to/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

### 2. Run systemd file

```bash
sudo systemctl daemon-reload
sudo systemctl enable midi-recorder.service
sudo systemctl start midi-recorder.service
```

To view status you can run: 

```bash
sudo systemctl status midi-recorder.service
```

To view logs you can run:

```bash
journalctl -u midi-recorder.service -f
```

To stop the daemon you can run:

```bash
sudo systemctl stop midi-recorder.service
```
