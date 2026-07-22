---
name: daily-pig
description: "Use when the user asks for 今日小猪 / 随机小猪 / 找猪, daily pig fortune, or PigHub pig images. Run the zero-dep CLI to draw a sticky daily pig from PigHub (once per day per user; --local for classic 62-pig roster), random/search PigHub art, and return image via MEDIA: path or markdown URL."
version: 1.2.0
author: daily-pig contributors (ported from huannai_plugin_rollpig)
license: MIT
platforms: [linux, macos, windows]
metadata:
  openclaw:
    emoji: "🐖"
    tags: [daily-pig, pig, fortune, leisure, fun, pighub, skill]
    category: leisure
    source: https://github.com/SonderXiaoming/huannai_plugin_rollpig
---

# 今日小猪 (Daily Pig)

把 [huannai_plugin_rollpig](https://github.com/SonderXiaoming/huannai_plugin_rollpig)（「今天是什么小猪」）做成 **agent 无关** 的 CLI skill。  
Claude Code / Codex / OpenCode / Pi / Cursor / Hermes 等：只要能跑 shell，就能用。

- **今日小猪（默认）**：从 **PigHub** 图库抽一张；同一用户当天固定；缓存空时自动 refresh
- **今日小猪 --local**：可选，本地 62 种（带 description/analysis）
- **随机小猪**：PigHub 盲抽（不占今日坑位）
- **找猪**：按关键词搜 PigHub 标题（最多 8 张）

## When to Use

- 用户说：今日小猪 / 今天什么猪 / 抽猪 / daily pig → **默认 hub**
- 用户说：随机小猪 / 找猪 xxx / PigHub
- 用户要本地图鉴或刷新 PigHub 目录

不要用手写 `random` 代替脚本（会破坏每日固定语义）。

## Prerequisites

- Python 3.10+（仅标准库）
- 网络：默认 `today` / `random` / `find` 走 PigHub
- 状态目录：`~/.daily-pig/`（可用 `DAILY_PIG_HOME` 覆盖）

## How to Run

**永远用 shell 跑脚本，不要手写抽签。**

先定位脚本（安装位置因 agent 而异）：

```bash
# 若已 clone 本仓库：
SCRIPT="/path/to/daily-pig/skills/daily-pig/scripts/daily_pig.py"

# 常见 skill 目录示例（按你实际安装改）：
# SCRIPT="$HOME/.agents/skills/daily-pig/scripts/daily_pig.py"
# SCRIPT="$HOME/.codex/skills/daily-pig/scripts/daily_pig.py"
# SCRIPT="$HOME/.claude/skills/daily-pig/scripts/daily_pig.py"
# SCRIPT="$HOME/.hermes/skills/leisure/daily-pig/scripts/daily_pig.py"
```

```bash
python3 "$SCRIPT" today --user "<stable-user-id>"
python3 "$SCRIPT" today --user "<stable-user-id>" --local
python3 "$SCRIPT" random
python3 "$SCRIPT" find "关键词" --limit 8
python3 "$SCRIPT" refresh
python3 "$SCRIPT" list
python3 "$SCRIPT" show pig
```

### 用户 ID

- 聊天平台：用稳定 uid（如 Telegram 数字 id）
- 环境变量：`DAILY_PIG_USER`（可省 `--user`）
- 默认：`local`

同一 `--user` + 同一 source（hub/local）同一天 → `is_repeat: true`。

## Agent 交付协议

1. 跑子命令  
2. 读 stdout：人类文案 + `MEDIA:/abs/path`（或 markdown 图链）+ `<!--DAILY_PIG_JSON-->` JSON  
3. 回复用户时：
   - 可俏皮复述，**不要改** title/name/description/analysis 事实  
   - **保留** `MEDIA:` 行或把图片附件发出去  
   - 不要把整段 JSON 甩给用户  
4. `ok: false` 时解释错误（先 refresh / 用 `--local`），不要编造猪  

### Hub 模板

```text
🐽 今日你是：{title}
来自 PigHub 的今日之猪～

MEDIA:{image_path}
```

### Local 模板

```text
🐽 今日你是：{name}
{description}
分析：{analysis}

MEDIA:{image_path}
```

## Command Map

| 用户说法 | 命令 |
|---------|------|
| 今日小猪 | `today --user …` |
| 今日小猪（本地） | `today --user … --local` |
| 随机小猪 | `random` |
| 找猪 丘吉尔 | `find 丘吉尔` |
| 刷新小猪 | `refresh` |
| 小猪图鉴 | `list` |
| 看看野猪 | `show wild-boar` |

## Data Layout

```text
skills/daily-pig/                 # skill 本体（可放在任意 agent skills 目录）
├── SKILL.md
├── scripts/daily_pig.py
└── resource/
    ├── pig.json
    ├── pig_hub.json
    └── image/{id}.png

~/.daily-pig/                     # 运行时状态（或 $DAILY_PIG_HOME）
├── today.json
└── hub-images/
```

## PigHub

- API: `https://pighub.top/api/all-images`
- 图: `https://pighub.top/images/{filename}`（目录里 `/data/` 是逻辑路径）
- 缓存空时 `today` 会自动 refresh 一次

## Common Pitfalls

1. 手写 random → 破坏每日固定  
2. `--user` 不稳定 → 一天多猪  
3. 丢掉图片路径/MEDIA → 只有字没有猪  
4. 用户没要求时误用 `--local`  
5. 把 hub 缓存写进 skill 的 `resource/image`  
6. 把 JSON trailer 贴给用户  

## Verification

- [ ] `today --user t1` → `source: hub` + 图  
- [ ] 连抽两次 → `is_repeat: true`  
- [ ] `today --local` 有 analysis  
- [ ] `list` ≈ 62 头  

## Credits

- `SonderXiaoming/huannai_plugin_rollpig`
- `Bearlele/nonebot-plugin-rollpig`
- `pighub.top`
