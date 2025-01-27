# AI Research and Report Generation System

## System Overview
This system is designed to automatically generate comprehensive AI/ML use case reports for companies across different industries. It consists of a Flask-based API server that orchestrates three main agent components to research, analyze, and compile detailed reports.

---

## Architecture Components

### 1. **Main Application Server (`main.py`)**
The core server component built with Flask that handles HTTP requests and orchestrates the report generation process.

#### Key Features:
- REST API endpoints for report generation and retrieval
- Report storage and management
- Comprehensive logging system
- CORS support for cross-origin requests

#### Main Endpoints:
- **`POST /api/generate-report`**: Generates new reports
- **`GET /api/reports`**: Lists all generated reports
- **`GET /api/reports/<filename>`**: Retrieves specific reports

---

### 2. **Research Agent (`agent_researcher.py`)**
Handles company and industry research using external APIs to gather market intelligence.

#### Key Functions:
- Company and industry research using Google Search API (via Serper)
- Data cleaning and normalization
- Extraction of strategic focus areas
- Market trend analysis
- Structured data organization

---

### 3. **Use Case Generator (`agent_use_case_generator.py`)**
Generates AI/ML use cases using LLM capabilities via the Groq API.

#### Features:
- LLM-powered use case generation
- Structured output formatting
- Use case validation
- Fallback mechanisms
- Customizable focus areas:
  - Customer experience
  - Operational efficiency
  - Product innovation

---

### 4. **Resource Collector (`agent_resource_collector.py`)**
Aggregates relevant resources and implementation guidelines for each use case.

#### Resource Types:
- Kaggle datasets
- Hugging Face models
- Research papers
- Technical requirements
- Implementation guidelines

---

## Data Flow

### 1. **Request Initiation**
- Client submits company name and industry
- `ReportGenerator` instance is created

### 2. **Research Phase**
- Company and industry research is conducted
- Market analysis data is collected
- Strategic focus areas are identified

### 3. **Use Case Generation**
- Research data is processed by LLM
- Structured use cases are generated
- Cases are validated and formatted

### 4. **Resource Collection**
- Relevant resources are gathered for each use case
- Technical requirements are generated
- Implementation guidelines are created

### 5. **Report Compilation**
- All components are assembled into a structured report
- Report is saved with a timestamp
- Response is sent to the client

---

## Technical Implementation Details

### Error Handling
- Comprehensive error handling at each stage
- Detailed logging for debugging
- Fallback mechanisms for failed operations

### Data Validation
- Input validation for required fields
- Use case structure validation
- Resource availability checks

### Storage
- Reports stored in JSON format
- Organized by company name and timestamp
- Directory management for report storage

### API Integration
- Groq API for LLM capabilities
- Serper API for web research
- Hugging Face API for model search
- Kaggle integration for datasets

---

## Configuration Requirements

### Environment Variables:
- `GROQ_API_KEY`: For LLM access
- `SERPER_API_KEY`: For web research

## High Level System Architecture 
![Untitled diagram-2025-01-27-131758](https://github.com/user-attachments/assets/4fddf8ae-4576-4839-85e0-9e46aa3089ba)

---

## Component Flow
![Untitled diagram-2025-01-27-132257](https://github.com/user-attachments/assets/b38adc13-f54b-49a4-bc27-4cce7f13479a)

---
