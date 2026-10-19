---
name: youtube-agent-skill
description: Get the transcript of a YouTube video and turn it into a summary, key points, notes, or answers to questions about the video. Use this whenever the user shares a YouTube link (youtube.com or youtu.be) or asks to summarize, explain, take notes from, or ask questions about a YouTube video, even if they do not say the word "transcript".
---

# YouTube Agent Skill

Fetches a video's captions with a small script, then works from that text.

## Workflow

1. Take the YouTube URL (or 11-character video ID) from the user.
2. Install the dependency if needed: `pip install youtube-transcript-api --break-system-packages`
3. Run: `python scripts/get_transcript.py "<url>" [--lang hi,en]`
   - Output is plain text, one line per caption chunk, with `[mm:ss]` timestamps.
   - `--lang` is an optional comma-separated list of preferred languages (default: `en,hi`).
4. Do what the user asked using only that text: summary, key points, notes, or Q&A.

## Output defaults

If the user gives no instruction, reply with: a 2-3 line overview, 5-8 key points with timestamps, and any steps or action items mentioned.
Reply in the language the user wrote in.

## When it fails

- If the script says captions are disabled or unavailable, tell the user plainly. Do not guess the video's content from its title.
- If the network blocks YouTube (the environment may restrict domains), tell the user, and ask them to paste the transcript text instead.
- Very long transcripts: summarize in sections, then combine.
