#!/usr/bin/env python3
"""
Baseline test: Measure how long Claude remembers the 'commit after every change' directive.

Test Design:
- Directive given at start: "Commit and push after every file change"
- Signal at end of response: ✓ (remembered) or ✗ (forgot)
- Make 15 sequential file changes
- Track which change number Claude first forgets

Run this test multiple times to establish a baseline pattern.
"""

import json
from datetime import datetime

# Test metadata
TEST_RUN = {
    "test_name": "baseline_commit_remembering",
    "timestamp": datetime.now().isoformat(),
    "description": "Measure how many file changes before forgetting commit directive",
    "total_changes": 15,
    "changes": []
}

# Phase 1 will record results here
RESULTS_FILE = "/ssd-pool/home-ext/pat/Projects/AlgoTrading/claudeTrader/tests/baseline_results.json"

def log_change(change_num, committed=True, notes=""):
    """Log a single file change and whether commit was done."""
    TEST_RUN["changes"].append({
        "change_num": change_num,
        "committed": committed,
        "notes": notes
    })

    # Find first failure
    failures = [c for c in TEST_RUN["changes"] if not c["committed"]]
    if failures:
        TEST_RUN["first_failure_at_change"] = failures[0]["change_num"]

    return TEST_RUN

def save_results():
    """Save test results to JSON."""
    with open(RESULTS_FILE, "w") as f:
        json.dump(TEST_RUN, f, indent=2)

if __name__ == "__main__":
    print("Baseline test initialized.")
    print(f"Results will be saved to: {RESULTS_FILE}")
    print(f"\nTest will track {TEST_RUN['total_changes']} sequential file changes.")
    print("Signal format: ✓ (committed) or ✗ (forgot)")
