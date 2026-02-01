# Continuo

Continuo is an automated piano practice tracking system that records, processes, and visualizes piano practice sessions based on the midi data generated from a digital piano.

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

---

## Components

### Raspberry Pi
- Continuously listens to a connected MIDI keyboard
- Automatically starts recording when playing begins
- Stops recording after a period of silence
- Uploads completed MIDI files to S3

### AWS Pipeline
- **S3** stores raw MIDI files
- **Lambda** is triggered on new uploads
- **SQS** decouples ingestion from processing
- **Fargate** runs stateless workers that extract features from MIDI files

### Backend API
- Built with FastAPI
- Reads processed data from PostgreSQL
- Exposes REST endpoints for sessions, statistics, and MIDI downloads

### Frontend
- Built with Vue
- Displays practice sessions and allows users to view analytics about them
- Communicates through the backend API

---

## Project Vision

While Continuo currently focuses on tracking and visualizing piano practice, the long-term vision is to evolve it into a experimentation platform for ML models to analyse MIDI practice data.

Some long-term goals:
- Machine learning–based analysis of practice habits
- Pattern discovery and similarity search across sessions
- Assistive tools for practice

---

## Project Status

Continuo is under active development.

Current focus areas:
- Cleaning up architecture and adding IaC
- Improving documentation
- Establishing a solid foundation before moving on to complex features

---

## License

This project is licensed under the Apache License 2.0.
See the [LICENSE](LICENSE) file for details.

