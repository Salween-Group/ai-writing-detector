---
name: ai-writing-detector
description: "Score any piece of writing on a 0-100 scale for how AI-generated it sounds (0 = obviously AI, 100 = indistinguishable from human). Auto-detects content type (blog post, LinkedIn post, email, Slack message) and applies channel-specific AI pattern detection on top of 40+ universal patterns and a banned vocabulary list. Use this skill whenever the user asks for an AI test, AI writing test, AI voice score, humanizer score, humanizer check, AI detection score, AI writing score, writing authenticity check, 'does this sound like AI', 'how human does this sound', 'check for AI patterns', 'score this draft', 'run the humanizer', 'AI detector', or any request to evaluate whether text reads as machine-generated versus human-written. Also trigger when the user pastes text and asks 'is this AI?', 'would this pass AI detection?', or 'how robotic does this sound?'. Do NOT use for rewriting or humanizing text — this skill only scores and diagnoses."
---

# AI Writing Detector v2

## What this skill does

You score a piece of writing on a 0-100 scale for how AI-generated it sounds. You auto-detect the content type, run through 40+ AI writing patterns (universal + channel-specific), check an expanded banned vocabulary list, assess originality, and deliver a single score with a detailed diagnostic report.

This is a diagnostic tool, not a rewriter. You identify the problems and show what to fix. The author does the rewriting.

## How to get the text

The user might:
- Paste text directly in the chat
- Reference a file path (read it)
- Point to a URL (fetch it)
- Reference a document created earlier in the conversation

If it's not clear what text to score, ask.

---

## Step 0: Auto-detect content type

Before scoring, classify the content. State your detection at the top of your report.

**Email** — Look for: subject lines, "To:"/"From:" headers, greeting formulas ("Hi [Name]", "Dear [Name]"), formal sign-offs ("Best", "Regards", "Thanks" + name), explicit ask + sign-off structure, "Following up on", "Per our conversation".

**LinkedIn** — Look for: one-sentence-per-line formatting, hashtags, engagement CTAs at the end ("Thoughts?", "Agree?"), @mentions, under 3,000 characters with no headings, emoji as section markers, story-hook openings.

**Slack** — Look for: channel references (#channel-name), @here/@channel mentions, thread-style short messages, very casual tone with no greeting or sign-off, under 500 characters, emoji shortcodes (:thumbsup:).

**Blog post** — Look for: headings/subheadings, more than 3,000 characters of structured prose, multiple developed paragraphs, meta-commentary ("In this article", "Key takeaways"), SEO-style structure.

If ambiguous, default to **blog post** and note it.

---

## Scoring method

Start at 100. Deduct points across seven scoring categories. Multiple occurrences of the same pattern stack up to 2x the base penalty (so a -10 pattern found 3+ times caps at -20 total for that pattern).

### Category deduction caps

Each category has a maximum total deduction. Once hit, stop counting deductions but still flag every violation — the author needs the full picture. Mark capped categories with "(CAP REACHED)" in the summary table.

| Category | What it covers | Max deduction |
|---|---|---|
| **Banned vocabulary** | Banned word list | -15 |
| **Content patterns** | #1-6, #25-34 | -20 |
| **Language & grammar** | #7-12 | -15 |
| **Style patterns** | #13-18 | -10 |
| **Communication patterns** | #19-21 | -15 |
| **Filler & hedging** | #22-24 | -10 |
| **Channel-specific patterns** | LinkedIn/Email/Slack extras | -5 |
| **Originality** | "Only I could write this" check | -5 |

Worst possible score: **100 - 15 - 20 - 15 - 10 - 15 - 10 - 5 - 5 = 5, floored to 0**. In practice, text that saturates every cap lands around 5. Text with problems in two or three categories but clean elsewhere lands in the 40-70 diagnostic sweet spot. Text with problems in two or three categories lands in the 40-70 diagnostic sweet spot.

### Severity override

When raw deductions (before caps) exceed **150 points**, the text is so saturated with AI patterns that caps alone understate the severity. In this case, apply a -10 penalty on top of the capped total. This prevents a text with 25+ banned words and 10+ pattern violations from scoring above 25.

### Score ranges
- **90-100**: Human-sounding. Clean.
- **70-89**: Minor AI tells. Quick fixes needed.
- **50-69**: Obvious AI patterns. Significant rewrite needed.
- **30-49**: Heavy AI patterns. Major rewrite.
- **0-29**: Reads like raw ChatGPT output. Full rewrite.

---

## Step 1: Banned vocabulary scan

Each occurrence costs **-5 points** (subject to the -15 category cap).

**The banned list:**
delve, tapestry, landscape (abstract use), leverage, multifaceted, nuanced, pivotal, realm, robust, seamless, testament, transformative, underscore (as verb), utilize, whilst, keen, embark, comprehensive, intricate, commendable, meticulous, paramount, groundbreaking, innovative, cutting-edge, synergy, holistic, paradigm, ecosystem, Additionally, align with, crucial, enduring, enhance, fostering, garner, highlight (as verb), interplay, intricacies, showcase, vibrant, valuable, profound, renowned, breathtaking, nestled, stunning, foster, cultivate, facilitate, elevate, essentially, certainly, overall (as filler qualifier), absolutely (as affirmation opener), typically, various (as vague pluralizer), superpower, journey (figurative), albeit

**Context-sensitive entries:**
- "Landscape" and "highlight" only count when used figuratively ("the marketing landscape" is banned; "the desert landscape" is fine)
- "Underscore" only counts as a verb ("underscores the importance"), not the character
- "Journey" only counts as figurative ("our leadership journey"), not literal travel
- "Overall" only counts as a filler qualifier ("Overall, this approach works"), not in data contexts ("overall revenue")
- "Absolutely" only counts as an affirmation opener ("Absolutely, here's how"), not as a genuine intensifier with specific evidence

Report banned words as a simple list with counts before moving to pattern analysis.

---

## Step 2: The pattern check

Work through each pattern. For every violation found, quote the offending text and state the deduction. Skip patterns that don't apply — don't pad the report with "no issues found" for clean patterns.

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
Multiple banned words appearing in the same paragraph. The clustering itself is the tell — even if individual words might pass, grouping them screams AI.
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
Emojis on headings or bullet points as visual flair rather than semantic content.
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
"In order to" (just say "To"), "Due to the fact that" (say "Because"), "At this point in time" (say "Now"), "It is important to note that" (just state it), "In today's [noun]" (just start with the point), "When it comes to" (cut it), "At the end of the day" (cut it), "The truth is" (just state the claim).
> Fix direction: Compress or delete.

**23. Excessive Hedging** (-8)
"Could potentially possibly", "might have some effect", "it could be argued that", "I was wondering if perhaps", "One might argue".
> Fix direction: Commit to the claim or cut it.

**24. Generic Positive Conclusions** (-10)
"The future looks bright", "Exciting times lie ahead", "continues their journey toward excellence", "And we're just getting started".
> Fix direction: End with a specific fact, open question, or concrete next step.

---

## Step 2b: Expanded structural patterns

These additional structural markers apply to all content types. Each costs **-5 points** and counts toward the **content patterns** or **language & grammar** cap (whichever is more relevant to the specific violation).

**25. Credential Stacking Opener** (-5)
Opening with 2-3 credential statements before making any point. "As a 15-year veteran of... who has worked with... and spoken at..."
> Fix direction: Weave credentials into the argument where they earn context, or skip them.

**26. Stat Bomb Opener** (-5)
Rapid-fire sequence of 3+ short statistical fragments at the top. "$2.3B market. 47% growth. 12M users."
> Fix direction: Weave stats into real sentences with context.

**27. Honesty Disclaimer** (-5)
"And I'll be honest:", "I'll be real:", "Can I be candid?" before a non-controversial claim.
> Fix direction: Just state the opinion. Real honesty doesn't announce itself.

**28. Punchy Orphan Closer** (-5)
Ending with a standalone short sentence designed as a mic-drop. "That's the whole game." "Full stop."
> Fix direction: Fold the thought into the final paragraph or close with a real observation.

**29. Tension-Colon Opener** (-5)
Opening with a colon-separated tension statement. "The problem with marketing today: nobody reads."
> Fix direction: State the observation as a normal sentence.

**30. Fake Candor Parentheticals** (-5)
Multiple parenthetical asides to simulate conversational tone. One is fine. Three or more in a short piece signals performative writing.
> Fix direction: Remove most parentheticals. Keep one if it genuinely adds an aside.

**31. Standalone Hype Fragment** (-5)
"This is big." or "Game changer." as its own sentence or paragraph.
> Fix direction: Replace with a specific claim about what changed and for whom.

**32. Self-Posed Question Transition** (-5)
"Why? Because..." or "How? Simple:" as a transition between paragraphs.
> Fix direction: Rewrite as a declarative statement.

**33. Reading Complexity Creep** (-5)
Clusters of multi-syllable vocabulary and nested dependent clauses that push reading level above 10th grade in conversational content. Three or more 3+ syllable words in one sentence, or sentences with 2+ embedded dependent clauses.
> Fix direction: Shorter words, shorter sentences. Aim for 7th-9th grade reading level in professional content.

**34. Runway Sentences** (-5)
Vague hype lines before the actual specific detail. "We're thrilled to announce something we've been working on for months:" — just say what it is.
> Fix direction: Cut the runway, start with the substance.

---

## Step 2c: Channel-specific patterns

Apply these **only** for the detected content type. Each costs **-5 points** toward the **channel-specific** cap (-10 max).

### LinkedIn-specific patterns

**L1. One-Line Paragraph Formatting** (-5)
Every sentence sits on its own line with a blank line between. This is the most recognizable AI/ghostwriter tell on LinkedIn.
> Fix direction: Group related sentences into real paragraphs (2-4 sentences each).

**L2. Engagement Bait Closers** (-5)
"Agree?", "Thoughts?", "What would you add?", "Drop a comment if...", "Repost if this resonates". If the post is worth engaging with, people will.
> Fix direction: Delete entirely. Or end with a genuine open question specific to the post's topic.

**L3. ALL-CAPS Word Injection** (-5)
Capitalizing individual words mid-sentence to simulate spoken intensity: "We've onboarded HUNDREDS of customers." "A VERY exciting email."
> Fix direction: Use the actual number or specific detail instead of a shouted word.

**L4. Information-Withheld Hook** (-5)
Opening 1-2 sentences that deliberately hide the subject to force the "see more" click. "At Netflix, we had 1 UNSPOKEN rule. It was about this 1 word." The reader can't tell what the post is about.
> Fix direction: Open with the actual insight. State what the rule is, then explain why it mattered.

**L5. Achievement Post Formula** (-5)
The 4-beat template: (1) emotion word + announcement, (2) team thanks, (3) generic lesson, (4) emoji sign-off. "Thrilled to announce [X]! 🎉 Couldn't have done it without my team. Biggest lesson: consistency wins. Excited for what's next! 🚀"
> Fix direction: Tell one specific story about what made this hard, surprising, or worth sharing.

**L6. Fake Dialogue Format** (-5)
Framing an opinion as a fabricated conversation between roles (CEO/CMO, Founder/Investor). "CEO: Why do we separate brand and performance? CMO: Because they're different things."
> Fix direction: State your argument directly. If you overheard or participated in an actual conversation, say so.

**L7. Period-Separated Emphasis** (-5)
"every. single. day." or "This. Is. The. Moment." to simulate spoken intensity.
> Fix direction: Use normal sentence rhythm. Earn emphasis through specificity.

**L8. Contrast Upgrade Formula** (-5)
"X is [positive]. [X variant] is a whole different game." Template that sounds punchy but is recycled endlessly.
> Fix direction: Collapse into a single sentence about the actual challenge.

**L9. Cliché Proverb Opener** (-5)
Starting with a well-worn business maxim: "Work smarter, not harder." "Culture eats strategy for breakfast."
> Fix direction: Replace with the specific observation or experience that prompted the post.

**L10. Permission Phrases** (-5)
"Read that again." or "Let that sink in." dropped after an unremarkable observation to manufacture gravity.
> Fix direction: Cut. If the observation is strong, it doesn't need permission to land.

### Email-specific patterns

**E1. AI Greeting Formulas** (-5)
"I hope this email finds you well", "I trust this message finds you in good spirits", "Hope you had a great weekend" (when the sender doesn't know the recipient).
> Fix direction: Skip the greeting filler. Start with the point, or use a simple "Hi [Name]".

**E2. AI Closing Stacks** (-5)
"Please don't hesitate to reach out", "I look forward to hearing from you", "Thank you for your time and consideration". Especially when stacked together.
> Fix direction: One sign-off. "Thanks, [Name]" is fine.

**E3. Buried Ask** (-5)
The actual request is in the third or fourth paragraph after extensive context.
> Fix direction: Lead with the ask. Provide context after.

**E4. Fake Personalization** (-5)
"I noticed your company is doing great things in [industry]", "I was impressed by your recent [post/talk]" without citing anything specific.
> Fix direction: Either cite the specific thing (title, date, what you noticed) or delete the flattery.

**E5. Vague CTA** (-5)
"Let me know if you'd like to chat sometime" instead of "Free Tuesday at 2pm?"
> Fix direction: Make the ask specific and easy to say yes to.

**E6. Subject Line AI Patterns** (-5)
"Quick question", "Checking in", "A thought", "[First name], quick thought" — generic subjects that could apply to any email.
> Fix direction: Make the subject specific to the email's content.

### Slack-specific patterns

**S1. Over-Formal for Slack** (-5)
"I wanted to reach out regarding...", "Please be advised that...", "At your earliest convenience" in a Slack message.
> Fix direction: Write like you talk. Slack is casual.

**S2. Too Long for the Medium** (-5)
More than 5-6 sentences in a single Slack message without a TL;DR.
> Fix direction: If it needs that many words, it should be an email, a doc, or a thread with a summary at the top.

**S3. Formal Structure in Slack** (-5)
Using greeting + body + sign-off format ("Hi team, ... Best, [Name]") in Slack.
> Fix direction: Just say the thing. No greeting or sign-off needed.

---

## Step 3: Originality check

This is a separate assessment from pattern detection. A text can be pattern-clean but still obviously AI-generated if it says nothing specific. Score originality as a **-0 to -5 deduction** from the originality cap.

Ask yourself:
- Could anyone with a search engine have written this? (-2)
- Is there zero firsthand experience, specific evidence, or named examples? (-2)
- Are the examples generic rather than drawn from specific experience? (-1)

Deduct the total (max -5) and note what's missing. If the text has genuine specifics, earned perspective, or clear domain expertise, deduct nothing.

---

## Step 4: Deliver the report

Structure your output exactly like this:

---

### AI Writing Score: [X]/100

**Detected as:** [Blog Post / LinkedIn Post / Email / Slack Message]

**Verdict:** [One of: "Human-sounding", "Minor AI tells", "Obvious AI patterns", "Heavy AI patterns", "Reads like ChatGPT"]

**Banned words found:** [count]
[list each word and its count, or "None"]

**Patterns flagged:**

[For each flagged pattern, use this format:]

**[Pattern name]** (-[points]) — [occurrence count]x
> "[quoted offending text]"
Suggested fix: [specific rewrite direction for this instance]

[Repeat for each flagged pattern. Skip clean patterns entirely.]

**Originality assessment:**
[1-2 sentences on whether the content has genuine specificity and earned perspective, or reads like anyone could have written it. State the deduction.]

**Deduction summary:**
| Category | Raw deductions | Capped deduction |
|---|---|---|
| Banned vocabulary | -X | -X |
| Content patterns (#1-6, #25-34) | -X | -X (CAP REACHED) |
| Language & grammar (#7-12) | -X | -X |
| Style patterns (#13-18) | -X | -X |
| Communication patterns (#19-21) | -X | -X |
| Filler & hedging (#22-24) | -X | -X |
| Channel-specific patterns | -X | -X |
| Originality | -X | -X |
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
- A point of view only this author could have (earned through experience, not borrowed from conventional wisdom)
