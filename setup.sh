#!/bin/bash
apt-get update && apt-get install -y wkhtmltopdf xvfb libfontconfig1 libxrender1
pip install -r requirements.txt
