#!/bin/bash
# Auto-detect workflow type from context
# Outputs: WORKFLOW_TYPE=development|knowledge|mixed

PROJECT_ROOT="${CLAUDE_PROJECT_DIR}"
CONTEXT_FILE="${PROJECT_ROOT}/.claude/data/workflow-context.txt"

# Detect project type
PROJECT_TYPE="generic"
if [ -f "${PROJECT_ROOT}/package.json" ] || [ -f "${PROJECT_ROOT}/tsconfig.json" ]; then
    PROJECT_TYPE="node"
elif [ -f "${PROJECT_ROOT}/requirements.txt" ] || [ -f "${PROJECT_ROOT}/pyproject.toml" ]; then
    PROJECT_TYPE="python"
elif [ -f "${PROJECT_ROOT}/Cargo.toml" ]; then
    PROJECT_TYPE="rust"
elif [ -f "${PROJECT_ROOT}/go.mod" ]; then
    PROJECT_TYPE="go"
fi

# Detect recent task type from git
TASK_TYPE="unknown"
if git -C "${PROJECT_ROOT}" log -1 --pretty=%B 2>/dev/null | grep -qE "(feat|fix|refactor|test|build)"; then
    TASK_TYPE="development"
elif git -C "${PROJECT_ROOT}" log -1 --pretty=%B 2>/dev/null | grep -qE "(plan|design|brainstorm|research)"; then
    TASK_TYPE="knowledge"
fi

# Determine workflow type
WORKFLOW_TYPE="mixed"
if [ "${PROJECT_TYPE}" != "generic" ] && [ "${TASK_TYPE}" = "development" ]; then
    WORKFLOW_TYPE="development"
elif [ "${TASK_TYPE}" = "knowledge" ]; then
    WORKFLOW_TYPE="knowledge"
fi

# Write to context file
CONTEXT_DIR=$(dirname "$CONTEXT_FILE")
mkdir -p "$CONTEXT_DIR"
echo "WORKFLOW_TYPE=${WORKFLOW_TYPE}" > "${CONTEXT_FILE}"
echo "PROJECT_TYPE=${PROJECT_TYPE}" >> "${CONTEXT_FILE}"
echo "DETECTED_AT=$(date +%Y-%m-%dT%H:%M:%S)" >> "${CONTEXT_FILE}"
