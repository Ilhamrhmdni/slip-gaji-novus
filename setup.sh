#!/bin/bash
# Instal wkhtmltopdf
apt-get update && apt-get install -y wkhtmltopdf

# Instal dependensi tambahan (penting untuk menjalankan wkhtmltopdf headless)
apt-get install -y xvfb libfontconfig1 libxrender1 libssl1.1

# Instal library Python dari requirements.txt
pip install -r requirements.txt
