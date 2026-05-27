#!/bin/bash
# Temporary File Cleanup Script
# Removes temporary/pollution files from specified directory

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default to current directory if no argument provided
TARGET_DIR="${1:-.}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo -e "${BLUE}=== Fireworks Tech Graph - Cleanup Script ===${NC}"
echo "Target directory: $TARGET_DIR"
echo "Timestamp: $TIMESTAMP"
echo ""

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Directory not found: $TARGET_DIR${NC}"
    exit 1
fi

# Patterns to clean up
TEMP_PATTERNS=(
    "*_test.svg"
    "*_backup.svg"
    "*_temp.svg"
    "*~"
    "*.tmp"
    "*.bak"
    ".#*"
    "#*#"
)

# Count files before cleanup
TOTAL_BEFORE=$(find "$TARGET_DIR" -maxdepth 1 -type f | wc -l | tr -d ' ')

# Files to remove
FILES_TO_REMOVE=()

# Scan for temporary files
for pattern in "${TEMP_PATTERNS[@]}"; do
    while IFS= read -r -d '' file; do
        FILES_TO_REMOVE+=("$file")
    done < <(find "$TARGET_DIR" -maxdepth 1 -type f -name "$pattern" -print0 2>/dev/null || true)
done

# Check for old test output directories (older than 7 days)
OLD_OUTPUT_DIRS=$(find "$TARGET_DIR" -type d -name "test-output-*" -mtime +7 2>/dev/null || true)

if [ -n "$OLD_OUTPUT_DIRS" ]; then
    while IFS= read -r dir; do
        if [ -d "$dir" ]; then
            FILES_TO_REMOVE+=("$dir")
        fi
    done <<< "$OLD_OUTPUT_DIRS"
fi

# Summary
echo -e "${BLUE}Scan Results:${NC}"
echo "Total files before: $TOTAL_BEFORE"
echo "Temporary files found: ${#FILES_TO_REMOVE[@]}"
echo ""

if [ "${#FILES_TO_REMOVE[@]}" -eq 0 ]; then
    echo -e "${GREEN}✓ No temporary files to clean${NC}"
    exit 0
fi

# Show what will be removed
echo -e "${YELLOW}Files to be removed:${NC}"
for file in "${FILES_TO_REMOVE[@]}"; do
    echo "  - $(basename "$file")"
done
echo ""

# Confirm removal
if [ "${#FILES_TO_REMOVE[@]}" -gt 10 ]; then
    echo -e "${YELLOW}Warning: ${#FILES_TO_REMOVE[@]} files will be removed${NC}"
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cleanup cancelled"
        exit 0
    fi
fi

# Remove files
REMOVED=0
FAILED=0

for file in "${FILES_TO_REMOVE[@]}"; do
    if rm -rf "$file" 2>/dev/null; then
        REMOVED=$((REMOVED + 1))
        echo -e "${GREEN}✓ Removed:${NC} $(basename "$file")"
    else
        FAILED=$((FAILED + 1))
        echo -e "${RED}✗ Failed to remove:${NC} $(basename "$file")"
    fi
done

# Count files after cleanup
TOTAL_AFTER=$(find "$TARGET_DIR" -maxdepth 1 -type f | wc -l | tr -d ' ')

# Summary
echo ""
echo "========================================"
echo -e "${BLUE}Cleanup Summary${NC}"
echo "========================================"
echo "Files removed: $REMOVED"
echo "Failed removals: $FAILED"
echo "Files before: $TOTAL_BEFORE"
echo "Files after: $TOTAL_AFTER"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✓ Cleanup completed successfully${NC}"
    exit 0
else
    echo -e "\n${YELLOW}⚠ Some files could not be removed${NC}"
    exit 1
fi
