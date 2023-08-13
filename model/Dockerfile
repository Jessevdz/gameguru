# Dockerfile for containers running the LLAMA model and model API.

# LLAMA models need GPU for inference
FROM --platform=amd64 nvidia/cuda:12.2.0-devel-ubuntu20.04
WORKDIR /home
# Install git
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install git -y
# Install python
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
# Clone the llama repo
RUN git clone https://github.com/facebookresearch/llama.git llama
# Install python requirements
COPY model_requirements.txt /home
RUN pip install -r model_requirements.txt
# Install llama requirements
WORKDIR /home/llama
RUN pip install -e .
# Copy code
WORKDIR /home
COPY *.py /home
# Start FastAPI
CMD uvicorn model_api:app --reload --host 0.0.0.0