FROM python:3.11-slim
RUN pip install --no-cache-dir fastapi uvicorn httpx
COPY server.py /app/server.py
CMD ["uvicorn","server:app","--app-dir","/app","--host","0.0.0.0","--port","8080"]
