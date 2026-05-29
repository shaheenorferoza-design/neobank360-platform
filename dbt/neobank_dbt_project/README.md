# Neobank360 Platform

## Overview

Neobank360 is an end-to-end modern data platform built to simulate real-time fraud monitoring for a digital banking environment.

The platform ingests streaming transaction events, processes them through a cloud-native analytics architecture, applies fraud detection logic, generates analyst-friendly explanations, and serves insights through operational and business dashboards.

The project demonstrates modern Data Engineering, Analytics Engineering, Streaming, Orchestration, BI, and CI/CD practices using Snowflake, dbt, Airflow, Kafka, Streamlit, Power BI, and GitHub Actions.

---

## Business Problem

Banks process thousands of transactions every minute. Detecting suspicious activity in near real-time is critical for preventing fraud and reducing financial risk.

This project simulates a fraud monitoring platform that:

* Ingests streaming banking events
* Detects high-velocity transaction patterns
* Tracks historical customer changes using SCD2
* Generates fraud alert explanations
* Delivers operational and executive dashboards
* Validates transformations through automated testing and CI

---

## Architecture

Refer to the architecture diagram included in this repository.

### High-Level Flow

Transaction Events
→ Kafka Producer
→ Redpanda / Kafka Topic
→ Kafka Consumer
→ Snowflake RAW Layer
→ Snowflake Streams (CDC)
→ dbt Staging Models
→ dbt Facts & Dimensions
→ dbt SCD2 Snapshots
→ Fraud Detection Mart
→ Fraud Explanation Layer
→ Streamlit Dashboard
→ Power BI Dashboard

---

## Technology Stack

### Data Ingestion & Streaming

* Python
* Kafka
* Redpanda

### Data Warehouse

* Snowflake

### Transformation Layer

* dbt Core
* Incremental Models
* Snapshots (SCD Type 2)
* Data Quality Tests

### Orchestration

* Apache Airflow

### Analytics & Visualization

* Streamlit
* Power BI

### DevOps

* Git
* GitHub
* GitHub Actions

### AI / GenAI

* Fraud Explanation Layer
* GenAI-ready architecture for future LLM integration

---

## Key Features

### Real-Time Event Streaming

Transaction events are continuously generated and published to Kafka topics.

### Snowflake CDC Processing

Snowflake Streams capture new transaction events and support incremental processing.

### Incremental dbt Models

Only newly arrived records are processed, improving efficiency and scalability.

### Fraud Detection

High-velocity and burst transaction patterns are identified using business rules.

### SCD Type 2 Tracking

Customer history is preserved using dbt snapshots.

### Fraud Explanation Layer

Fraud alerts are converted into analyst-friendly natural language explanations.

### Automated Orchestration

Airflow coordinates transformation execution and validation workflows.

### Automated Quality Checks

dbt tests validate data quality before downstream consumption.

### Continuous Integration

GitHub Actions automatically validates dbt changes on every code push.

---

## Project Structure

```text
neobank360-platform/

├── streaming/
│   ├── producer/
│   └── consumer/
│
├── dbt/
│   └── transformations/
│
├── airflow/
│   └── dags/
│
├── dashboard/
│   └── streamlit/
│
├── powerbi/
│
├── snapshots/
│
├── tests/
│
└── .github/
    └── workflows/
```

---

## Dashboards

### Operational Dashboard

Built using Streamlit for near real-time monitoring.

### Executive Dashboard

Built using Power BI for fraud analytics and business reporting.

Includes:

* Total Fraud Alerts
* High Risk Alerts
* Fraud Distribution
* Fraud by Customer
* Fraud Trend Analysis
* Suspicious Transaction Investigation

---

## CI/CD

GitHub Actions automatically performs:

* dbt validation
* dbt parsing
* dbt testing

on every push to the repository.

---

## Future Enhancements

* LLM-powered fraud explanations
* Agentic AI fraud analyst assistant
* Customer risk scoring models
* Kubernetes deployment
* Cloud-native data lake integration
* Real-time alerting and notifications

---

## Author

Shaheen Feroza

Data Engineer | Snowflake | dbt | Airflow | Kafka | Analytics Engineering
