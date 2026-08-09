# Continuo

Continuo is an automated piano practice tracking system that records, processes, and
visualizes piano practice sessions based on the midi data generated from a digital piano.

The project has three main goals:
1. Build a useful personal tool for tracking and analyzing piano practice
2. Serve as a personal learning project, this is the first time I'm using AWS
3. Build my own MIDI dataset that I can use for AI experiments

---

## Architecture

Raspberry Pi
→ Amazon S3
→ AWS Lambda
→ Amazon SQS
→ AWS Fargate
→ PostgreSQL
→ FastAPI backend
→ Vue frontend

The AWS resources are provisioned by hand in the console. There is no
infrastructure-as-code in this repository, so the diagram above describes a deployment
that exists but is not reproducible from a `terraform apply`. Bringing it under IaC is on
the list.

---

## Components

### Raspberry Pi

`pi-agent/auto-recorder.py`. Listens to a MIDI input port with `mido`, buffers incoming
messages, and closes a session after a 15-second silence threshold. Saves the segment as
a `.mid` file and uploads it to S3 with `boto3`. Configured through environment variables
(`PORT_NAME`, `BUCKET_NAME`, AWS credentials, region).

### AWS pipeline

- **S3** stores raw MIDI files
- **Lambda** is triggered on new uploads
- **SQS** decouples ingestion from processing
- **Fargate** runs stateless workers that extract features from MIDI files

The Lambda function is configured in the AWS console and its source is not version
controlled here. The worker is: `worker/worker.py` long-polls SQS, downloads the
referenced object from S3, parses it with `pretty_midi`, and inserts duration and note
count into a `practice_sessions` table over SQLAlchemy. `worker/Dockerfile` is the image
that runs on Fargate.

### Backend API

`backend-api/`. FastAPI over the same PostgreSQL table. Endpoints for listing sessions,
aggregate statistics, and streaming a stored MIDI file back out of S3.

### Frontend

Built with Vue, displays practice sessions and analytics, talks to the backend API. Not
part of this repository yet.

---

## Project Vision

While Continuo currently focuses on tracking and visualizing piano practice, the
long-term vision is to evolve it into an experimentation platform for ML models to
analyse MIDI practice data.

Some long-term goals:
- Machine learning–based analysis of practice habits
- Pattern discovery and similarity search across sessions
- Assistive tools for practice

---

## Project Status

Continuo is under active development.

Current focus areas:
- Committing the frontend and the Lambda source
- Putting the manually provisioned AWS resources under IaC
- Improving documentation

---

## License

This project is licensed under the Apache License 2.0.
See the [LICENSE](LICENSE) file for details.
