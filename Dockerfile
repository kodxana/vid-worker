FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TORCH_CUDA_ARCH_LIST="7.0 7.5 8.0 8.6 8.9 9.0+PTX"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    git \
    wget \
    ffmpeg \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Install Python packages
RUN python3 -m pip install --no-cache-dir --upgrade pip

# Install CUDA 12.4 specific packages
RUN pip3 install --no-cache-dir nvidia-cublas-cu12==12.4.5.8
ENV LD_LIBRARY_PATH=/opt/conda/lib/python3.8/site-packages/nvidia/cublas/lib/:$LD_LIBRARY_PATH

# Install PyTorch with CUDA support
RUN pip3 install --no-cache-dir \
    torch==2.2.0 \
    torchvision==0.17.0 \
    --index-url https://download.pytorch.org/whl/cu121

# Install flash-attention
RUN pip3 install --no-cache-dir \
    ninja \
    packaging \
    && pip3 install --no-cache-dir git+https://github.com/Dao-AILab/flash-attention.git@v2.6.3

# Install xDiT for parallel inference
RUN pip3 install --no-cache-dir xfuser==0.4.0

# Install other dependencies
COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

# Set working directory
WORKDIR /app

# Create model directory
RUN mkdir -p /app/ckpts

# Download model files
ENV MODEL_CACHE="ckpts"
ENV BASE_URL="https://weights.replicate.delivery/default/hunyuan-video/ckpts"

RUN cd /app/ckpts && \
    wget -O hunyuan-video-t2v-720p.tar "${BASE_URL}/hunyuan-video-t2v-720p.tar" && \
    tar xf hunyuan-video-t2v-720p.tar && \
    rm hunyuan-video-t2v-720p.tar && \
    wget -O text_encoder.tar "${BASE_URL}/text_encoder.tar" && \
    tar xf text_encoder.tar && \
    rm text_encoder.tar && \
    wget -O text_encoder_2.tar "${BASE_URL}/text_encoder_2.tar" && \
    tar xf text_encoder_2.tar && \
    rm text_encoder_2.tar

# Copy the rest of the application
COPY . /app

# Set environment variables for parallel inference
ENV TOKENIZERS_PARALLELISM=false
ENV CUDA_LAUNCH_BLOCKING=1
ENV NCCL_P2P_DISABLE=1
ENV NCCL_DEBUG=INFO

# Add RunPod handler requirements
RUN pip install --no-cache-dir runpod

# Default command
CMD [ "python", "-u", "/app/src/rp_handler.py" ] 