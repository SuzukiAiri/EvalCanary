FROM python:3.11-slim
RUN pip install --no-cache-dir fastapi uvicorn docker
COPY controller.py /app/controller.py
CMD ["uvicorn","controller:app","--app-dir","/app","--host","0.0.0.0","--port","8090"]
