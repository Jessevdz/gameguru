# Dockerfile for the streamlit frontend

FROM --platform=linux/amd64 python
WORKDIR /home
COPY *.py /home
COPY pages/add.py /home/pages/add.py
COPY *.txt /home
RUN pip install -r frontend_requirements.txt
CMD streamlit run ask.py --server.port=8501 --server.address=0.0.0.0