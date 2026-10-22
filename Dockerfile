FROM agentkit-prod-public-cn-beijing.cr.volces.com/base/py-simple:python3.12-bookworm-slim-latest

WORKDIR /app
COPY requirements.txt ./
RUN uv pip install --system --default-index https://pypi.org/simple -r requirements.txt
COPY app.py config.example.json faq.md ./
EXPOSE 8000
CMD ["python", "app.py"]
