# Continuo

Continuo is an automated piano practice tracking system that records, processes, and visualizes practice sessions using MIDI data.

The project has two main goals:
1. Build a useful personal tool for tracking and analyzing piano practice
2. Serve as a learning and experimentation platform for modern backend systems and cloud infrastructure (AWS, async processing, scalability)

---

## System Overview

Continuo automatically detects when a piano practice session starts and ends, records the MIDI data, processes it asynchronously, and exposes structured statistics through a web interface.

At a high level:
- Practice sessions are captured automatically (no manual input)
- MIDI files are processed asynchronously
- Extracted features are stored in a database
- A backend API exposes the data
- A frontend visualizes practice history and statistics

---

## Architecture

Raspberry Pi (MIDI listener)
→ Amazon S3 (raw MIDI storage)
→ AWS Lambda (ingestion trigger)
→ Amazon SQS (job queue)
→ AWS Fargate (feature extraction worker)
→ PostgreSQL (Neon)
→ FastAPI backend
→ Vue frontend


---

## Components

### Raspberry Pi
- Continuously listens to a connected MIDI keyboard
- Automatically starts recording when playing begins
- Stops recording after a period of silence
- Uploads completed MIDI files to S3

### AWS Ingestion Pipeline
- **S3** stores raw MIDI files
- **Lambda** is triggered on new uploads
- **SQS** decouples ingestion from processing
- **Fargate** runs stateless workers that extract features from MIDI files

### Backend API
- Built with **FastAPI**
- Reads processed data from PostgreSQL (Neon)
- Exposes REST endpoints for sessions, statistics, and MIDI downloads

### Frontend
- Built with **Vue**
- Displays practice sessions, trends, and statistics
- Communicates exclusively through the backend API

---

## Design Principles

- **Asynchronous processing** — ingestion and processing are decoupled
- **Scalability** — workers scale independently via SQS + Fargate
- **Separation of concerns** — capture, processing, storage, and visualization are isolated
- **Infrastructure as learning** — AWS managed services are used intentionally to explore real-world architectures

---

## Project Vision

While Continuo currently focuses on tracking and visualizing piano practice through MIDI feature extraction, the long-term vision is to evolve it into a flexible experimentation platform for intelligent MIDI processing.

Future directions may include:
- Machine learning–based analysis of practice habits
- Expressive performance modeling
- Pattern discovery and similarity search across sessions
- Generative or assistive tools for practice and composition
- Training and evaluating custom models on symbolic music data

Continuo is intentionally designed with asynchronous processing and modular components to support future experimentation with machine learning and artificial intelligence workflows.

This project is as much a learning environment as it is an end product.
Architectural decisions may evolve as new experiments and research are introduced.

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

