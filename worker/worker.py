import os, json, boto3, pretty_midi, time
from sqlalchemy import create_engine, text

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
engine = create_engine(os.environ['DATABASE_URL'])
QUEUE_URL = os.environ['SQS_QUEUE_URL']

while True:
    response = sqs.receive_message(QueueUrl=QUEUE_URL, WaitTimeSeconds=20)

    if 'Messages' in response:
        for msg in response['Messages']:
            body = json.loads(msg['Body'])
            bucket, key = body['bucket'], body['key']

            local_file = "/tmp/processing.mid"
            s3.download_file(bucket, key, local_file)

            midi_data = pretty_midi.PrettyMIDI(local_file)
            ai_results = {"duration": float(midi_data.get_end_time()), "status": "analyzed"}

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
                        "meta": json.dumps(ai_results)
                    }
                )
                conn.commit()

            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])
            print(f"Finished processing {key}")