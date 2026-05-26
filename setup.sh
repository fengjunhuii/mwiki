#!/usr/bin/env bash
# mwiki setup.sh — 将 Skills symlink 到多个 Agent 的全局 skills 目录
# 用法：bash setup.sh [vault-path]

set -euo pipefail

VAULT_PATH="${1:-$(pwd)}"
CONFIG_DIR="$HOME/.obsidian-wiki"
CONFIG_FILE="$CONFIG_DIR/config"
SKILLS_SRC="$VAULT_PATH/.skills"

# 支持的 Agent 及其 Skills 目录
declare -A AGENTS=(
    ["claude-code"]="$HOME/.claude/skills"
    ["cursor"]=".cursor/skills"
    ["codex"]="$HOME/.codex/skills"
    ["gemini-cli"]="$HOME/.gemini/skills"
    ["hermes"]="$HOME/.hermes/skills"
    ["openclaw"]="$HOME/.openclaw/skills"
    ["cline"]="$HOME/.cline/skills"
    ["aider"]="$HOME/.aider/skills"
    ["continue"]="$HOME/.continue/skills"
    ["copilot"]="$HOME/.copilot/skills"
    ["windsurf"]="$HOME/.windsurf/skills"
    ["zed"]="$HOME/.zed/skills"
    ["pearai"]="$HOME/.pearai/skills"
    ["devika"]="$HOME/.devika/skills"
)

echo "========================================"
echo " mwiki 多 Agent 安装脚本"
echo "========================================"
echo "Vault 路径: $VAULT_PATH"
echo ""

# 保存配置
mkdir -p "$CONFIG_DIR"
echo "VAULT_PATH=$VAULT_PATH" > "$CONFIG_FILE"
echo "已保存配置到 $CONFIG_FILE"
echo ""

# 确保 .skills 目录存在
mkdir -p "$SKILLS_SRC"

# 统计
success=0
failed=0
skipped=0

for agent in "${!AGENTS[@]}"; do
    target="${AGENTS[$agent]}"
    link_name="$target/mwiki"

    echo -n "[$agent] ... "

    # 创建目标目录（如果不存在）
    if ! mkdir -p "$target" 2>/dev/null; then
        echo "SKIP (无法创建目录: $target)"
        ((skipped++))
        continue
    fi

    # 移除旧的 symlink（如果存在）
    if [ -L "$link_name" ]; then
        rm -f "$link_name"
    fi

    # 创建 symlink
    if ln -s "$SKILLS_SRC" "$link_name" 2>/dev/null; then
        echo "OK -> $link_name"
        ((success++))
    else
        echo "FAIL (无法创建 symlink)"
        echo "  错误：请检查 $target 目录的写权限"
        ((failed++))
    fi
done

# 安装全局 wiki-update 命令
GLOBAL_BIN="$HOME/.local/bin"
mkdir -p "$GLOBAL_BIN"

cat > "$GLOBAL_BIN/wiki-update" << 'SCRIPT'
#!/usr/bin/env bash
# mwiki 全局 wiki-update 命令
# 从任何目录都能调用 wiki-update

CONFIG="$HOME/.obsidian-wiki/config"
if [ ! -f "$CONFIG" ]; then
    echo "错误：未找到 mwiki 配置，请先运行 setup.sh"
    exit 1
fi

source "$CONFIG"
cd "$VAULT_PATH"
echo "在 Vault 路径执行 wiki-update: $VAULT_PATH"
# 实际 wiki-update 逻辑由 Agent Skill 实现
SCRIPT

chmod +x "$GLOBAL_BIN/wiki-update"
echo ""
echo "已安装全局命令: $GLOBAL_BIN/wiki-update"

# 输出摘要
echo ""
echo "========================================"
echo " 安装完成"
echo "========================================"
echo "成功: $success | 失败: $failed | 跳过: $skipped"
echo "共支持 ${#AGENTS[@]} 种 Agent"
echo ""

if [ "$failed" -gt 0 ]; then
    echo "⚠ 有 $failed 个 Agent 安装失败，请检查上方错误信息"
    exit 1
fi

echo "所有 Agent 安装成功"
