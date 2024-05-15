#!/usr/bin/env bash

alembic upgrade head
python -O src/main.py
