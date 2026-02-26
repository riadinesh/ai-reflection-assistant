#!/bin/bash
cd /Users/riadinesh/Desktop/Projects/ai-reflection-assistant/backend
/Users/riadinesh/Desktop/Projects/ai-reflection-assistant/backend/venv/bin/python -m app.summarize >> /tmp/reflections.log 2>> /tmp/reflections-error.log
