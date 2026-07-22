<div align="center">

<img src="docs/assets/logo.jpeg" width="220" alt="今日小猪 logo">

# 🐖 hermes-daily-pig

### 今天是什么小猪 · Hermes Skill 版

**对 Hermes 说一句「今日小猪」，拿回一张今日限定猪图。**  
每人每天固定一只 · 默认走 PigHub 大海 · 也可切回经典 62 种本地猪圈。

[![MIT License](https://img.shields.io/badge/license-MIT-18a87b?style=flat-square)](LICENSE)
[![Hermes Skill](https://img.shields.io/badge/Hermes-Skill-111827?style=flat-square)](https://hermes-agent.nousresearch.com/)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square)](skills/daily-pig/scripts/daily_pig.py)
[![PigHub](https://img.shields.io/badge/PigHub-1000%2B%20pigs-ff69b4?style=flat-square)](https://pighub.top)
[![Local Roster](https://img.shields.io/badge/local%20roster-62-f59e0b?style=flat-square)](skills/daily-pig/resource/pig.json)

[安装](#-安装到-hermes) · [玩法](#-三句口令) · [图鉴](#-本地猪圈精选-62-种里的明星) · [致谢](#-致谢--出处--我们改了什么)

</div>

---

## 这是什么

把群聊名梗 **「今日小猪」** 包装成 [Hermes Agent](https://hermes-agent.nousresearch.com/) 可加载的 skill：

| 你说 | 发生什么 |
|------|----------|
| **今日小猪** | 从 **PigHub** 抽今日之猪，同一用户当天结果锁定 |
| **随机小猪** | 再从 PigHub 盲抽一张（不占今日坑位） |
| **找猪 丘吉尔** | 按标题关键词搜 PigHub（最多 8 张） |
| **今日小猪（本地）** | 可选：经典 62 种，自带毒舌 `description` + `analysis` |

底层是零依赖 Python CLI，stdout 里直接吐 `MEDIA:/绝对路径`，Telegram / gateway 能原图发出去。

> 本仓库是 **移植与再包装**，不是原作者官方续作。  
> 猪圈先辈列表见文末 **[致谢](#-致谢--出处--我们改了什么)**，请先给他们点 star 🐷

---

## 🐷 三句口令

在 Hermes（CLI / Desktop / Telegram gateway）里直接说：

```text
今日小猪
随机小猪
找猪 喜报
```

或手动跑脚本：

```bash
SCRIPT="$HOME/.hermes/skills/leisure/daily-pig/scripts/daily_pig.py"

# 默认：PigHub 今日之猪（每人每天固定）
python3 "$SCRIPT" today --user 364882308

# 经典本地 62 种（带性格分析）
python3 "$SCRIPT" today --user 364882308 --local

python3 "$SCRIPT" random
python3 "$SCRIPT" find 丘吉尔
python3 "$SCRIPT" refresh   # 刷新 PigHub 目录缓存
python3 "$SCRIPT" list      # 本地图鉴
```

### 输出长这样

```text
今日你是：猪克力
来源：PigHub
URL：https://pighub.top/images/...

MEDIA:/Users/you/.hermes/daily-pig/hub-images/猪克力.jpg
```

Agent 应把文案 + `MEDIA:` 行原样交给用户（**不要丢掉 MEDIA 行**，否则只有字没有猪）。

---

## 🎨 本地猪圈精选（62 种里的明星）

本地模式 `today --local` / `show` 使用随仓库分发的经典 roster。下面是一部分你可能已经在群聊见过的脸：

| | | | |
|:---:|:---:|:---:|:---:|
| <img src="docs/assets/gallery/pig.png" width="140"><br>**猪**<br>普通小猪 | <img src="docs/assets/gallery/wild-boar.png" width="140"><br>**野猪**<br>勇猛的野猪！ | <img src="docs/assets/gallery/zhuge-liang.png" width="140"><br>**猪葛亮**<br>猪里最聪明的一个 | <img src="docs/assets/gallery/teammate-pig.png" width="140"><br>**猪队友**<br>团灭发动机 |
| <img src="docs/assets/gallery/demon-pig.png" width="140"><br>**恶魔猪**<br>满肚子坏心眼 | <img src="docs/assets/gallery/heaven-pig.png" width="140"><br>**天堂猪**<br>似了喵~ | <img src="docs/assets/gallery/zombie-pig.png" width="140"><br>**僵尸猪**<br>喜欢的食物是猪脑 | <img src="docs/assets/gallery/buddha-pig.png" width="140"><br>**佛猪**<br>施猪，一切随缘 |
| <img src="docs/assets/gallery/mechanical-pig.png" width="140"><br>**机械猪**<br>人机 | <img src="docs/assets/gallery/cyberpunk-pig.png" width="140"><br>**赛博朋克猪**<br>赛博猪猪 2077 | <img src="docs/assets/gallery/vangogh_pig.png" width="140"><br>**梵高猪**<br>星夜里的金色印象 | <img src="docs/assets/gallery/rainbow-pig.png" width="140"><br>**大色猪**<br>斯图亚特·彩虹猪 |
| <img src="docs/assets/gallery/tank_pig.png" width="140"><br>**坦克猪**<br>等待驾驶的重装小猪 | <img src="docs/assets/gallery/pig_god.png" width="140"><br>**智慧小猪之神**<br>智慧与好运 | <img src="docs/assets/gallery/apple-pig.png" width="140"><br>**苹果猪** | <img src="docs/assets/gallery/lemon-pig.png" width="140"><br>**柠檬猪** |

完整 62 头名单：`python3 …/daily_pig.py list` 或打开 [`skills/daily-pig/resource/pig.json`](skills/daily-pig/resource/pig.json)。

每条本地猪长这样：

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

默认 **今日小猪** 不走 62 池，而是从 [PigHub](https://pighub.top) 公开图库里抽（目录缓存约 1000+ 张，可 `refresh`）。

README 里放几张 **示意快照**（版权与更新以 PigHub 为准；完整图库请去官网）：

| | | | |
|:---:|:---:|:---:|:---:|
| <img src="docs/assets/hub/猪克力.jpg" width="150"><br>猪克力 | <img src="docs/assets/hub/猪理人.jpg" width="150"><br>猪理人 | <img src="docs/assets/hub/猪名言（丘吉尔）.png" width="150"><br>猪名言（丘吉尔） | <img src="docs/assets/hub/喜报.png" width="150"><br>喜报 |
| <img src="docs/assets/hub/悲报（死猪）.png" width="150"><br>悲报（死猪） | <img src="docs/assets/hub/恐怖猪.png" width="150"><br>恐怖猪 | <img src="docs/assets/hub/猪之暗面.jpg" width="150"><br>猪之暗面 | <img src="docs/assets/hub/猪龙鱼公爵.png" width="150"><br>猪龙鱼公爵 |

```bash
python3 "$SCRIPT" refresh
python3 "$SCRIPT" find 喜报
python3 "$SCRIPT" random
```

图片实际下载地址使用：

```text
https://pighub.top/images/{filename}
```

（目录 JSON 里常见 `/data/...` 路径是逻辑路径；本 skill 已改成 `/images/` 才能稳定下到图。详见 [NOTICE.md](NOTICE.md)。）

---

## ✨ 主要功能

- **今日锁定**：按 `--user`（Telegram 建议用数字 uid）一天一只，重复抽取返回同一只
- **双池切换**：默认 Hub 大海；`--local` 回到经典 62 + 性格分析
- **找猪 / 随机**：PigHub 标题搜索与盲抽
- **自动缓存**：Hub 图落到 `$HERMES_HOME/daily-pig/hub-images/`，今日记录在 `today.json`
- **Agent 友好**：`MEDIA:` + JSON trailer，方便 gateway 发图
- **零第三方依赖**：系统 `python3` 即可（标准库 `urllib`）

```text
今日缓存规则
────────────
source = hub | local
同一天 + 同一 user + 同一 source → 固定
换日 或 切换 source → 重新抽
```

---

## 📦 安装到 Hermes

### 一键脚本

```bash
git clone https://github.com/anamaxlec/hermes-daily-pig.git
cd hermes-daily-pig
bash install.sh
```

会安装到：

```text
~/.hermes/skills/leisure/daily-pig/
```

### 手动安装

```bash
git clone https://github.com/anamaxlec/hermes-daily-pig.git
mkdir -p ~/.hermes/skills/leisure
cp -R hermes-daily-pig/skills/daily-pig ~/.hermes/skills/leisure/
```

### 验证

```bash
python3 ~/.hermes/skills/leisure/daily-pig/scripts/daily_pig.py today --user test
```

在聊天里说 **今日小猪**。若 agent 没自动加载 skill，新开会话或 `/reload-skills`（视你的 Hermes 版本）。

> Profile 隔离：把 `HERMES_HOME` 指到对应 profile 目录再装一遍即可。

---

## 🗂 仓库结构

```text
hermes-daily-pig/
├── README.md                 # 你正在看的这份
├── NOTICE.md                 # 上游致谢 + 修改说明（必读）
├── LICENSE                   # MIT（保留原作者版权声明）
├── install.sh
├── docs/assets/
│   ├── logo.jpeg
│   ├── gallery/              # 本地明星猪展示图
│   └── hub/                  # PigHub 示意快照（非完整图库）
└── skills/daily-pig/         # 真正装进 Hermes 的 skill
    ├── SKILL.md
    ├── scripts/daily_pig.py
    └── resource/
        ├── pig.json          # 本地 62 种
        ├── pig_hub.json      # PigHub 目录缓存（可 refresh）
        └── image/*.png
```

运行时状态（**不进 git**）：

```text
$HERMES_HOME/daily-pig/
├── today.json
└── hub-images/
```

---

## 🛠 CLI 速查

| 命令 | 作用 |
|------|------|
| `today [--user ID]` | PigHub 今日猪（默认） |
| `today --local` | 本地 62 种 + analysis |
| `today --no-download` | Hub 模式只返回 URL |
| `random` | 再盲抽一张 Hub 图 |
| `find KEYWORD` | 搜标题，最多 8 张 |
| `refresh` | 拉最新 `pighub.top/api/all-images` |
| `list` / `show ID` | 本地图鉴 |

---

## 🙏 致谢 · 出处 · 我们改了什么

**没有这些项目，就没有这头猪。请优先 star 上游。**

| 项目 | 说明 | 链接 |
|------|------|------|
| **nonebot-plugin-rollpig** | 原始「今天是什么小猪」灵感与传统 | https://github.com/Bearlele/nonebot-plugin-rollpig |
| **huannai_plugin_rollpig** | 我们直接参考/移植的 HoshinoBot 版（命令、资源、PigHub 刷新思路） | https://github.com/SonderXiaoming/huannai_plugin_rollpig |
| **PigHub** | 在线猪图大海 | https://pighub.top |
| **Hermes Agent** | 运行本 skill 的 agent 框架 | https://github.com/NousResearch/hermes-agent |

### 相对 `huannai_plugin_rollpig` 的主要修改

1. 去掉 NoneBot / HoshinoBot 插件壳，改成 **独立 CLI + Hermes `SKILL.md`**
2. **`today` 默认源改为 PigHub**；本地 62 种保留为 `today --local`
3. 修正图片 URL：`/data/` → 实际可用的 **`/images/`**
4. 今日缓存与 Hub 下载放到 **`$HERMES_HOME/daily-pig/`**，避免污染 skill 目录
5. 增加 agent 交付约定：`MEDIA:` 行 + JSON trailer
6. 本仓库 README / docs 展示图与安装脚本

更细的对照表见 **[NOTICE.md](NOTICE.md)**。

### 版权与内容说明

- 代码与本地 roster 移植路径遵循上游 **MIT**（见 [LICENSE](LICENSE)，保留 Bear_lele 等版权声明）
- **PigHub 上的图片版权归原作者 / PigHub**；本仓库 `docs/assets/hub/` 仅为 README 示意快照，不宣称拥有其版权
- 本地 `resource/image` 随上游插件资源分发，用于经典模式；若权利人有异议请开 issue，我们会配合调整
- 本项目与原作者、PigHub **无官方隶属关系**

---

## 🧪 自检

```bash
python3 skills/daily-pig/scripts/daily_pig.py list | head
python3 skills/daily-pig/scripts/daily_pig.py today --user ci-test
python3 skills/daily-pig/scripts/daily_pig.py today --user ci-test   # 应 is_repeat
python3 skills/daily-pig/scripts/daily_pig.py today --user ci-test --local
```

---

## 🗺 可能的下一步

- [ ] Hermes cron：每天早上自动推送今日小猪
- [ ] 群聊共享「今日全员猪榜」
- [ ] 用户自定义本地猪 JSON / 投稿
- [ ] 更漂亮的 HTML 图鉴页

PR 与新猪投稿都欢迎 —— 记得在 PR 里写清楚图源。

---

<div align="center">

**今天也要开开心心做一头猪。**

<sub>Ported with 🐽 for Hermes · please star the <a href="https://github.com/SonderXiaoming/huannai_plugin_rollpig">upstream pigsty</a> first</sub>

</div>
