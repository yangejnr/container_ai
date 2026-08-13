# AI-Based Container Scanner

An edge-AI prototype for reading and validating ISO 6346 shipping-container identification codes using computer vision, OCR and standards-based check-digit verification.

## Project Vision

Container identification is a routine but important part of port, logistics and customs workflows. Manual reading and transcription can introduce delays and data-entry errors, particularly when operations depend on connectivity to central systems.

This project explores a lightweight edge-computing approach in which a camera image is processed locally, the detected container code is normalised, the ISO 6346 check digit is validated and the result is recorded locally for later review or integration.

## Processing Pipeline

```text
Container Image
      │
      ▼
 Image Pre-processing
      │
      ▼
 OCR Extraction
      │
      ▼
 Code Normalisation
      │
      ▼
 ISO 6346 Validation
      │
      ▼
 Local Result Logging
```

## Implemented Prototype Capabilities

- image processing with OpenCV
- OCR using EasyOCR
- ISO 6346 check-digit validation in Python
- local SQLite logging of scan results
- demonstration scripts for end-to-end scanning
- voice-triggered demonstration workflow
- Raspberry Pi as the intended edge-deployment target

## Why Edge Deployment?

A local processing pipeline can reduce dependence on continuous cloud connectivity and keeps the core image-to-validation workflow close to the inspection point. This repository is therefore structured as a proof of concept for edge deployment rather than as a cloud-only AI service.

## Technology

- Python
- OpenCV
- EasyOCR
- SQLite
- Raspberry Pi / edge computing
- speech-recognition experimentation

## Validation and Limitations

This repository demonstrates the technical pipeline, but it does **not** currently contain a reproducible benchmark dataset or automated evaluation suite sufficient to substantiate a production accuracy claim. Any historical accuracy figures should therefore be treated as preliminary project observations rather than independently reproducible performance results.

Before production use, the system would require:

- a labelled evaluation dataset
- repeatable OCR and validation benchmarks
- latency and failure-rate measurement
- automated tests
- configuration hardening
- authentication and access controls
- operational monitoring and log management
- integration with authorised enterprise systems

## Repository Structure

```text
container_ai/
├── src/                  # prototype implementation
├── executive_summary.md  # business/technical assessment
├── executive_summary.docx
└── README.md
```

## Status

**Functional research prototype / MVP.** It demonstrates container-code OCR, standards validation and local persistence, but it is not presented as a production inspection system.

## Author

**Yange Henry Terzugwe**  
MSc Robotics — University of Plymouth  
Software Developer • AI & Robotics Practitioner
