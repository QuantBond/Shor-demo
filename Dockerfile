# Base image with Python 3.9
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy the required files to the container
COPY simple_rsa.py /app/simple_rsa.py
COPY shor.py /app/shor.py
COPY Shor_demo.ipynb /app/Shor_demo.ipynb

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    numpy \
    sympy \
    qiskit \
    qiskit-aer \
    pycryptodome \
    notebook

# Expose the port for Jupyter Notebook
EXPOSE 8888

# Command to run Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

