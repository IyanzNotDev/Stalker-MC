# Minecraft Stalker API

API sederhana untuk mencari informasi akun Minecraft berdasarkan username.
Dibuat dengan Flask, di-deploy ke Render.

---

## Creator

Iyann Nak MBG
Telegram: t.me/IyanAlfarez

---

## Struktur File

minecraft-stalker-api/
├── server.py          # Main server (register blueprint)
├── stalker.py         # Endpoint Minecraft Stalker (blueprint)
├── requirements.txt   # Dependencies Python
├── render.yaml        # Konfigurasi deploy ke Render
└── README.md          # Dokumentasi ini

---

## Penjelasan File

| File | Fungsi |
|------|--------|
| server.py | File utama. Menjalankan Flask server, register blueprint dari stalker.py, dan menyediakan endpoint root (/) serta status (/api/status). |
| stalker.py | Berisi semua logic endpoint Minecraft: stalk user, UUID to username, dan batch stalk. Dipisah biar rapi (blueprint). |
| requirements.txt | Daftar library Python yang dibutuhkan: Flask, CORS, Requests, Gunicorn. |
| render.yaml | Konfigurasi untuk deploy otomatis ke Render.com (free tier). |
| README.md | Dokumentasi ini. |


---
