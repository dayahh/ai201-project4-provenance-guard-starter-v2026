# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 45 attacks · 2026-11-04 00:05
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **45**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| CA01 | control_ai | baseline: unmodified AI text should be labelled AI | 200 | `47ce0e4ecbfb` | ai | 0.859 |  |
| CA02 | control_ai | baseline: unmodified AI text should be labelled AI | 200 | `848c45afa481` | ai | 0.856 |  |
| CH01 | control_human | baseline: lively human text should be labelled human | 200 | `7b609094cec2` | human | 0.276 |  |
| EV01 | evasion_typos | style signal: typos raise word variety so AI reads human | 200 | `025133b40d32` | ai | 0.700 |  |
| EV02 | evasion_typos | both signals: typos raise perplexity and word variety | 200 | `191f1c787d09` | unsure | 0.601 |  |
| EV03 | evasion_typos | model signal: heavy typos make the text unpredictable to gpt2 | 200 | `3c29d6095337` | ai | 0.652 |  |
| EV04 | evasion_casual | style signal: contractions and question marks inflate punctuation density | 200 | `33c958351f39` | unsure | 0.424 |  |
| EV05 | evasion_casual | style signal: an informal aside per sentence | 200 | `0dd422870da1` | unsure | 0.543 |  |
| SC01 | sentence_chop | style signal: mixing very short and long sentences raises length spread | 200 | `15485704f9cf` | unsure | 0.517 |  |
| SC02 | sentence_chop | style signal: one-word sentences between generated ones | 200 | `17d1f39d5307` | ai | 0.666 |  |
| PS01 | punctuation_stuffing | style signal: dashes, semicolons and parentheses inserted without changing words | 200 | `500af70fe3d5` | unsure | 0.372 |  |
| PS02 | punctuation_stuffing | style signal: question marks and exclamation marks on generated sentences | 200 | `7f42abcf89e0` | unsure | 0.507 |  |
| QP01 | quote_padding | both signals: a pasted human quotation dilutes the AI paragraph | 200 | `904e041fceff` | unsure | 0.479 |  |
| QP02 | quote_padding | model signal: a long rare-word quotation raises perplexity | 200 | `9293b65580c1` | unsure | 0.636 |  |
| HG01 | homoglyph | model signal: Cyrillic look-alike letters wreck tokenization so perplexity spikes | 200 | `c62da59ee3c7` | unsure | 0.602 |  |
| HG02 | homoglyph | model signal: zero-width spaces inside words | 200 | `74146b95bbf6` | ai | 0.805 |  |
| RP01 | repetition | both signals: one generated sentence repeated, degenerate input | 200 | `8939b569eef9` | ai | 0.998 |  |
| SH01 | short_text | model signal: barely above the minimum length, too short for a stable perplexity | 400 | `—` | — | — |  |
| SH02 | short_text | route: below the minimum word count should be refused, not scored | 400 | `—` | — | — |  |
| FP01 | false_positive | model signal: plain writing from a second-language writer | 200 | `90dbb951129e` | ai | 0.811 |  |
| FP02 | false_positive | model signal: a younger writer's plain school paragraph | 200 | `e32502b4d78c` | ai | 0.809 |  |
| FP03 | false_positive | both signals: plain workplace instructions written by a person | 200 | `7705176780e3` | ai | 0.792 |  |
| FP04 | false_positive | both signals: a formal cover letter written by a person | 200 | `99054b402772` | ai | 0.730 |  |
| FP05 | false_positive | style signal: a person who writes even, mid-length sentences | 200 | `2437bec2a444` | ai | 0.841 |  |
| FP06 | false_positive | model signal: a short human summary of a news story in simple words | 200 | `a892a6310d6e` | ai | 0.842 |  |
| MR01 | malformed_body | route: an empty body | 400 | `—` | — | — |  |
| MR02 | malformed_body | route: JSON that doesn't parse | 400 | `—` | — | — |  |
| MR03 | malformed_body | route: a JSON list instead of an object | 400 | `—` | — | — |  |
| MR04 | malformed_body | route: text field is a list | 400 | `—` | — | — |  |
| MR05 | malformed_body | route: text is only whitespace | 400 | `—` | — | — |  |
| MR06 | malformed_body | route: creator_id is an object | 200 | `4f4384eb1622` | ai | 0.859 |  |
| MR07 | malformed_body | route: an enormous text (~54 KB) | 413 | `—` | — | — |  |
| MR08 | malformed_body | route: right body, wrong content type | 400 | `—` | — | — |  |
| FL01 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 200 | `0f80716fb6a4` | ai | 0.843 |  |
| FL02 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 200 | `a8ebc0eb40f2` | ai | 0.843 |  |
| FL03 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 200 | `51bf1b251e3c` | ai | 0.843 |  |
| FL04 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 200 | `3f2e2e5a9ed6` | ai | 0.843 |  |
| FL05 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 200 | `03e33b02b2cf` | ai | 0.843 |  |
| FL06 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 429 | `—` | — | — |  |
| FL07 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 429 | `—` | — | — |  |
| FL08 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 429 | `—` | — | — |  |
| FL09 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 429 | `—` | — | — |  |
| FL10 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 429 | `—` | — | — |  |
| FL11 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 429 | `—` | — | — |  |
| FL12 | flood_same_creator | rate limiter: twelve rapid submissions from one creator_id | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `control_ai` | 2 | 0 | 2 |
| `control_human` | 1 | 0 | 1 |
| `evasion_casual` | 2 | 0 | 2 |
| `evasion_typos` | 3 | 0 | 3 |
| `false_positive` | 6 | 0 | 6 |
| `flood_same_creator` | 12 | 0 | 12 |
| `homoglyph` | 2 | 0 | 2 |
| `malformed_body` | 8 | 0 | 8 |
| `punctuation_stuffing` | 2 | 0 | 2 |
| `quote_padding` | 2 | 0 | 2 |
| `repetition` | 1 | 0 | 1 |
| `sentence_chop` | 2 | 0 | 2 |
| `short_text` | 2 | 0 | 2 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### CA01 — `control_ai`

*Targeting:* baseline: unmodified AI text should be labelled AI

```json
{
  "id": "CA01",
  "status": 200,
  "content_id": "47ce0e4ecbfb",
  "creator_id": "attacker_CA01",
  "guess": "ai",
  "confidence": 0.8592,
  "model_score": 0.9372,
  "style_score": 0.7422,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### CA02 — `control_ai`

*Targeting:* baseline: unmodified AI text should be labelled AI

```json
{
  "id": "CA02",
  "status": 200,
  "content_id": "848c45afa481",
  "creator_id": "attacker_CA02",
  "guess": "ai",
  "confidence": 0.8561,
  "model_score": 0.8995,
  "style_score": 0.7909,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### CH01 — `control_human`

*Targeting:* baseline: lively human text should be labelled human

```json
{
  "id": "CH01",
  "status": 200,
  "content_id": "7b609094cec2",
  "creator_id": "attacker_CH01",
  "guess": "human",
  "confidence": 0.2758,
  "model_score": 0.4263,
  "style_score": 0.05,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV01 — `evasion_typos`

*Targeting:* style signal: typos raise word variety so AI reads human

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "025133b40d32",
  "creator_id": "attacker_EV01",
  "guess": "ai",
  "confidence": 0.6999,
  "model_score": 0.6717,
  "style_score": 0.7422,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion_typos`

*Targeting:* both signals: typos raise perplexity and word variety

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "191f1c787d09",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.601,
  "model_score": 0.4744,
  "style_score": 0.7909,
  "label": "We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion_typos`

*Targeting:* model signal: heavy typos make the text unpredictable to gpt2

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "3c29d6095337",
  "creator_id": "attacker_EV03",
  "guess": "ai",
  "confidence": 0.6522,
  "model_score": 0.5698,
  "style_score": 0.7758,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion_casual`

*Targeting:* style signal: contractions and question marks inflate punctuation density

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "33c958351f39",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.4245,
  "model_score": 0.7013,
  "style_score": 0.0094,
  "label": "We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion_casual`

*Targeting:* style signal: an informal aside per sentence

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "0dd422870da1",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.5429,
  "model_score": 0.7791,
  "style_score": 0.1886,
  "label": "We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.",
  "error": null,
  "verdict": ""
}
```

### SC01 — `sentence_chop`

*Targeting:* style signal: mixing very short and long sentences raises length spread

```json
{
  "id": "SC01",
  "status": 200,
  "content_id": "15485704f9cf",
  "creator_id": "attacker_SC01",
  "guess": "unsure",
  "confidence": 0.5171,
  "model_score": 0.7379,
  "style_score": 0.186,
  "label": "We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.",
  "error": null,
  "verdict": ""
}
```

### SC02 — `sentence_chop`

*Targeting:* style signal: one-word sentences between generated ones

```json
{
  "id": "SC02",
  "status": 200,
  "content_id": "17d1f39d5307",
  "creator_id": "attacker_SC02",
  "guess": "ai",
  "confidence": 0.6659,
  "model_score": 0.8241,
  "style_score": 0.4286,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PS01 — `punctuation_stuffing`

*Targeting:* style signal: dashes, semicolons and parentheses inserted without changing words

```json
{
  "id": "PS01",
  "status": 200,
  "content_id": "500af70fe3d5",
  "creator_id": "attacker_PS01",
  "guess": "unsure",
  "confidence": 0.372,
  "model_score": 0.6108,
  "style_score": 0.0138,
  "label": "We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.",
  "error": null,
  "verdict": ""
}
```

### PS02 — `punctuation_stuffing`

*Targeting:* style signal: question marks and exclamation marks on generated sentences

```json
{
  "id": "PS02",
  "status": 200,
  "content_id": "7f42abcf89e0",
  "creator_id": "attacker_PS02",
  "guess": "unsure",
  "confidence": 0.5074,
  "model_score": 0.8257,
  "style_score": 0.03,
  "label": "We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.",
  "error": null,
  "verdict": ""
}
```

### QP01 — `quote_padding`

*Targeting:* both signals: a pasted human quotation dilutes the AI paragraph

```json
{
  "id": "QP01",
  "status": 200,
  "content_id": "904e041fceff",
  "creator_id": "attacker_QP01",
  "guess": "unsure",
  "confidence": 0.479,
  "model_score": 0.7984,
  "style_score": 0.0,
  "label": "We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.",
  "error": null,
  "verdict": ""
}
```

### QP02 — `quote_padding`

*Targeting:* model signal: a long rare-word quotation raises perplexity

```json
{
  "id": "QP02",
  "status": 200,
  "content_id": "9293b65580c1",
  "creator_id": "attacker_QP02",
  "guess": "unsure",
  "confidence": 0.6358,
  "model_score": 0.7214,
  "style_score": 0.5074,
  "label": "We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.",
  "error": null,
  "verdict": ""
}
```

### HG01 — `homoglyph`

*Targeting:* model signal: Cyrillic look-alike letters wreck tokenization so perplexity spikes

```json
{
  "id": "HG01",
  "status": 200,
  "content_id": "c62da59ee3c7",
  "creator_id": "attacker_HG01",
  "guess": "unsure",
  "confidence": 0.6015,
  "model_score": 0.3842,
  "style_score": 0.9274,
  "label": "We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.",
  "error": null,
  "verdict": ""
}
```

### HG02 — `homoglyph`

*Targeting:* model signal: zero-width spaces inside words

```json
{
  "id": "HG02",
  "status": 200,
  "content_id": "74146b95bbf6",
  "creator_id": "attacker_HG02",
  "guess": "ai",
  "confidence": 0.8049,
  "model_score": 0.8401,
  "style_score": 0.7521,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### RP01 — `repetition`

*Targeting:* both signals: one generated sentence repeated, degenerate input

```json
{
  "id": "RP01",
  "status": 200,
  "content_id": "8939b569eef9",
  "creator_id": "attacker_RP01",
  "guess": "ai",
  "confidence": 0.9975,
  "model_score": 0.9958,
  "style_score": 1.0,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### SH01 — `short_text`

*Targeting:* model signal: barely above the minimum length, too short for a stable perplexity

```json
{
  "id": "SH01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_SH01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### SH02 — `short_text`

*Targeting:* route: below the minimum word count should be refused, not scored

```json
{
  "id": "SH02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_SH02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* model signal: plain writing from a second-language writer

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "90dbb951129e",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "confidence": 0.8108,
  "model_score": 0.8724,
  "style_score": 0.7184,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* model signal: a younger writer's plain school paragraph

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "e32502b4d78c",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8091,
  "model_score": 0.8283,
  "style_score": 0.7804,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* both signals: plain workplace instructions written by a person

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "7705176780e3",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7922,
  "model_score": 0.7195,
  "style_score": 0.9012,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* both signals: a formal cover letter written by a person

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "99054b402772",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7302,
  "model_score": 0.8344,
  "style_score": 0.5739,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* style signal: a person who writes even, mid-length sentences

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "2437bec2a444",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8408,
  "model_score": 0.88,
  "style_score": 0.782,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* model signal: a short human summary of a news story in simple words

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "a892a6310d6e",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.8422,
  "model_score": 0.8636,
  "style_score": 0.8102,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MR01 — `malformed_body`

*Targeting:* route: an empty body

```json
{
  "id": "MR01",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR02 — `malformed_body`

*Targeting:* route: JSON that doesn't parse

```json
{
  "id": "MR02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR03 — `malformed_body`

*Targeting:* route: a JSON list instead of an object

```json
{
  "id": "MR03",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR04 — `malformed_body`

*Targeting:* route: text field is a list

```json
{
  "id": "MR04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR05 — `malformed_body`

*Targeting:* route: text is only whitespace

```json
{
  "id": "MR05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR06 — `malformed_body`

*Targeting:* route: creator_id is an object

```json
{
  "id": "MR06",
  "status": 200,
  "content_id": "4f4384eb1622",
  "creator_id": {
    "name": "x"
  },
  "guess": "ai",
  "confidence": 0.8592,
  "model_score": 0.9372,
  "style_score": 0.7422,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MR07 — `malformed_body`

*Targeting:* route: an enormous text (~54 KB)

```json
{
  "id": "MR07",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MR07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR08 — `malformed_body`

*Targeting:* route: right body, wrong content type

```json
{
  "id": "MR08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL01",
  "status": 200,
  "content_id": "0f80716fb6a4",
  "creator_id": "flood_bot",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.8881,
  "style_score": 0.7758,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL02 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL02",
  "status": 200,
  "content_id": "a8ebc0eb40f2",
  "creator_id": "flood_bot",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.8881,
  "style_score": 0.7758,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL03 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL03",
  "status": 200,
  "content_id": "51bf1b251e3c",
  "creator_id": "flood_bot",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.8881,
  "style_score": 0.7758,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL04 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL04",
  "status": 200,
  "content_id": "3f2e2e5a9ed6",
  "creator_id": "flood_bot",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.8881,
  "style_score": 0.7758,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL05 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL05",
  "status": 200,
  "content_id": "03e33b02b2cf",
  "creator_id": "flood_bot",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.8881,
  "style_score": 0.7758,
  "label": "This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL06 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL06",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_bot",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL07 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL07",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_bot",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL08 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL08",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_bot",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL09 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL09",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_bot",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL10 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL10",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_bot",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL11 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL11",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_bot",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL12 — `flood_same_creator`

*Targeting:* rate limiter: twelve rapid submissions from one creator_id

```json
{
  "id": "FL12",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_bot",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
