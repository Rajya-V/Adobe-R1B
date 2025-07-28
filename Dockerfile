FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt

# Copy the pre-downloaded model cache into the Hugging Face cache location inside the container
COPY model_cache/models--sentence-transformers--all-MiniLM-L6-v2 /root/.cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2

COPY . .

CMD ["python", "run.py"]