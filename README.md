## System Overview

Continuo is a 

## Architecture

Raspberry Pi
  → S3
    → Lambda
      → SQS
        → Fargate (feature extraction)
          → Postgres (Neon)
            → FastAPI
              → Vue frontend
