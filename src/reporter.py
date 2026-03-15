import os
import json
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
from prompt_builder import build_prompt
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_bug_report(bug_description: str) -> dict:
    """
    Takes a plain text bug description and returns
    a structured bug report as a Python dictionary.
    """
    prompt = build_prompt(bug_description)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        bug_report = json.loads(raw_output)
    except json.JSONDecodeError:
        bug_report = {
            "error": "Failed to parse response as JSON",
            "raw_output": raw_output
        }

    return bug_report


def save_report(bug_report: dict, filename: str = "bug_report.json", output_dir: Path = None):
    """
    Saves the bug report dictionary to a JSON file in the output folder.
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "output"
    
    output_path = output_dir / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(bug_report, f, indent=2)
    print(f"Report saved to {output_path}")


def main():
    print("=== Bug Reporter - AI Powered QA Tool ===\n")
    bug_description = input("Describe the bug in plain English:\n> ")

    print("\nGenerating structured bug report...\n")
    report = generate_bug_report(bug_description)

    print(json.dumps(report, indent=2))

    save_choice = input("\nSave this report to file? (y/n): ")
    if save_choice.lower() == "y":
        save_report(report)


if __name__ == "__main__":
    main()
