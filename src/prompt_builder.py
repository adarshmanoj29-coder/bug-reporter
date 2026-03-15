def build_prompt(bug_description: str) -> str:
    """
    Takes a raw bug description from the user and builds
    a structured prompt for the LLM to generate a formal bug report.
    """
    prompt = f"""
You are a senior QA engineer. A developer has given you the following 
raw bug description:

"{bug_description}"

Your task is to generate a formal, structured bug report in JSON format 
with exactly these fields:

{{
  "title": "A short, clear bug title (max 10 words)",
  "severity": "One of: Critical / High / Medium / Low",
  "environment": "Where this likely occurs e.g. Browser, Mobile, Backend API",
  "steps_to_reproduce": ["Step 1", "Step 2", "Step 3"],
  "expected_behavior": "What should happen",
  "actual_behavior": "What actually happens",
  "suggested_test_cases": ["Test case 1", "Test case 2", "Test case 3"]
}}

Return only valid JSON. No explanation, no markdown, no code blocks.
Just the raw JSON object.
"""
    return prompt