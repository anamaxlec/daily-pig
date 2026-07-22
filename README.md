<div align="center">

<img src="docs/assets/hero.svg" width="920" alt="Daily Pig — 今日小猪">

# 🐖 daily-pig

### 给 agent 用的「今天是什么小猪」

**对 agent 说一句「今日小猪」，或者自己跑一行命令，抽今天的猪。**
每人每天固定一只。默认从 PigHub 抽，也可以切回本地 62 种。

[![MIT License](https://img.shields.io/badge/license-MIT-18a87b?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square)](skills/daily-pig/scripts/daily_pig.py)
[![skill CLI](https://img.shields.io/badge/skill-CLI-111827?style=flat-square)](skills/daily-pig/SKILL.md)
[![PigHub](https://img.shields.io/badge/PigHub-1000%2B%20pigs-ff69b4?style=flat-square)](https://pighub.top)
[![本地猪圈](https://img.shields.io/badge/%E6%9C%AC%E5%9C%B0%E7%8C%AA%E5%9C%88-62-f59e0b?style=flat-square)](skills/daily-pig/resource/pig.json)

[安装](#-安装) · [玩法](#-三句口令) · [图鉴](#-本地猪圈精选) · [致谢](#-致谢)

</div>

---

## 这是什么

把群聊抽签梗「今天是什么小猪」搬到了 agent 上。

| 你说 | 发生什么 |
|------|----------|
| **今日小猪** | 从 PigHub 抽一只，今天之内重抽不变 |
| **随机小猪** | 从 PigHub 盲抽一张，不占今天的名额 |
| **找猪 丘吉尔** | 按关键词搜 PigHub（最多 8 张） |
| **今日小猪（本地）** | 用本地 62 种，带描述和性格分析 |

就是一个 Python 脚本，只用标准库。输出文案和图片路径，能跑 shell 的 agent 都能用：Claude Code、Codex、OpenCode、Pi、Hermes，或者你自己在终端跑也行。

> 这是上游插件的移植版，不是官方项目。出处见[文末致谢](#-致谢)，建议先给上游点 star。

---

## 🐷 三句口令

在 agent 对话里直接说：

```text
今日小猪
随机小猪
找猪 喜报
```

或者自己跑：

```bash
SCRIPT="skills/daily-pig/scripts/daily_pig.py"   # 或安装后的绝对路径

python3 "$SCRIPT" today --user alice          # 默认从 PigHub 抽
python3 "$SCRIPT" today --user alice --local  # 本地 62 种
python3 "$SCRIPT" random
python3 "$SCRIPT" find 丘吉尔
python3 "$SCRIPT" refresh                     # 更新 PigHub 目录
python3 "$SCRIPT" list                        # 本地图鉴
```

输出示例：

```text
今日你是：猪克力
来源：PigHub
URL：https://pighub.top/images/...

MEDIA:/Users/you/.daily-pig/hub-images/猪克力.jpg
```

`MEDIA:` 后面是图片的本地路径，agent 把文案和这张图一起发给用户即可。

---

## 🎨 本地猪圈精选

本地模式从这 62 种里抽，每种配了描述和一段性格分析：

| | | | |
|:---:|:---:|:---:|:---:|
| <img src="docs/assets/gallery/pig.png" width="140"><br>**猪**<br>普通小猪 | <img src="docs/assets/gallery/wild-boar.png" width="140"><br>**野猪**<br>勇猛的野猪！ | <img src="docs/assets/gallery/zhuge-liang.png" width="140"><br>**猪葛亮**<br>猪里最聪明的一个 | <img src="docs/assets/gallery/teammate-pig.png" width="140"><br>**猪队友**<br>团灭发动机 |
| <img src="docs/assets/gallery/demon-pig.png" width="140"><br>**恶魔猪**<br>满肚子坏心眼 | <img src="docs/assets/gallery/heaven-pig.png" width="140"><br>**天堂猪**<br>似了喵~ | <img src="docs/assets/gallery/zombie-pig.png" width="140"><br>**僵尸猪**<br>喜欢的食物是猪脑 | <img src="docs/assets/gallery/buddha-pig.png" width="140"><br>**佛猪**<br>施猪，一切随缘 |
| <img src="docs/assets/gallery/mechanical-pig.png" width="140"><br>**机械猪**<br>人机 | <img src="docs/assets/gallery/cyberpunk-pig.png" width="140"><br>**赛博朋克猪**<br>赛博猪猪 2077 | <img src="docs/assets/gallery/vangogh_pig.png" width="140"><br>**梵高猪**<br>星夜里的金色印象 | <img src="docs/assets/gallery/rainbow-pig.png" width="140"><br>**大色猪**<br>斯图亚特·彩虹猪 |
| <img src="docs/assets/gallery/tank_pig.png" width="140"><br>**坦克猪**<br>等待驾驶的重装小猪 | <img src="docs/assets/gallery/pig_god.png" width="140"><br>**智慧小猪之神**<br>智慧与好运 | <img src="docs/assets/gallery/apple-pig.png" width="140"><br>**苹果猪** | <img src="docs/assets/gallery/lemon-pig.png" width="140"><br>**柠檬猪** |

完整名单：`python3 …/daily_pig.py list`，或直接看 [pig.json](skills/daily-pig/resource/pig.json)。

```json
{
  "id": "teammate-pig",
  "name": "猪队友",
  "description": "团灭发动机",
  "analysis": "你天生自带令人窒息的操作光环……是群聊里不可或缺的开心果。"
}
```

---

## 🌐 PigHub 大海捞猪

默认模式从 [PigHub](https://pighub.top) 抽，图库一千多张，`refresh` 更新目录。下面几张是示意：

| | | | |
|:---:|:---:|:---:|:---:|
| <img src="docs/assets/hub/猪克力.jpg" width="150"><br>猪克力 | <img src="docs/assets/hub/猪理人.jpg" width="150"><br>猪理人 | <img src="docs/assets/hub/猪名言（丘吉尔）.png" width="150"><br>猪名言（丘吉尔） | <img src="docs/assets/hub/喜报.png" width="150"><br>喜报 |
| <img src="docs/assets/hub/悲报（死猪）.png" width="150"><br>悲报（死猪） | <img src="docs/assets/hub/恐怖猪.png" width="150"><br>恐怖猪 | <img src="docs/assets/hub/猪之暗面.jpg" width="150"><br>猪之暗面 | <img src="docs/assets/hub/猪龙鱼公爵.png" width="150"><br>猪龙鱼公爵 |

```bash
python3 "$SCRIPT" refresh
python3 "$SCRIPT" find 喜报
python3 "$SCRIPT" random
```

图片实际地址是 `https://pighub.top/images/{filename}`——目录接口返回的路径是 `/data/...`，下载时要换成 `/images/`。细节见 [NOTICE.md](NOTICE.md)。

---

## ✨ 功能

- `today`：每人每天固定一只，重抽不变，第二天重置
- `today --local`：本地 62 种（上游原版池子）；不加则默认 PigHub
- `find` / `random`：搜 PigHub 或盲抽
- 抽签记录和图片缓存放在 `~/.daily-pig/`（可用 `DAILY_PIG_HOME` 改）
- 只用 Python 标准库，无第三方依赖

---

## 📦 安装

### 一键安装

```bash
git clone https://github.com/anamaxlec/daily-pig.git
cd daily-pig
bash install.sh
```

脚本会检测下面几个目录，装进第一个存在的：

| Agent | 路径 |
|-------|------|
| 通用 | `~/.agents/skills/daily-pig` |
| Codex | `~/.codex/skills/daily-pig` |
| Claude Code | `~/.claude/skills/daily-pig` |
| OpenCode | `~/.opencode/skills/daily-pig` |
| Hermes | `~/.hermes/skills/leisure/daily-pig` |

指定目录：

```bash
DAILY_PIG_SKILL_DIR="$HOME/.codex/skills/daily-pig" bash install.sh
```

### 手动安装

```bash
git clone https://github.com/anamaxlec/daily-pig.git
cp -R daily-pig/skills/daily-pig /path/to/your/skills/daily-pig
```

### 验证

```bash
python3 /path/to/daily-pig/scripts/daily_pig.py today --user test
```

装好后在对话里说「今日小猪」。没反应的话开个新会话再试。

---

## 🗂 仓库结构

```text
daily-pig/
├── README.md
├── NOTICE.md                 # 上游致谢 + 修改说明
├── LICENSE
├── install.sh
├── docs/assets/
│   ├── hero.svg              # 原创头图（非上游 PigLogo）
│   ├── gallery/              # 本地猪展示图
│   └── hub/                  # PigHub 示意快照
└── skills/daily-pig/
    ├── SKILL.md
    ├── scripts/daily_pig.py
    └── resource/
        ├── pig.json
        ├── pig_hub.json
        └── image/*.png
```

运行时状态（不进 git）：

```text
~/.daily-pig/
├── today.json
└── hub-images/
```

---

## 🛠 命令

| 命令 | 作用 |
|------|------|
| `today [--user ID]` | 今日小猪（默认 PigHub） |
| `today --local` | 本地 62 种 |
| `today --no-download` | 只返回图片 URL，不下载 |
| `random` | 盲抽一张 |
| `find KEYWORD` | 搜标题，最多 8 张 |
| `refresh` | 更新 PigHub 目录 |
| `list` / `show ID` | 本地图鉴 |

环境变量：`DAILY_PIG_HOME`（状态目录）、`DAILY_PIG_USER`（默认用户）、`DAILY_PIG_SKILL_DIR`（安装目录）。

---

## 🙏 致谢

这些项目是上游，请先给它们点 star。

| 项目 | 说明 |
|------|------|
| [nonebot-plugin-rollpig](https://github.com/Bearlele/nonebot-plugin-rollpig) | 最早的「今天是什么小猪」插件 |
| [huannai_plugin_rollpig](https://github.com/SonderXiaoming/huannai_plugin_rollpig) | 本仓库移植的 HoshinoBot 版本 |
| [PigHub](https://pighub.top) | 在线猪图库 |

### 和上游的区别

- 去掉 HoshinoBot 插件框架，改成独立 CLI
- `today` 默认从 PigHub 抽（上游只用本地池），本地池保留为 `--local`
- 修了图片地址：`/data/` 改为 `/images/`
- 抽签记录存 `~/.daily-pig/`，不绑任何 agent
- 头图是自绘的 SVG，没用上游的 PigLogo

细节见 [NOTICE.md](NOTICE.md)。

### 版权

- 代码沿用上游 MIT 协议（[LICENSE](LICENSE)）
- PigHub 图片版权归原站所有，`docs/assets/hub/` 只是示意
- 本地图片资源来自上游插件，如有异议请开 issue
- 本项目与上游作者、PigHub 没有官方关系

---

## 🧪 自检

```bash
python3 skills/daily-pig/scripts/daily_pig.py list | head
python3 skills/daily-pig/scripts/daily_pig.py today --user ci-test
python3 skills/daily-pig/scripts/daily_pig.py today --user ci-test   # is_repeat
python3 skills/daily-pig/scripts/daily_pig.py today --user ci-test --local
```

---

## TODO

- [ ] 定时任务：每天早上自动推一只
- [ ] 群聊「今日全员猪榜」
- [ ] 自定义本地猪 / 投稿
- [ ] HTML 图鉴页

欢迎 PR，新增猪图请注明来源。

---

<div align="center">

**今天也要开心做猪。**

<sub>🐽 猪来自 <a href="https://github.com/SonderXiaoming/huannai_plugin_rollpig">上游猪圈</a> 和 <a href="https://pighub.top">PigHub</a>，喜欢请先给它们点 star</sub>

</div>
