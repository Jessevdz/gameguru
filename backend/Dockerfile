# Dockerfile for the backend service orchestration

FROM --platform=linux/amd64 python
WORKDIR /home
COPY *.py /home
COPY *.txt /home
RUN pip install -r backend_requirements.txt
# Download the sentence transformer model during build instead of container startup
RUN python -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("thenlper/gte-large")'
CMD uvicorn backend_api:app --reload --host 0.0.0.0