import os, json, boto3, pretty_midi, time
from sqlalchemy import create_engine, text

# 1. Setup Connections
s3 = boto3.client('s3')
sqs = boto3.client('sqs')
engine = create_engine(os.environ['DATABASE_URL'])
QUEUE_URL = os.environ['SQS_QUEUE_URL']

print("Fargate Worker active. Waiting for SQS messages...")

while True:
    # 2. Long-poll SQS (Waits for a file to arrive)
    response = sqs.receive_message(QueueUrl=QUEUE_URL, WaitTimeSeconds=20)

    if 'Messages' in response:
        for msg in response['Messages']:
            body = json.loads(msg['Body'])
            bucket, key = body['bucket'], body['key']

            # 3. Download from S3 to temporary storage
            local_file = "/tmp/processing.mid"
            s3.download_file(bucket, key, local_file)

            # 4. RUN AI SEGMENTER LOGIC
            midi_data = pretty_midi.PrettyMIDI(local_file)
            # Example math:
            ai_results = {"duration": float(midi_data.get_end_time()), "status": "analyzed"}

            # 5. Update Neon Database
            # 5. Insert New Row into Neon Database
            with engine.connect() as conn:
                conn.execute(
                    text("""
                         INSERT INTO practice_sessions (s3_key, duration_seconds, note_count, ai_metadata)
                         VALUES (:k, :dur, :notes, :meta)
                         """),
                    {
                        "k": key,
                        "dur": float(midi_data.get_end_time()),
                        "notes": len(midi_data.instruments[0].notes) if midi_data.instruments else 0,
                        "meta": json.dumps(ai_results)  # SQLAlchemy handles the JSON stringing
                    }
                )
                conn.commit()

            # 6. Delete message from queue
            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])
            print(f"Finished processing {key}")