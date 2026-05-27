#!/bin/bash
# init-wiki.sh — Initialize a wiki vault for codebase analysis
# Usage: bash init-wiki.sh <project-path> [--name <wiki-name>]

set -e

# Parse arguments
PROJECT_PATH=""
WIKI_NAME=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)
            WIKI_NAME="$2"
            shift 2
            ;;
        *)
            PROJECT_PATH="$1"
            shift
            ;;
    esac
done

if [ -z "$PROJECT_PATH" ]; then
    echo "Usage: bash init-wiki.sh <project-path> [--name <wiki-name>]"
    echo "  project-path: Path to the source code project to analyze"
    echo "  --name: Optional wiki directory name (default: <project-dir>-Wiki)"
    exit 1
fi

# Resolve absolute path
PROJECT_PATH=$(cd "$PROJECT_PATH" 2>/dev/null && pwd || echo "$PROJECT_PATH")

if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project directory does not exist: $PROJECT_PATH"
    exit 1
fi

# Derive wiki name from project directory
if [ -z "$WIKI_NAME" ]; then
    PROJECT_DIR=$(basename "$PROJECT_PATH")
    WIKI_NAME="${PROJECT_DIR}-Wiki"
fi

# Get the directory where this script lives (skill root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="$SKILL_ROOT/assets"

# Create wiki directory structure
echo "Creating wiki: $WIKI_NAME"
mkdir -p "$WIKI_NAME"
mkdir -p "$WIKI_NAME/entities"
mkdir -p "$WIKI_NAME/concepts"
mkdir -p "$WIKI_NAME/changelog"
mkdir -p "$WIKI_NAME/_archive"
mkdir -p "$WIKI_NAME/.cache"

# Copy template files
DATE=$(date +%Y-%m-%d)

# Generate SCHEMA.md
if [ -f "$ASSETS_DIR/schema-template.md" ]; then
    sed -e "s/PROJECT_NAME/$WIKI_NAME/g" \
        -e "s/YYYY-MM-DD/$DATE/g" \
        "$ASSETS_DIR/schema-template.md" > "$WIKI_NAME/SCHEMA.md"
    echo "  Created SCHEMA.md"
fi

# Generate index.md
if [ -f "$ASSETS_DIR/index-template.md" ]; then
    sed -e "s/YYYY-MM-DD/$DATE/g" \
        "$ASSETS_DIR/index-template.md" > "$WIKI_NAME/index.md"
    echo "  Created index.md"
fi

# Generate README.md
if [ -f "$ASSETS_DIR/readme-template.md" ]; then
    sed -e "s/PROJECT_NAME/$WIKI_NAME/g" \
        -e "s/YYYY-MM-DD/$DATE/g" \
        "$ASSETS_DIR/readme-template.md" > "$WIKI_NAME/README.md"
    echo "  Created README.md"
fi

# Generate log.md
if [ -f "$ASSETS_DIR/log-template.md" ]; then
    sed -e "s/PROJECT_NAME/$WIKI_NAME/g" \
        -e "s/YYYY-MM-DD/$DATE/g" \
        -e "s|\[源码路径\]|$PROJECT_PATH|g" \
        "$ASSETS_DIR/log-template.md" > "$WIKI_NAME/log.md"
    echo "  Created log.md"
fi

# Generate purpose.md
if [ -f "$ASSETS_DIR/purpose-template.md" ]; then
    sed -e "s/PROJECT_NAME/$WIKI_NAME/g" \
        -e "s|YYYY-MM-DD|$DATE|g" \
        -e "s|\[源码仓库路径\]|$PROJECT_PATH|g" \
        "$ASSETS_DIR/purpose-template.md" > "$WIKI_NAME/purpose.md"
    echo "  Created purpose.md"
fi

# Create .gitignore
cat > "$WIKI_NAME/.gitignore" << 'EOF'
.cache/
*.tmp
EOF
echo "  Created .gitignore"

# Initialize git if not already a repo
if [ ! -d "$WIKI_NAME/.git" ]; then
    cd "$WIKI_NAME"
    git init
    cd - > /dev/null
    echo "  Initialized git repository"
fi

echo ""
echo "Wiki vault created: $WIKI_NAME/"
echo "Source project: $PROJECT_PATH"
echo ""
echo "Next steps:"
echo "  1. Use '/llm-wiki scan' to analyze the project structure"
echo "  2. Use '/llm-wiki analyze' to deep-dive into modules"
echo "  3. Use '/llm-wiki generate' to create wiki pages"
