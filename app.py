# Copyright 2026 simple-customer-service contributors
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path

from agentkit.apps import AgentkitAgentServerApp
from veadk import Agent
from veadk.memory.short_term_memory import ShortTermMemory

ROOT = Path(__file__).resolve().parent


def create_app(config: dict) -> AgentkitAgentServerApp:
    agent = Agent(
        name="customer_service",
        description="一个简单的中文智能客服",
        instruction=(
            "你是友好、简洁的中文客服。根据以下示例 FAQ 回答问题。"
            "这些是演示政策，不代表任何真实商家。"
            "缺少信息时先询问；FAQ 未涵盖的问题说明需要咨询人工客服。"
            "你没有订单查询、退款或联系人工的工具，"
            "不得声称已经执行这些操作，不索取密码或验证码。\n\n"
            + (ROOT / "faq.md").read_text(encoding="utf-8")
        ),
        model_provider="openai",
        model_name=config["model_name"],
        model_api_base=config["model_api_base"],
        model_api_key=config["model_api_key"],
        tools=[],
    )
    return AgentkitAgentServerApp(
        agent=agent,
        short_term_memory=ShortTermMemory(backend="local"),
    )


if __name__ == "__main__":
    config_path = ROOT / "config.json"
    if not config_path.exists():
        raise SystemExit("请复制 config.example.json 为 config.json，填写模型和 API Key。")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not config.get("model_api_key", "").strip():
        raise SystemExit("请在 config.json 中填写 model_api_key。")
    create_app(config).run(host=config["host"], port=config["port"])
