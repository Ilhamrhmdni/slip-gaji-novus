#!/bin/bash
# Instal wkhtmltopdf
apt-get update && apt-get install -y wkhtmltopdf

# Instal dependensi tambahan jika diperlukan
apt-get install -y xvfb libfontconfig1 libxrender1

# Instal requirements Python
pip install -r requirements.txt
