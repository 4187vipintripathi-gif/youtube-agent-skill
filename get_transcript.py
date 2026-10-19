#!/usr/bin/env python3
"""Print a YouTube video's transcript with [mm:ss] timestamps."""
import argparse
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi


def video_id(url_or_id: str) -> str:
    s = url_or_id.strip()
    if re.fullmatch(r"[\w-]{11}", s):
        return s
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/|/live/)([\w-]{11})", s)
    if not m:
        sys.exit("Could not find a video ID in: " + url_or_id)
    return m.group(1)


def fmt(seconds: float) -> str:
    seconds = int(seconds)
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--lang", default="en,hi", help="comma-separated, in order of preference")
    args = p.parse_args()

    vid = video_id(args.url)
    langs = [x.strip() for x in args.lang.split(",") if x.strip()]

    try:
        if hasattr(YouTubeTranscriptApi, "get_transcript"):  # older versions
            items = YouTubeTranscriptApi.get_transcript(vid, languages=langs)
            rows = [(i["start"], i["text"]) for i in items]
        else:  # v1.x
            fetched = YouTubeTranscriptApi().fetch(vid, languages=langs)
            rows = [(i.start, i.text) for i in fetched]
    except Exception as e:  # captions off, video private, network blocked, etc.
        sys.exit(f"Could not get transcript for {vid}: {type(e).__name__}: {e}")

    for start, text in rows:
        print(f"[{fmt(start)}] {text.replace(chr(10), ' ')}")


if __name__ == "__main__":
    main()
