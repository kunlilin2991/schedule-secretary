# schedule-secretary — Project Brief

> 这是一份给 Claude Code 的项目交接文档,沉淀了项目从 idea 到架构决策的全过程。
> 当 Claude Code 第一次打开这个项目时,**先完整读这份文档**,再开始工作。
> 文档是活的,随时根据实际进展更新。

---

## 0. TL;DR(30 秒理解项目)

**做什么**:一个**自用**的 AI 日程秘书,接收多模态输入(文字/图片/语音),
LLM 自动解析成日程,通过飞书卡片确认后,写入飞书日历。

**核心价值**:把"日程录入"从手动操作变成"发条消息给 AI"。

**形态**:**不做 app**,不做日历 UI。栖息在飞书内,通过飞书机器人作为入口,
飞书日历作为视图和提醒。**用户感知不到"app"的存在**。

**底座**:**Hermes Agent**(NousResearch 开源,2026 年成熟的 agent harness)。
你的工作只是写一个 `schedule_secretary` skill + 配置飞书机器人。

**目标用户**:**只有作者本人**。不做 to C,不做 to B,不做商业化。

---

## 1. 项目背景

### 1.1 为什么做这个

作者每天接收大量需要变成日程的信息——微信消息、口头通知、邮件、报表、海报。
传统流程("打开日历 app → 手动建事件 → 设提醒")的摩擦点:
- 切换 app 打断工作流
- 多模态信息(图片、语音)要先用脑子解析才能录入
- 录入慢、容易漏
- 没有 AI 主动思考(冲突检测、建议、习惯学习)

LLM 时代,这件事应该可以变成"发消息给 AI,它替我处理"。

### 1.2 为什么不做商业化

讨论过完整商业模式后的判断:
- 这个赛道海外有 Motion 跑通了高端订阅($19-29/月),但服务的是时薪 50+ 美元的人群
- 中国 C 端订阅天花板太低,LLM 成本+用户付费意愿倒挂,商业上跑不通
- "信息录入摩擦"是 D 级痛点,不是 A 级痛点
- OS 厂商(Apple Intelligence / Gemini)和超级 app(豆包/字节)在系统级吃掉这个场景
- 历史上 Sunrise / Tempo / Timeful 全死了,被巨头收购后关闭
- 即使能做,获客和留存对独立开发者是地狱难度

**结论:商业上不值得做,但作为自用工具极其有用,因此走自用路线。**

### 1.3 为什么不做独立 app

讨论过手机 app + Windows app 的完整方案后的判断:
- 独立 app 要重新发明日历视图、强提醒、多端同步——全是系统已经做好的事
- 国产 Android ROM 对第三方 app 的后台/提醒限制极严,做不出可靠的强提醒
- "强提醒"是日历的核心价值,这件事**只有系统日历能做好**(AlarmClock 级别)
- Flutter/原生开发投入 1-2 个月,产出的是一个比系统日历更差的工具
- 作者要的是"AI 大脑",不是"UI 工具"

**结论:不做 app,只做 agent。**

### 1.4 为什么用飞书,不用微信

- 微信对外部 SDK 极不友好,主动发消息容易封号
- 企业微信能用但限制多
- **飞书有官方 API,机器人主动发消息合法且稳定**
- 飞书 Interactive Card 原生支持"AI 给草稿 + 用户点按钮确认"流程
- 飞书自带日历,API 完整,可以作为日程的主存储 + 视图 + 提醒源
- 飞书 Windows / 手机 / 网页全平台一致,天然解决多端同步
- 国产 Android ROM 对飞书的后台保活有白名单优待
- 作者已经在用飞书

### 1.5 为什么用 Hermes Agent,不用 OpenClaw,不自己写

走过的弯路:
- 最初想用 OpenClaw,但 OpenClaw 是"重型框架",作者只需要"飞书接入 + LLM 调用 + cron"几个功能,装了能跑 50 件事的工具
- 考虑过完全自己写(500-800 行 Python),但这是 24-25 年的思路
- **2026 年正确答案是 Hermes Agent(NousResearch 出品,2026 年 3-5 月成熟)**

Hermes Agent 的关键优势:
- **官方支持飞书/Lark adapter**(v0.6.0 起,first-class)
- **支持 WebSocket 模式**,完美适合家里 Ubuntu 在 NAT 后的场景
- 飞书 Interactive Card 回调完整支持
- 内置自然语言 cron scheduler("每天早 8 点汇报今天日程"——这正是主动提醒的核心)
- MEMORY.md / SKILL Markdown 标准(Anthropic Skill 兼容)
- Honcho 用户建模 + 长期记忆
- **`hermes claw migrate` 一键从 OpenClaw 迁移配置**
- 支持中国模型(Kimi/MiniMax/GLM/DeepSeek/MiMo)
- 16+ 渠道支持,未来可扩展(钉钉、企微、微信等)
- 文档完整,153k stars,极活跃(2026-05-16 还在发版)

### 1.6 为什么单向同步(飞书日历主,谷歌日历可选)

讨论过双向同步飞书↔谷歌日历后的判断:
- 真·双向同步是分布式系统的脏活(conflict resolution 问题)
- 作者真实需求是"在公司能查日程",不是"在公司能改日程"
- 即使要镜像到谷歌日历,也用单向写入(agent 写双份),不做反向同步
- MVP 阶段**只做飞书,不做谷歌镜像**——降低复杂度

---

## 2. 当前基础设施(已就绪的东西)

### 2.1 硬件

| 设备 | 状态 | 用途 |
|---|---|---|
| 家里 Ubuntu Linux | ✅ 已部署 | 算力主力,跑 Hermes Agent |
| 境外 VPS (1C/1G/15G, IP: 38.47.125.215) | ✅ 已部署 | 公网入口、反向隧道、Xray 代理 |
| Windows 公司电脑 | ⚠️ 公司有网络限制,无法接入飞书 | 仅作为可选浏览器入口 |
| 个人 PC | ❌ 坏了,预计修一周 | 作者本地开发环境(暂不可用) |

### 2.2 软件 & 服务

| 项目 | 状态 |
|---|---|
| 反向 SSH 隧道(autossh + systemd, VPS ↔ 家里 Ubuntu) | ✅ 已配置 |
| Xray VLESS+Reality 代理(loop-prevention 路由) | ✅ 已配置 |
| OpenRouter API(DeepSeek v3.2 为主) | ✅ 已配置 |
| Claude Code(用于 AI 辅助开发) | ✅ 已配置在 Windows 公司电脑(WSL2) |
| OpenClaw / CowAgent | ✅ 已配置在家里 Ubuntu(待迁移到 Hermes) |
| Hermes Agent | ❌ 待安装 |
| 飞书自建应用(机器人 + 日历权限) | ⚠️ 待申请(权限审批异步,提前申请省时间) |

---

## 3. 目标架构

```
┌─────────────────────────────────────────────────┐
│  家里 Ubuntu(算力主力,NAT 后)                │
│                                                   │
│  ┌─────────────────────────────────────┐        │
│  │  Hermes Agent                        │        │
│  │  - 飞书 adapter(WebSocket 模式)    │        │
│  │  - 自然语言 cron scheduler           │        │
│  │  - MEMORY.md 长期记忆                │        │
│  │  - Honcho 用户建模                   │        │
│  │  - DeepSeek via OpenRouter           │        │
│  │  - 多模态(文/图/语音)              │        │
│  │                                       │        │
│  │  + skills/schedule_secretary.md       │        │
│  │    ├─ parse_event(多模态 → 结构化) │        │
│  │    ├─ check_conflict(查飞书日历)   │        │
│  │    ├─ draft_card(发飞书卡片)        │        │
│  │    ├─ write_event(调飞书日历 API)  │        │
│  │    └─ daily_brief(cron 主动汇报)   │        │
│  └──────────────────┬───────────────────┘        │
│                      │                            │
│                      │ Lark SDK WebSocket         │
│                      ▼                            │
└──────────────────────┼─────────────────────────────┘
                       │
                       │ (外部网络)
                       │
                       ▼
              ┌─────────────────┐
              │  飞书服务器      │
              └────────┬────────┘
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
            飞书 IM   飞书日历   飞书文档
              │        │
              │        │ 自动多端同步
              │        │
              ▼        ▼
         手机/电脑/平板的飞书 app
         (视图 + 飞书原生强提醒)
```

**关键设计**:
- **入口唯一**:飞书 IM(用户给 bot 发消息)
- **出口双重**:飞书 IM(确认卡片、主动提醒消息)+ 飞书日历(事件 + 系统级强提醒)
- **存储单一**:飞书日历是唯一事实源
- **零客户端**:不写 app、不写 Windows 端、不写 Web 端

---

## 4. MVP 范围

### 4.1 MVP 做什么(v0.1)

- [x] Hermes Agent 部署在家里 Ubuntu
- [x] 飞书机器人接入(WebSocket 模式)
- [x] `schedule_secretary` skill 基础版:
  - 接收纯文字消息
  - LLM 解析成结构化事件
  - 写入飞书日历
  - 飞书 IM 返回确认消息
- [x] 飞书日历的原生强提醒生效

### 4.2 MVP+1 做什么(v0.2)

- [ ] 飞书 Interactive Card:AI 给草稿,用户点按钮才确认入库
- [ ] 图片识别(多模态 LLM 解析截图、海报)
- [ ] 语音输入(Whisper 或飞书原生语音转文字)
- [ ] 冲突检测(查飞书日历,提示时间冲突)

### 4.3 v0.3 及之后

- [ ] 自然语言 cron(每天早晨汇报、每周日总结)
- [ ] 长期记忆(记住常见联系人、地点、习惯)
- [ ] 主动思考(基于历史模式给建议)
- [ ] 飞书文档评论 @ bot(用 Hermes 已有能力)
- [ ] (可选)谷歌日历单向镜像
- [ ] (可选)Web 入口给公司网络环境使用

### 4.4 明确不做

- ❌ 独立 Android app / iOS app
- ❌ Windows 桌面 app
- ❌ 日历视图、月视图、周视图(用飞书自带的)
- ❌ 自己实现提醒系统(飞书日历负责)
- ❌ 双向同步飞书↔谷歌
- ❌ to B / to C 商业化任何方向
- ❌ 上架应用市场

---

## 5. 任务清单(按优先级)

### Phase 0: 准备(无需电脑,可手机完成)

- [ ] 在 GitHub 建 private repo `schedule-secretary`(初始空仓库)
- [ ] 申请飞书开放平台自建应用,拿到 App ID / Secret(权限审批异步,提前申请)
- [ ] 通读 Hermes Agent 文档,重点:
  - 安装和初始化
  - Feishu / Lark 配置
  - Skills 系统
  - Cron scheduler
- [ ] 测试飞书自带日历在作者手机上的强提醒可靠性(锁屏 30 分钟后是否仍能响)

### Phase 1: Hermes Agent 落地

- [ ] 在家里 Ubuntu 上安装 Hermes Agent
- [ ] `hermes claw migrate --dry-run` — 看 OpenClaw 配置能迁移什么
- [ ] `hermes gateway setup` 配置飞书 adapter(WebSocket 模式)
- [ ] 测试:给飞书 bot 发"hello",收到回应

### Phase 2: 飞书日历集成

- [ ] 给飞书应用申请日历权限:
  - `calendar:calendar`
  - `calendar:calendar.event:create`
  - `calendar:calendar.event:read`
  - `calendar:calendar.event:update`
  - `calendar:calendar.event:delete`
- [ ] 写一个最简 test script,调飞书日历 API 创建一个测试事件
- [ ] 验证手机飞书日历能看到该事件,提醒能弹

### Phase 3: schedule_secretary skill v0.1

- [ ] 写 skill markdown 文件:`skills/schedule_secretary/SKILL.md`
- [ ] 实现 `parse_event` 子能力(纯文字 → 结构化 JSON)
- [ ] 实现 `write_event` 子能力(结构化 JSON → 飞书日历 API)
- [ ] 端到端测试:发"明天下午 3 点和小王开会"→ 飞书日历看到事件

### Phase 4: 卡片确认流程

- [ ] 实现 `draft_card` 子能力(返回飞书 Interactive Card)
- [ ] 实现卡片按钮回调(确认/修改/取消)
- [ ] 端到端测试:发消息 → 收到卡片 → 点确认 → 事件写入

### Phase 5: 多模态

- [ ] 图片输入:发截图给 bot,LLM 解析图中的事件信息
- [ ] 语音输入:发语音消息,转文字后解析
- [ ] 测试常见场景:微信群截图、活动海报、邮件截图

### Phase 6: 冲突检测和主动能力

- [ ] `check_conflict` 子能力:查飞书日历当时间段是否有其他事件
- [ ] 卡片里展示冲突信息,允许"仍然添加"或"建议替代时间"
- [ ] 自然语言 cron:配置"每天早 8 点汇报今天日程"

---

## 6. 关键技术决策和坑

### 6.1 Prompt 设计要点(parse_event 核心难点)

LLM 解析日程容易在以下场景出错,**prompt 必须特殊处理**:

1. **相对时间**:"下周三"在不同上下文里有歧义
   - 解法:prompt 里**显式注入当前 datetime**(`current_datetime: 2026-XX-XX HH:MM Beijing`)
2. **不完整信息**:"周三开会" 没说几点
   - 解法:不要让 LLM 瞎猜,返回 `time: null`,在卡片里追问
3. **重复事件**:"每周一例会 10 点"
   - 解法:生成 iCal RRULE,反复测试边界
4. **多事件**:一张海报有 3 个活动
   - 解法:prompt 明确"返回数组,即使只有一个事件"
5. **时区**:海外邮件含其他时区
   - 解法:默认时区 `Asia/Shanghai`,prompt 说明转换规则
6. **事件 vs 备忘**:"记得明天买牛奶" 是 todo 不是日程
   - 解法:让 LLM 自己分类 `event(有具体时间)` vs `reminder(只是要做的事)`

### 6.2 强提醒可靠性

- 完全依赖飞书日历的原生提醒
- 国产 ROM 上飞书有保活白名单,理论可靠
- **必须实测**:作者手机锁屏 30 分钟+,飞书提醒是否仍能弹
- 如失败,考虑双重提醒:飞书机器人推送 + 飞书日历提醒

### 6.3 不要做双向同步

- 飞书日历是唯一事实源
- 不要尝试同步到谷歌日历后再反向同步
- 如需谷歌日历视图,**只做单向写入,谷歌端只读**

### 6.4 OpenRouter / DeepSeek 调用稳定性

- 家里 Ubuntu 通过 OpenRouter 调 DeepSeek,网络稳定性问题不大
- 但要做超时、重试、降级
- 多模态可能要用 Qwen-VL 或 GPT-4o-mini(看 Hermes 的 provider 配置)

### 6.5 飞书 API rate limit

- 每天给单个外部联系人发消息有上限(自用足够)
- 日历 API 也有 rate limit,大批量操作要做退避

---

## 7. Skill 结构草案

```
skills/
└── schedule_secretary/
    ├── SKILL.md                    # 主入口,描述能力和触发条件
    ├── prompts/
    │   ├── parse_event.md          # 解析事件的 system prompt
    │   ├── classify_intent.md      # 区分 event vs reminder vs query
    │   └── daily_brief.md          # 每日汇报的 prompt
    ├── tools/
    │   ├── feishu_calendar.py      # 飞书日历 API 封装
    │   ├── feishu_card.py          # 飞书 Interactive Card 构造
    │   └── conflict_checker.py     # 冲突检测逻辑
    └── tests/
        ├── parse_event_cases.md    # 测试用例(各种边界情况)
        └── e2e_test.py
```

`SKILL.md` 的关键字段(Anthropic Skill 标准):
- `name`: schedule_secretary
- `description`: 接收多模态信息,解析成日程,写入飞书日历
- `triggers`: 用户在飞书 IM 发送含时间信息的消息
- `tools`: feishu_calendar, feishu_card

---

## 8. 未解决的问题(待 review)

这些是项目正式启动前需要 double check 的事项:

- [ ] **OpenClaw 的什么配置需要迁移到 Hermes**,什么可以丢弃
- [ ] **Hermes 飞书 adapter 是否支持 Interactive Card 回调**(README 说支持,需实测)
- [ ] **飞书日历 API 在 Hermes 里需要写自己的 tool 还是已有插件**
- [ ] **资源占用是否在家里 Ubuntu 可承受范围**(Hermes + 现有服务并存)
- [ ] **是否保留 OpenClaw 作为通用助理**,与 Hermes 并存,还是完全替换
- [ ] **VPS 上的 SearXNG 是否真的在运行**(此前提到但未确认)
- [ ] **后续是否加 Web 入口给公司网络使用**(MVP 暂不做,v0.3+ 再考虑)

---

## 9. 开发环境

### 9.1 推荐方案

- **主开发环境**:GitHub Codespaces(浏览器即可访问,装 Claude Code 即用)
- **部署环境**:家里 Ubuntu(Hermes Agent 运行处)
- **应急编辑**:手机 SSH 到家里 Ubuntu + 终端 Claude Code
- **版本控制**:GitHub private repo `schedule-secretary`
- **CI/CD**:暂不做,等项目稳定后用 GitHub Actions 实现"push 后自动 SSH 部署"

### 9.2 Claude Code 使用建议

- 第一次打开项目:**先读完 PROJECT.md**,理解决策背景再动手
- 不要试图说服作者"加个 Android app"——这是已经否决的方案
- 不要试图加商业化——这是已经否决的方向
- 优先使用 Hermes Agent 已有能力,而不是从零写
- Skill 用 Markdown 格式(Anthropic Skill 标准),不要用 Python class

---

## 10. 项目元信息

- **作者**:Kunli(Hihonor / Honor Device Co.)
- **创建时间**:2026-06
- **当前阶段**:架构设计完成,准备开发
- **沟通语言**:中文为主,代码注释和 API 文档可英文
- **License**:私有项目,不开源(暂定)

---

## 附录 A: 关键参考

- Hermes Agent: https://github.com/NousResearch/hermes-agent
- Hermes 飞书文档: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/feishu
- 飞书开放平台: https://open.feishu.cn
- 飞书日历 API: https://open.feishu.cn/document/server-docs/calendar-v4/
- OpenClaw → Hermes 迁移: 见 Hermes v0.6.0 Release Notes

## 附录 B: 讨论历史压缩版

完整的产品/架构讨论经过以下几轮迭代收敛到当前方案:

1. **初想**:做一个 to C 的 AI 日程 app — 否决(商业不可行)
2. **转向自用工具**:做手机 + Windows 双客户端 — 否决(强提醒做不好)
3. **极简化**:只做 Android,日历交给系统日历 — 改进
4. **改为中间件**:不做日历 UI,只做"输入层" — 关键洞察
5. **改用飞书**:绕过微信封号风险,飞书 API 友好 — 确定
6. **进一步简化**:不要日历 app,飞书日历就是 UI + 提醒 — 完整简化
7. **架构反思**:OpenClaw 太重 — 准备换底座
8. **找到 Hermes Agent**:2026 年最合适的 agent harness — 当前方案
9. **确认飞书支持**:Hermes 官方 first-class 支持飞书 — 锁定

每一步的具体理由和被否决方案的细节,见上面各节。
