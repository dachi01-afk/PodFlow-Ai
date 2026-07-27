#!/usr/bin/env python3
"""PodFlow AI - Autonomous Podcast Network"""

import sys
import json
from pipeline import PipelineOrchestrator
from dashboard import CLIDashboard
from data import TOPICS


def get_user_topic():
    """Get topic from user selection or input."""
    print("\n🎙️  PODFLOW AI - Select Topic\n")
    print("Available trending topics:")
    for i, topic in enumerate(TOPICS['topics'], 1):
        print(f"  {i}. {topic['keyword']}")
    
    print(f"\n  Or enter your own topic below:")
    choice = input("\nYour choice (1-3 or custom topic): ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(TOPICS['topics']):
        return TOPICS['topics'][int(choice) - 1]['keyword']
    else:
        return choice


def main():
    topic = get_user_topic()
    
    if not topic:
        print("No topic selected. Exiting.")
        sys.exit(1)
    
    dashboard = CLIDashboard()
    pipeline = PipelineOrchestrator(status_callback=dashboard.update_status)
    
    dashboard.start(topic)
    
    try:
        results = pipeline.run(topic)
        
        print("\n" + "="*60)
        print("OUTPUT FILES:")
        print(f"  Audio: {results.get('audio_path', 'N/A')}")
        print(f"  Metadata: {results.get('metadata', {}).get('_file_path', 'output/metadata/')}")
        print(f"  Social: {results.get('social', {}).get('_file_path', 'output/social/')}")
        print("="*60)
        
        print("\nPROMPT ARCHITECTURE:")
        print("  See docs/prompt_architecture.md for details")
        
        dashboard.finish()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
