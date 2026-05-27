#!/bin/bash

# Claude Code Bash Command Validator
# Validates Bash commands against forbidden patterns for security

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command from JSON
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# If no command found, allow it
if [ -z "$COMMAND" ]; then
  exit 0
fi

# Define forbidden patterns (security-sensitive paths and files)
FORBIDDEN_PATTERNS=(
  "node_modules"
  "frontend/node_modules"
  ".env"
  "__pycache__"
  ".terraform"
  "service-account-key.json"
  "*.pyc"
  "*.log"
  "venv/"
  ".venv/"
)

# Check against forbidden patterns
for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
  if [[ "$COMMAND" == *"$pattern"* ]]; then
    echo "Error: Access to '$pattern' is blocked by security policy" >&2
    exit 2  # Exit code 2 = blocking error
  fi
done

# Check for dangerous command patterns
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  ":(){ :|:& };:"
  "mkfs"
  "dd if="
  "> /dev/sd"
  "chmod -R 777 /"
  "curl | bash"
  "wget | bash"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if [[ "$COMMAND" == *"$pattern"* ]]; then
    echo "Error: Dangerous command pattern detected: '$pattern'" >&2
    exit 2
  fi
done

# Command is clean, allow it
exit 0
