# Bug Reporter - AI Powered QA Tool

A command-line tool that converts plain English bug descriptions into 
structured, formal bug reports using AI.

## What it does

- Takes a raw bug description as input
- Uses an LLM to generate a structured bug report with severity, 
  steps to reproduce, expected vs actual behavior, and suggested test cases
- Saves reports as JSON files
- Includes a full pytest test suite with 13 tests

## Tech Stack

- Python 3.11
- Groq API (llama-3.3-70b-versatile)
- pytest
- python-dotenv

## Project Structure
```
bug-reporter/
├── src/
│   ├── reporter.py        # Core logic and CLI
│   └── prompt_builder.py  # Prompt engineering
├── tests/
│   └── test_reporter.py   # 13 pytest tests
├── output/                # Generated reports saved here
└── README.md
```

## How to run

1. Clone the repo
2. Install dependencies: `pip install groq python-dotenv pytest`
3. Create a `.env` file with your Groq API key: `GROQ_API_KEY=your_key`
4. Run: `python src/reporter.py`

## How to run tests
```
pytest tests/test_reporter.py -v
```

## Example output

Input:
> The login button on the mobile app does nothing when clicked after 
entering valid credentials on iOS 17

Output:
```json
{
  "title": "Login Button Fails on iOS 17",
  "severity": "High",
  "environment": "Mobile App on iOS 17",
  "steps_to_reproduce": [...],
  "expected_behavior": "User should be logged in successfully",
  "actual_behavior": "Login button click has no effect",
  "suggested_test_cases": [...]
}
