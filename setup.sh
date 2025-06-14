#!/bin/bash

# Nama project: GitPulse
# Jalankan di Linux

echo "📦 Menyiapkan virtual environment..."
python3 -m venv venv

echo "📂 Mengaktifkan virtual environment..."
source venv/bin/activate

echo "⬇️ Menginstall dependensi..."
pip install -r requirements.txt

echo "📁 Membuat folder output jika belum ada..."
mkdir -p output

echo "🚀 Menjalankan program GitPulse..."
python main.py

echo "✅ Selesai. Lihat hasil di output/last_commit.txt"