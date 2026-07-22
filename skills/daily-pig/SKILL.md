---
name: daily-pig
description: "Use when the user asks for 今日小猪 / 随机小猪 / 找猪, daily pig fortune, or PigHub pig images. Draw a sticky daily pig from PigHub (once per day per user; --local for classic 62-pig roster), random/search PigHub art, and send the image via MEDIA:."
version: 1.1.0
author: Hermes Agent (ported from huannai_plugin_rollpig)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [daily-pig, pig, fortune, leisure, fun, pighub]
    category: leisure
    related_skills: [petdex]
    source: https://github.com/SonderXiaoming/huannai_plugin_rollpig
---

# 今日小猪 (Daily Pig)

把 [huannai_plugin_rollpig](https://github.com/SonderXiaoming/huannai_plugin_rollpig)（HoshinoBot「今天是什么小猪」）包装成 Hermes skill。

- **今日小猪（默认）**：从 **PigHub** 图库抽一张；同一用户当天结果固定，0 点换日重置；缓存空时自动 `refresh`
- **今日小猪 --local**：可选，走本地 62 种（带 description/analysis）经典池
- **随机小猪**：从 PigHub 缓存再随机一张（不写入今日缓存）
- **找猪**：按关键词搜索 PigHub 标题（最多 8 张）

## When to Use

- 用户说：今日小猪 / 今天什么猪 / 抽猪 / daily pig → **默认 hub**（不要加 `--local`，除非用户明确要本地/性格分析版）
- 用户说：随机小猪 / 找猪 xxx / PigHub
- 用户想看本地小猪图鉴、或刷新 PigHub 目录

不要用它做：宠物 mascot（→ `petdex`）、正经算命业务、改 Bot 源码。

## Prerequisites

- Python 3.10+（系统 `python3` 即可，无额外依赖）
- `today` 默认依赖 PigHub：`resource/pig_hub.json` + 网络（空缓存会自动 refresh）
- 本地后备：`resource/pig.json` + `resource/image/*.png`（62 种，仅 `--local` / `list` / `show`）
- 状态目录：`$HERMES_HOME/daily-pig/`（`today.json` + hub 图片缓存）

## How to Run

**永远用 `terminal` 跑脚本，不要手写抽签逻辑。**

```bash
SCRIPT="$HOME/.hermes/skills/leisure/daily-pig/scripts/daily_pig.py"
# profile 隔离时：
# SCRIPT="${HERMES_HOME:-$HOME/.hermes}/skills/leisure/daily-pig/scripts/daily_pig.py"

# 默认：PigHub 今日小猪
python3 "$SCRIPT" today --user "<stable-user-id>"
# 可选：经典本地 62 种
python3 "$SCRIPT" today --user "<stable-user-id>" --local
python3 "$SCRIPT" random
python3 "$SCRIPT" find "关键词" --limit 8
python3 "$SCRIPT" refresh
python3 "$SCRIPT" list
python3 "$SCRIPT" show pig
```

### 用户 ID 规则（今日小猪必须稳定）

- Telegram DM：用对方数字 user id（例如 `364882308`）
- 有 `HERMES_USER_ID` 环境变量时可不传 `--user`
- 缺省回落 `local`（本机 CLI 自用）

同一 `--user` + 同一 `source`（hub/local）同一天重复调用 → 返回同一只猪（`is_repeat: true`）。  
切换 hub ↔ local 会重置当日缓存。

## Agent 交付协议（Telegram / 消息平台）

1. 运行对应子命令。
2. 读 stdout：人类可读文案 + `MEDIA:/abs/path` 行 + `<!--DAILY_PIG_JSON-->` 后的 JSON。
3. **最终回复必须**：
   - 用中文俏皮口吻复述结果（可微调语气，**不要改** title / name / description / analysis 事实）
   - **原样保留** `MEDIA:/absolute/path` 行，平台才会发图
   - 不要把 base64 或整段 JSON 塞给用户
4. 若 `ok: false`：把错误说明白（例如先 `refresh` 或改用 `--local`），不要编造猪。

### 推荐回复模板（今日小猪 · Hub 默认）

```text
🐽 今日你是：{title}
来自 PigHub 的今日之猪～

MEDIA:{image_path}
```

### 本地模式模板（仅 `--local`）

```text
🐽 今日你是：{name}
{description}
分析：{analysis}

MEDIA:{image_path}
```

重复抽取时加一句「今天抽过啦，还是这只～」。

## Command Map

| 用户说法 | 命令 |
|---------|------|
| 今日小猪 / 今天是什么猪 | `today --user …`（**PigHub**） |
| 今日小猪（本地/性格分析） | `today --user … --local` |
| 随机小猪 | `random` |
| 找猪 丘吉尔 | `find 丘吉尔` |
| 刷新小猪 / 更新 PigHub | `refresh` |
| 小猪图鉴 / 有哪些猪 | `list` |
| 看看野猪 | `show wild-boar` 或 `show 野猪` |

## Data Layout

```
~/.hermes/skills/leisure/daily-pig/
├── SKILL.md
├── scripts/daily_pig.py
└── resource/
    ├── pig.json          # 本地 62 种：id/name/description/analysis
    ├── pig_hub.json      # PigHub 目录缓存（可 refresh）
    └── image/{id}.png    # 与 id 同名

$HERMES_HOME/daily-pig/
├── today.json            # {"date","source":"hub|local","records":{user: pig}}
└── hub-images/           # 下载的 PigHub 图缓存
```

图片扩展名匹配：`png/jpg/jpeg/webp/gif`（与原插件一致）。

## PigHub 说明

- 目录 API：`https://pighub.top/api/all-images`
- 图 URL：`https://pighub.top/images/{filename}`（目录里的 `/data/` 是逻辑路径，实际下载用 `/images/`）
- **`today`（默认）/ `random` / `find`** 会下载到本地再 `MEDIA:`，失败则退回 markdown 图片链接
- `today` 在 hub 缓存为空时会**自动 refresh 一次**；平时不要无刷
- Hub 条目字段主要是 `title` / `filename` / `thumbnail`（没有本地那套 analysis）

## Common Pitfalls

1. **手写 random 而不是跑脚本** — 会破坏「每天固定」语义，且丢图。
2. **`--user` 每天变** — 会变成每天多只猪；用平台稳定 id。
3. **丢掉 `MEDIA:` 行** — 用户只能看到文字看不到猪。
4. **把 `today` 误跑成 `--local`** — 用户没要求本地时，默认必须走 hub。
5. **改 skill 内 `resource/image` 当缓存** — hub 缓存应落在 `$HERMES_HOME/daily-pig/`，别污染 skill 资源。
6. **把完整 JSON 甩给用户** — JSON 只给 agent 解析。
7. **旧 today.json 仍是 local 记录** — 脚本在 `source` 切换时会重置；也可删 `$HERMES_HOME/daily-pig/today.json`。

## Verification

- [ ] `python3 …/daily_pig.py today --user test1` → `source: hub` + title + MEDIA（hub 缓存图）
- [ ] 同一 user 连抽两次，`is_repeat: true` 且同一 hub id/title
- [ ] 换 user 可能不同猪
- [ ] `today --local` 仍能出 62 池 name + analysis
- [ ] `list` 显示 62 头
- [ ] `refresh` 后 `random` / `find` 能出图
- [ ] 回复里含可投递的 `MEDIA:/…` 绝对路径

## Credits

- 原作 / 移植：`SonderXiaoming/huannai_plugin_rollpig`（HoshinoBot）
- 上游灵感：`Bearlele/nonebot-plugin-rollpig`
- 图库：`pighub.top`
