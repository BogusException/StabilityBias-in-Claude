#!/bin/bash
# Solution 3: Skill Wrapper
# Concept: Wrap file writes with auto-commit
# User would invoke: /write-and-commit instead of Write tool directly
# Pro: Enforces at tool level
# Con: Requires user to use different tool

echo "Skill wrapper concept:"
echo "  /write-and-commit <path> <content>"
echo "  Automatically:"
echo "    1. Write the file"
echo "    2. Git add"
echo "    3. Git commit"
echo "    4. Git push"
echo ""
echo "Evaluation:"
echo "  Pro: Enforces at the tool level, no forgetting possible"
echo "  Con: Requires discipline to use /write-and-commit instead of Write"
echo "  Con: Bypasses skill if user forgets to use it"
echo "  Estimated success rate: 70% (still requires remembering to use it)"
