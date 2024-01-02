# app/Dockerfile

#FROM python:3.9-slim
FROM continuumio/miniconda3

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/streamlit/streamlit-example.git .

#RUN pip3 install -r requirements.txt
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "glabtop2", "/bin/bash", "-c"]

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

#ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "glabtop2", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# # syntax=docker/dockerfile:1
# FROM continuumio/miniconda3

# WORKDIR /myapp

# # Create the environment:
# #COPY environment.yml .
# COPY . .
# RUN conda env create -f environment.yml

# # Make RUN commands use the new environment:
# SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# # Demonstrate the environment is activated:
# RUN echo "Make sure it works"
# RUN conda info

# # The code to run when container is started:
# #COPY run.py .
# ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "MAIN.py"]