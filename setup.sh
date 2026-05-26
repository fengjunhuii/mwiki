#!/usr/bin/env bash
# mwiki setup.sh — 将 Skills 链接到多个 Agent 的全局/项目 skills 目录
# 用法：bash setup.sh [vault-path]  或直接 bash setup.sh 进入交互模式
# 平台：Linux / macOS / Windows (Git Bash / MSYS2)

set -euo pipefail

CONFIG_DIR="$HOME/.obsidian-wiki"
CONFIG_FILE="$CONFIG_DIR/config"

# ─── 1. 确定 Vault 路径 ───────────────────────────────────────────────
if [ $# -ge 1 ]; then
    VAULT_PATH="$1"
else
    echo "========================================"
    echo " mwiki 多 Agent 安装脚本"
    echo "========================================"
    echo ""
    echo "请输入 Obsidian Vault 路径（即 mwiki 项目根目录）"
    echo "留空使用当前目录: $(pwd)"
    read -rp "> " VAULT_PATH
    VAULT_PATH="${VAULT_PATH:-$(pwd)}"
    echo ""
fi

# 转为绝对路径
VAULT_PATH="$(cd "$VAULT_PATH" 2>/dev/null && pwd)" || {
    echo "错误：路径不存在或无法访问: $VAULT_PATH"
    exit 1
}

# ─── 2. 校验 Vault ────────────────────────────────────────────────────
SKILLS_SRC="$VAULT_PATH/.skills"

if [ ! -d "$SKILLS_SRC" ]; then
    echo "错误：未找到 .skills/ 目录: $SKILLS_SRC"
    echo "请确认路径指向已初始化的 mwiki Vault（运行 /wiki-setup 初始化）"
    exit 1
fi

echo "========================================"
echo " mwiki 多 Agent 安装脚本"
echo "========================================"
echo "Vault 路径: $VAULT_PATH"
echo "Skills 源:  $SKILLS_SRC"

# 检测平台
IS_WINDOWS=false
if [[ "$(uname -s)" == MINGW* ]] || [[ "$(uname -s)" == MSYS* ]] || [[ "$(uname -s)" == CYGWIN* ]]; then
    IS_WINDOWS=true
    echo "平台: Windows (将使用 Junction 链接)"
fi
echo ""

# ─── 3. 保存配置 ─────────────────────────────────────────────────────
mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_FILE" << CONF
VAULT_PATH=$VAULT_PATH
SKILLS_SRC=$SKILLS_SRC
CONF
echo "已保存配置到 $CONFIG_FILE"
echo ""

# ─── 4. Agent 定义（全局 vs 项目级）─────────────────────────────────
# 全局 Agent：skills 目录在 $HOME 下
declare -A GLOBAL_AGENTS=(
    ["claude-code"]="$HOME/.claude/skills"
    ["codex"]="$HOME/.codex/skills"
    ["gemini-cli"]="$HOME/.gemini/skills"
    ["hermes"]="$HOME/.hermes/skills"
    ["openclaw"]="$HOME/.openclaw/skills"
    ["aider"]="$HOME/.aider/skills"
    ["copilot"]="$HOME/.copilot/skills"
    ["zed"]="$HOME/.zed/skills"
    ["pearai"]="$HOME/.pearai/skills"
    ["devika"]="$HOME/.devika/skills"
)

# 项目级 Agent：skills 目录在 Vault 内
declare -A PROJECT_AGENTS=(
    ["cursor"]="$VAULT_PATH/.cursor/skills"
    ["cline"]="$VAULT_PATH/.cline/skills"
    ["continue"]="$VAULT_PATH/.continue/skills"
    ["windsurf"]="$VAULT_PATH/.windsurf/skills"
)

# ─── 5. 跨平台链接工具函数 ──────────────────────────────────────────

# 将 Unix 路径转为 Windows 路径（用于 cmd /c mklink）
to_win_path() {
    if command -v cygpath &>/dev/null; then
        cygpath -w "$1"
    else
        # 手动转换 /c/path -> C:\path
        local p="$1"
        if [[ "$p" =~ ^/([a-zA-Z])/ ]]; then
            p="${p:1:1}:\\${p:3}"
        fi
        echo "${p//\//\\}"
    fi
}

# 移除旧的链接（支持 symlink / junction / 目录副本）
remove_old_link() {
    local target="$1"

    if [ -L "$target" ]; then
        # Unix symlink
        rm -f "$target"
    elif [ -d "$target" ]; then
        if $IS_WINDOWS; then
            # Windows: 可能是 junction 或副本目录
            local win_path
            win_path="$(to_win_path "$target")"
            # 尝试 rmdir（junction 用 rmdir 移除，不会删除源内容）
            if cmd //c "rmdir \"${win_path}\"" 2>/dev/null; then
                return 0
            fi
            # 如果 rmdir 失败，可能是普通目录副本
            rm -rf "$target"
        else
            rm -rf "$target"
        fi
    fi
}

# 创建跨平台链接
create_link() {
    local src="$1"
    local dst="$2"  # 链接路径（目录名/mwiki）

    if ! $IS_WINDOWS; then
        # Unix: 标准 symlink
        ln -s "$src" "$dst" && return 0
    else
        # Windows: 优先 Junction，后备目录副本
        local win_src win_dst_parent win_dst_name
        win_src="$(to_win_path "$src")"
        win_dst_parent="$(to_win_path "$(dirname "$dst")")"
        win_dst_name="$(basename "$dst")"

        # 尝试 mklink /J（Junction）
        if cmd //c "mklink /J \"${win_dst_parent}\\${win_dst_name}\" \"${win_src}\"" 2>/dev/null; then
            return 0
        fi

        # Junction 失败，回退到目录副本
        if cp -r "$src" "$dst" 2>/dev/null; then
            return 0
        fi
    fi

    return 1
}

# ─── 6. 创建链接 ────────────────────────────────────────────────────
success=0
failed=0
skipped=0

create_symlink() {
    local agent="$1"
    local target_dir="$2"

    local link_name="$target_dir/mwiki"

    echo -n "  [$agent] $target_dir ... "

    # 创建目标目录
    if ! mkdir -p "$target_dir" 2>/dev/null; then
        echo "SKIP (无法创建目录)"
        echo "    原因：请检查权限或手动创建 $target_dir"
        skipped=$((skipped + 1))
        return
    fi

    # 移除旧链接
    remove_old_link "$link_name"

    # 创建新链接
    if create_link "$SKILLS_SRC" "$link_name"; then
        echo "OK"
        success=$((success + 1))
    else
        echo "FAIL"
        echo "    原因：无法创建链接 $link_name -> $SKILLS_SRC"
        echo "    建议：检查 $target_dir 的写权限，或尝试以管理员身份运行"
        failed=$((failed + 1))
    fi
}

echo "--- 全局 Agent（skills 在 HOME 目录）---"
for agent in $(echo "${!GLOBAL_AGENTS[@]}" | tr ' ' '\n' | sort); do
    create_symlink "$agent" "${GLOBAL_AGENTS[$agent]}"
done

echo ""
echo "--- 项目级 Agent（skills 在 Vault 目录内）---"
for agent in $(echo "${!PROJECT_AGENTS[@]}" | tr ' ' '\n' | sort); do
    create_symlink "$agent" "${PROJECT_AGENTS[$agent]}"
done

# ─── 7. 安装全局 wiki-update 命令 ──────────────────────────────────
echo ""
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
echo "已安装全局命令: $GLOBAL_BIN/wiki-update"

# 提示 PATH 配置
case ":$PATH:" in
    *":$GLOBAL_BIN:"*) ;;
    *)
        echo ""
        echo "提示：$GLOBAL_BIN 不在 PATH 中，建议添加："
        echo "  echo 'export PATH=\"$GLOBAL_BIN:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
        ;;
esac

# ─── 8. 输出摘要 ────────────────────────────────────────────────────
total=$(( ${#GLOBAL_AGENTS[@]} + ${#PROJECT_AGENTS[@]} ))

echo ""
echo "========================================"
echo " 安装完成"
echo "========================================"
echo "Vault: $VAULT_PATH"
echo "成功: $success | 失败: $failed | 跳过: $skipped"
echo "共支持 $total 种 Agent"
echo ""

if [ "$failed" -gt 0 ]; then
    echo "⚠ 有 $failed 个 Agent 安装失败，请检查上方错误信息"
    exit 1
fi

echo "所有 Agent 安装成功"
