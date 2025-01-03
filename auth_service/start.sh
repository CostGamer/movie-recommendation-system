#!/bin/bash

export $(grep -v '^#' .env | xargs)
uvicorn --factory app.main:setup_app --host ${UVICORN_HOST} --port ${UVICORN_PORT} --reload
