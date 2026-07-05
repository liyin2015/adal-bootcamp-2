# Container image for the AdaL Support Agent BFF proxy: serves the site (site/)
# and proxies /api/* to AdaL Cloud with the Clerk JWT injected server-side.
#
# Build context is the example root (support-agent-cloud/) so the image can
# bundle proxy/, site/, and agent/ together:
#   docker build -f proxy/Dockerfile -t support-proxy .
FROM python:3.11-slim

WORKDIR /app

# Install proxy deps first (layer cache).
COPY proxy/requirements.txt ./proxy/requirements.txt
RUN pip install --no-cache-dir -r proxy/requirements.txt

# Bundle the proxy server, the static site, and the agent config.
COPY proxy/server.py ./proxy/server.py
COPY site/ ./site/
COPY agent/ ./agent/

# App Runner / ALB health checks and traffic hit 8080.
ENV HOST=0.0.0.0 PORT=8080
EXPOSE 8080

# ADAL_JWT must be provided at runtime (env var / secret) — never baked in.
WORKDIR /app/proxy
CMD ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
