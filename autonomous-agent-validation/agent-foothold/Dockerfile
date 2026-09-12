FROM python:3.11-slim
RUN pip install --no-cache-dir pyjwt cryptography requests
COPY sa-token /var/run/secrets/kubernetes.io/serviceaccount/token
CMD ["sleep","infinity"]
