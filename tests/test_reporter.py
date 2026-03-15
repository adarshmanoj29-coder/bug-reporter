import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from prompt_builder import build_prompt
from reporter import generate_bug_report, save_report


# ── Prompt Builder Tests ──────────────────────────────────────────────────────

def test_prompt_contains_bug_description():
    """Prompt must include the original bug text."""
    description = "Button does not work on mobile"
    prompt = build_prompt(description)
    assert description in prompt

def test_prompt_requests_json_output():
    """Prompt must instruct the LLM to return JSON."""
    prompt = build_prompt("some bug")
    assert "JSON" in prompt

def test_prompt_contains_required_fields():
    """Prompt must ask for all required bug report fields."""
    prompt = build_prompt("some bug")
    required_fields = [
        "title",
        "severity",
        "steps_to_reproduce",
        "expected_behavior",
        "actual_behavior",
        "suggested_test_cases"
    ]
    for field in required_fields:
        assert field in prompt, f"Missing field in prompt: {field}"

def test_prompt_is_not_empty():
    """Prompt must not be empty or whitespace only."""
    prompt = build_prompt("crash on startup")
    assert prompt.strip() != ""

def test_prompt_with_empty_description():
    """Prompt builder should still return a string even with empty input."""
    prompt = build_prompt("")
    assert isinstance(prompt, str)


# ── Bug Report Structure Tests ────────────────────────────────────────────────

def test_report_has_required_keys():
    """Generated report must contain all required keys."""
    report = generate_bug_report("App crashes when uploading a file larger than 10MB")
    required_keys = [
        "title",
        "severity",
        "environment",
        "steps_to_reproduce",
        "expected_behavior",
        "actual_behavior",
        "suggested_test_cases"
    ]
    for key in required_keys:
        assert key in report, f"Missing key in report: {key}"

def test_report_severity_is_valid():
    """Severity must be one of the four accepted values."""
    report = generate_bug_report("App crashes when uploading a file larger than 10MB")
    valid_severities = ["Critical", "High", "Medium", "Low"]
    assert report["severity"] in valid_severities

def test_report_steps_is_a_list():
    """Steps to reproduce must be returned as a list."""
    report = generate_bug_report("Search bar returns no results for valid queries")
    assert isinstance(report["steps_to_reproduce"], list)

def test_report_steps_not_empty():
    """Steps to reproduce must contain at least one step."""
    report = generate_bug_report("Search bar returns no results for valid queries")
    assert len(report["steps_to_reproduce"]) > 0

def test_report_suggested_test_cases_is_list():
    """Suggested test cases must be returned as a list."""
    report = generate_bug_report("Dark mode text is unreadable on settings screen")
    assert isinstance(report["suggested_test_cases"], list)

def test_report_title_is_string():
    """Title must be a non-empty string."""
    report = generate_bug_report("Dark mode text is unreadable on settings screen")
    assert isinstance(report["title"], str)
    assert len(report["title"]) > 0


# ── Save Report Tests ─────────────────────────────────────────────────────────

def test_save_report_creates_file(tmp_path):
    """save_report must create a JSON file in the output directory."""
    sample_report = {
        "title": "Test Bug",
        "severity": "Low",
        "environment": "Web",
        "steps_to_reproduce": ["Step 1"],
        "expected_behavior": "Works",
        "actual_behavior": "Fails",
        "suggested_test_cases": ["Test A"]
    }

    save_report(sample_report, filename="test_output.json", output_dir=tmp_path)
    saved_file = tmp_path / "test_output.json"
    assert saved_file.exists()

def test_save_report_content_is_valid_json(tmp_path):
    """Saved file must contain valid parseable JSON."""
    sample_report = {"title": "Test", "severity": "Medium"}
    save_report(sample_report, filename="test_output.json", output_dir=tmp_path)

    saved_file = tmp_path / "test_output.json"
    with open(saved_file, "r") as f:
        content = json.load(f)
    assert content["title"] == "Test"
