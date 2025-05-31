#!/bin/bash

# Instal dependensi
apt-get update && apt-get install -y \
    libfontconfig1 \
    libxrender1 \
    libx11-dev \
    xfonts-75dpi \
    xfonts-base

# Download dan instal wkhtmltopdf secara manual
curl -LO https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb 
dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb || true

# Instal dependensi yang hilang (jika ada)
apt-get install -f -y

# Instal library Python
pip install -r requirements.txt
