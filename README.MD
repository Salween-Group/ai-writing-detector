# AI Writing Detector

## What this skill does

This skill scores a piece of writing on a 0-100 scale for how AI-generated it sounds. 100 is human-sounding. It works through 24 specific AI writing patterns, flags every violation it finds, tallies the deductions, and gives the author a final score with actionable line-level fixes.

This is a diagnostic tool, not a rewriter. It identifies the problems and shows what to fix. 

Inspired by some code buried deep in here: https://github.com/ericosiu/ai-marketing-skills

An interesting way to use it, if you have a separate voice guideline file your LLM can reference, is to ask it to rewrite the piece of writing until the score is 90 or better.  

