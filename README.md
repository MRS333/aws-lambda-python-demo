# AWS Lambda Python Project

## Overview
This is a simple serverless project built using AWS Lambda and Python. The Lambda function handles backend logic and can be tested locally using the provided development server script.

## Project Structure
- `lambda_function.py`: Main AWS Lambda function handler.
- `utils/`, `models/`: Modular Python code for organization and reuse.
- `tests/`: Unit tests for the Lambda function.
- `requirements.txt`: Lists Python dependencies.
- `local_dev_server.py`: Script for local testing of the Lambda function.

## Notes
There are some optional Node.js files included, but they are not required to run or deploy the Python-based Lambda function.

## Deployment
You can deploy this Lambda function by:
- Uploading a zip of the code via the AWS Console
- Using the AWS CLI or AWS SAM for more advanced workflows

## Getting Started
To test locally:

```bash
pip install -r requirements.txt
python local_dev_server.py
