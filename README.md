# shuai-cover-resize

将一张已有封面重构为小红书、B站、YouTube 和公众号所需比例，同时保持原文案、人物身份与核心画面一致。

## 安装

```bash
git clone git@github.com:qizong007/shuai-cover-resize.git ~/.agents/skills/shuai-cover-resize
```

## 使用

在 Codex 中调用 `$shuai-cover-resize`，并提供源封面及目标比例。未指定比例时默认生成 `4:3`、`3:4` 和 `16:9`。

