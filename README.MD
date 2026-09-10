# AI Writing Detector

## What this skill does

This skill scores a piece of writing on a 0-100 scale for how AI-generated it sounds. 100 is human-sounding. It auto-detects the content type (blog post, LinkedIn post, email, Slack message), works through 45+ AI writing patterns plus channel-specific extras and a banned vocabulary list, applies false-positive guards so genuinely human quirks aren't punished, tallies the capped deductions, and gives the author a final score with actionable line-level fixes.

This is a diagnostic tool, not a rewriter. It identifies the problems and shows what to fix.

## Credits

- Inspired by some code buried deep in here: https://github.com/ericosiu/ai-marketing-skills
- Patterns #35-39, several banned words and filler phrases, the false-positive guards, and the self-check step (v2.1.0) were informed by Peter Yang's [no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT). Descriptions are written in our own voice.
