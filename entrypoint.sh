#!/bin/sh
sleep 10
python create_users.py
uvicorn app.main:app --host 0.0.0.0 --port 8000