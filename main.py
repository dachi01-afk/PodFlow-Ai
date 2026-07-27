#!/usr/bin/env python3
"""PodFlow AI - Autonomous Podcast Network"""

import sys
from crew import create_crew
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
    dashboard.start(topic)
    
    try:
        crew = create_crew(topic)
        result = crew.kickoff(inputs={"topic": topic})
        
        print("\n" + "="*60)
        print("PIPELINE COMPLETED!")
        print("="*60)
        print(result)
        
        dashboard.finish()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
