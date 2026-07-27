import json
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DATA_DIR, "trending_topics.json"), "r") as f:
    TOPICS = json.load(f)
