# 最简单的智能客服

使用 VeADK 定义客服，使用 AgentKit Python SDK 的 `AgentkitAgentServerApp` 提供 HTTP 服务。支持中文 FAQ 问答、流式回复和内存中的连续对话。

## 启动

需要 Python 3.12 和 uv，以及已开通的模型。

在 AgentKit 云上部署时，VeADK 使用运行角色自动置换模型凭据，无需提供密钥、环境变量或 `config.json`。部署入口填写 `app.py`，默认监听 `0.0.0.0:8000`。运行角色需具备 VeADK 获取模型凭据所需的权限。

仓库自带 Dockerfile，使用 AgentKit 官方 Python 3.12 基础镜像，并显式从 PyPI 安装依赖，避免构建环境的镜像源尚未同步 SDK 版本。

本地运行时，可以通过可选的 `config.json` 显式提供模型配置：

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
cp config.example.json config.json
```

编辑 `config.json`，填写 `model_api_key`，并确认 `model_name` 为账号可用的模型名称或 Endpoint ID。然后启动：

```bash
.venv/bin/python app.py
```

应用不读取或设置环境变量，不需要 `.env` 或 `export`。有 `config.json` 时读取该文件，否则使用 `config.example.json`；密钥留空时由 VeADK 自动获取。依赖 SDK 自身可能读取其内部默认配置。`config.json` 已被 Git 忽略，仓库不包含真实密钥。

## 对话

```bash
curl -N http://127.0.0.1:8000/invoke \
  -H 'Content-Type: application/json' \
  -H 'user_id: demo-user' \
  -H 'session_id: demo-session' \
  -d '{"prompt":"你们多久发货？"}'
```

响应为 SDK 原生 SSE 事件，回复文字位于 `content.parts[].text`。再次请求时沿用相同的 `user_id` 和 `session_id` 即可连续对话；新对话更换 `session_id`。应用重启后内存会话丢失。SDK 也提供原生会话及 `/run_sse` 接口。

修改 `faq.md` 即可调整客服知识，修改后重启服务。示例没有订单、退款或人工转接系统；超出 FAQ 的问题会提示咨询人工。

这个最小示例未添加应用层用户认证，对外访问应通过平台的鉴权入口；仅需本机访问时可在 `config.json` 中将 `host` 改为 `127.0.0.1`。
