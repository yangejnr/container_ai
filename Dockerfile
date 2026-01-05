FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY src/ ./src/

# FIXED: Removed --only-binary=all → installs requests!
#RUN pip install flask==3.0.3 gunicorn==22.0.0 numpy easyocr opencv-python-headless requests pillow

# ... same until pip ...
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install flask gunicorn numpy requests pillow \
    && pip install easyocr --no-cache-dir \
    && python -c "import easyocr; r = easyocr.Reader(['en']); print('Models OK!')" \
    && pip install opencv-python-headless
# ... rest same


EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.dashboard:app"]

