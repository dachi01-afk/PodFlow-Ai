from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from typing import List, Dict


def generate_rss_feed(channel_name: str, episodes: List[Dict]) -> str:
    """Generate RSS feed XML for podcast"""

    rss = Element("rss", version="2.0")
    rss.set("xmlns:itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
    rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")

    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = channel_name or "PodFlow"
    SubElement(channel, "description").text = f"Podcast by {channel_name or 'PodFlow'}"
    SubElement(channel, "language").text = "id"
    SubElement(channel, "itunes:author").text = channel_name or "PodFlow"

    for episode in episodes:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = episode.get("title") or "Untitled"
        SubElement(item, "description").text = episode.get("description") or ""
        SubElement(item, "enclosure", {
            "url": episode.get("audio_url") or "",
            "type": "audio/mpeg",
            "length": str(episode.get("audio_length") or 0),
        })
        SubElement(item, "pubDate").text = episode.get("published_at") or ""
        SubElement(item, "itunes:duration").text = episode.get("duration") or "00:00"

    xml_string = tostring(rss, encoding="unicode", method="xml")
    return parseString(xml_string).toprettyxml(indent="  ")
