#!/bin/bash
source ./bin/activate
export REDIS_URL=redis://localhost:6379
export SLACK_API_TOKEN=irOXdHlJ0lIAwG5UGLOTdTTS
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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
export TRANSLATE_ENGINE=google
export GOOGLE_API_KEY=AIzaSyDjR8W6bKo54_yI0hazfTikTnMRNzaCmGs
python app.py
