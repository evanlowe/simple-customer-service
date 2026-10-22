FROM agentkit-prod-public-cn-beijing.cr.volces.com/base/py-simple:python3.12-bookworm-slim-latest

WORKDIR /app
COPY requirements.txt ./
RUN uv pip install --system --default-index https://mirrors.aliyun.com/pypi/simple/ \
    -r requirements.txt \
    "https://files.pythonhosted.org/packages/27/bb/15257acbae782be1b3bee6a8a9072ecdf75ca58f5adf0d8f833a052191e5/agentkit_sdk_python-0.9.1-py3-none-any.whl#sha256=3efac69969308366795661f42b737204873b591ba2cd39b36bdb7e7a86c0cafc"
COPY app.py config.example.json faq.md ./
EXPOSE 8000
CMD ["python", "app.py"]
