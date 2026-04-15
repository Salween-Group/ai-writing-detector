---
name: ai-writing-detector
description: "Score any piece of writing on a 0-100 scale for how AI-generated it sounds (0 = obviously AI, 100 = indistinguishable from human), using 24 documented AI writing patterns from Wikipedia's detection guide plus a banned vocabulary list. Use this skill whenever the user asks for an AI test, AI writing test, AI voice score, humanizer score, humanizer check, AI detection score, AI writing score, writing authenticity check, 'does this sound like AI', 'how human does this sound', 'check for AI patterns', 'score this draft', 'run the humanizer', 'AI detector', or any request to evaluate whether text reads as machine-generated versus human-written. Also trigger when the user pastes text and asks 'is this AI?', 'would this pass AI detection?', or 'how robotic does this sound?'. Do NOT use for rewriting or humanizing text — this skill only scores and diagnoses."
---

# AI Writing Detector

## What this skill does

You score a piece of writing on a 0-100 scale for how AI-generated it sounds. You work through 24 specific AI writing patterns, flag every violation you find, tally the deductions, and give the author a final score with actionable line-level fixes.

This is a diagnostic tool, not a rewriter. You identify the problems and show what to fix. The author does the rewriting.


## How to get the text

The user might:
- Paste text directly in the chat
- Reference a file path (read it)
- Point to a URL (fetch it)
- Reference a document created earlier in the conversation

If it's not clear what text to score, ask.

## Scoring method

Start at 100. Deduct points for each pattern detected. Penalties are listed next to each pattern below. Multiple occurrences of the same pattern stack up to 2x the base penalty (so a -10 pattern found 3+ times caps at -20 total for that pattern).

### Category deduction caps

To keep the scoring scale meaningful across the full 0-100 range, each category has a maximum total deduction. Once a category hits its cap, stop counting further deductions in that category — but still flag every violation you find (the author needs to see them all). When a cap is reached, mark it in the deduction summary table with "(CAP REACHED)".

| Category | Patterns | Max deduction |
|---|---|---|
| **Banned vocabulary** | Banned word list | -15 |
| **Content patterns** | #1-6 (Significance Inflation through Formulaic Challenges) | -20 |
| **Language & grammar patterns** | #7-12 (AI Vocabulary Clustering through False Ranges) | -15 |
| **Style patterns** | #13-18 (Em Dash Overuse through Curly Quotes) | -10 |
| **Communication patterns** | #19-21 (Collaborative Artifacts through Sycophantic Tone) | -15 |
| **Filler & hedging** | #22-24 (Filler Phrases through Generic Conclusions) | -10 |

This means the absolute worst possible score is **100 - 15 - 20 - 15 - 10 - 15 - 10 = 15**. A text that trips every category cap lands around 15. A text with real problems in two or three categories but clean elsewhere will land in the 40-70 range — which is the diagnostic sweet spot.

### Score ranges
- **90-100**: Human-sounding. Clean.
- **70-89**: Minor AI tells. Quick fixes needed.
- **50-69**: Obvious AI patterns. Significant rewrite needed.
- **30-49**: Heavy AI patterns. Major rewrite.
- **0-29**: Reads like raw ChatGPT output. Full rewrite.

## Step 1: Banned vocabulary scan

Check the text for every word on this list. Each occurrence is an instant **-5 points**.

**The banned list:**
delve, tapestry, landscape (abstract use), leverage, multifaceted, nuanced, pivotal, realm, robust, seamless, testament, transformative, underscore (as verb), utilize, whilst, keen, embark, comprehensive, intricate, commendable, meticulous, paramount, groundbreaking, innovative, cutting-edge, synergy, holistic, paradigm, ecosystem, Additionally, align with, crucial, enduring, enhance, fostering, garner, highlight (as verb), interplay, intricacies, showcase, vibrant, valuable, profound, renowned, breathtaking, nestled, stunning

"Landscape" and "highlight" only count when used figuratively (e.g. "the marketing landscape" is banned; "the desert landscape" is fine). "Underscore" only counts as a verb ("underscores the importance"), not a character.

Report banned words as a simple list with counts before moving to pattern analysis.

## Step 2: The 24 pattern check

Work through each pattern. For every violation found, quote the offending text and state the deduction. Skip patterns that don't apply — don't pad the report with "no issues found" for every clean pattern.

### CONTENT PATTERNS

**1. Significance Inflation** (-10)
Puffing up importance: "stands as", "is a testament", "pivotal moment", "underscores its importance", "reflects broader", "setting the stage for", "indelible mark", "deeply rooted".
> Fix direction: Replace inflated framing with the specific fact. What actually happened?

**2. Undue Notability Claims** (-5)
Listing media mentions without context. "Active social media presence", "leading expert" without evidence.
> Fix direction: Either add the specific claim from the source, or cut.

**3. Superficial -ing Analyses** (-8)
Tacking "-ing" participial phrases for fake depth: "highlighting", "underscoring", "emphasizing", "ensuring", "reflecting", "symbolizing", "contributing to", "fostering", "showcasing".
> Fix direction: End the sentence before the -ing phrase. Start a new sentence with the actual point.

**4. Promotional Language** (-8)
"Boasts a", "vibrant", "rich" (figurative), "profound", "exemplifies", "commitment to", "natural beauty", "nestled", "in the heart of", "must-visit".
> Fix direction: Replace with a concrete fact or number.

**5. Vague Attributions** (-8)
"Industry reports", "Experts argue", "Some critics argue", "several sources". No specific citations.
> Fix direction: Name the source, date, and finding — or cut the claim.

**6. Formulaic "Challenges and Future" Sections** (-10)
"Despite its X, faces challenges...", "Despite these challenges, continues to Y", "Future Outlook" as a section header.
> Fix direction: State the specific challenge and what was done about it.

### LANGUAGE AND GRAMMAR PATTERNS

**7. AI Vocabulary Clustering** (-10)
Multiple banned words appearing in the same paragraph. The clustering itself is the tell — even if individual words might pass, grouping them together screams AI.
> Fix direction: Rewrite the paragraph in plain language.

**8. Copula Avoidance** (-5)
Using "serves as", "stands as", "marks", "represents", "boasts", "features", "offers" instead of simple "is", "are", or "has".
> Fix direction: Use "is" or "has". Simple verbs.

**9. Negative Parallelisms** (-5)
"Not only...but...", "It's not just about X, it's Y", "It's not merely X, it's Y".
> Fix direction: Just state the positive claim directly.

**10. Rule of Three Overuse** (-8)
Forcing ideas into groups of three. Triple adjectives, triple nouns, triple parallel clauses.
> Fix direction: Use two things, or four, or one. Break the pattern.

**11. Elegant Variation / Synonym Cycling** (-5)
Excessive synonym substitution to avoid repeating a word. "The CEO... The business leader... The company head..."
> Fix direction: Just use the same word again. Repetition is fine.

**12. False Ranges** (-5)
"From X to Y" where X and Y aren't on a meaningful scale.
> Fix direction: List the items plainly or pick the one that matters most.

### STYLE PATTERNS

**13. Em Dash Overuse** (-5)
More than 1 em dash per 200 words.
> Fix direction: Replace with commas, periods, or parentheses.

**14. Overuse of Boldface** (-3)
Mechanical bold emphasis on every key term.
> Fix direction: Remove most bold. Reserve it for one or two truly critical points.

**15. Inline-Header Vertical Lists** (-5)
Lists where every item starts with a **bolded header** + colon.
> Fix direction: Use plain bullets or convert to prose.

**16. Title Case in Headings** (-3)
Capitalizing All Main Words In Every Heading instead of sentence case.
> Fix direction: Use sentence case (only capitalize the first word and proper nouns).

**17. Emoji Decoration** (-5)
Emojis on headings or bullet points.
> Fix direction: Remove them.

**18. Curly Quotation Marks** (-2)
Using smart quotes instead of straight quotes (minor tell, but detectable).
> Fix direction: Replace with straight quotes if targeting plain text.

### COMMUNICATION PATTERNS

**19. Collaborative Artifacts** (-10)
"I hope this helps", "Of course!", "Certainly!", "Would you like...", "let me know", "here is a...".
> Fix direction: Delete. These are chatbot mannerisms, not writing.

**20. Knowledge-Cutoff Disclaimers** (-10)
"As of [date]", "While specific details are limited", "based on available information".
> Fix direction: Delete or replace with a specific date and source.

**21. Sycophantic Tone** (-8)
"Great question!", "You're absolutely right!", "That's an excellent point!"
> Fix direction: Delete. Respond to the substance, not the person.

### FILLER AND HEDGING

**22. Filler Phrases** (-5 each)
"In order to" (just say "To"), "Due to the fact that" (say "Because"), "At this point in time" (say "Now"), "It is important to note that" (just state it).
> Fix direction: Compress or delete.

**23. Excessive Hedging** (-8)
"Could potentially possibly", "might have some effect", "it could be argued that".
> Fix direction: Commit to the claim or cut it.

**24. Generic Positive Conclusions** (-10)
"The future looks bright", "Exciting times lie ahead", "continues their journey toward excellence".
> Fix direction: End with a specific fact, open question, or concrete next step.

## Step 3: Deliver the report

Structure your output exactly like this:

---

### AI Writing Score: [X]/100

**Verdict:** [One of: "Human-sounding", "Minor AI tells", "Obvious AI patterns", "Reads like ChatGPT"]

**Banned words found:** [count]
[list each word and its count, or "None"]

**Patterns flagged:**

[For each flagged pattern, use this format:]

**[Pattern name]** (-[points]) — [occurrence count]x
> "[quoted offending text]"
Suggested fix: [specific rewrite direction for this instance]

[Repeat for each flagged pattern. Skip clean patterns entirely.]

**Deduction summary:**
| Category | Raw deductions | Capped deduction |
|---|---|---|
| Banned vocabulary | -X | -X |
| Content patterns (#1-6) | -X | -X (CAP REACHED) |
| Language & grammar (#7-12) | -X | -X |
| Style patterns (#13-18) | -X | -X |
| Communication patterns (#19-21) | -X | -X |
| Filler & hedging (#22-24) | -X | -X |
| **Total** | **-X (raw)** | **-X (after caps)** |

Show both columns so the author sees the full severity even when caps apply. If a category wasn't flagged at all, omit it from the table.

**Top 3 fixes that would move the score the most:**
1. [Most impactful fix]
2. [Second most impactful]
3. [Third most impactful]

---

## What good human writing looks like (for calibration)

When scoring, remember what you're comparing against. Good human writing has:
- Opinions, not just reporting
- Varied sentence rhythm — short punches mixed with longer constructions
- Specific details over vague claims
- Simple verbs (is, has, does) over elaborate constructions
- Acknowledgment of uncertainty or mixed feelings (real uncertainty, not hedge-stacking)
- First-person perspective when appropriate
- Humor, edge, or personality
- Concrete examples with names, dates, numbers
