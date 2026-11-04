# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. A writer sends `POST /submit` with `{"text": ..., "creator_id": ...}`.
2. The route (`app.py::submit`) checks the input. Anything that isn't a JSON object, or is missing `text`, has a non-string `text`, has fewer than 20 words or more than 20,000 characters, gets a 4xx with a plain explanation, and the rejection is logged.
3. **Signal one** (`detector.model_signal`) runs GPT-2 locally and turns the text's perplexity into a 0–1 "how predictable is this" score.
4. **Signal two** (`stylometry.style_signal`) measures the text's shape (sentence-length spread, vocabulary variety, expressive punctuation) and turns it into a 0–1 score.
5. `scoring.py::combine_signals` merges them into one score (0.6 model / 0.4 style). If the two signals disagree by more than 0.4, the score can't reach the AI band.
6. `scoring.py::score_to_label` maps the score to one of three plain-English labels.
7. The decision is written to `logs/audit.jsonl` with a new `content_id`, and the writer gets back the label, both signal scores and the id they need to appeal with `POST /appeal`.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to GPT-2 (perplexity), squashed onto 0–1 with a logistic curve: perplexity 45 scores 0.5, and lower perplexity scores higher. I left the midpoint at 45. My clearly-AI calibration texts scored perplexity 7–15 and clearly-human ones 52–84, so 45 already separates those two groups.

**Why that might differ between human and AI writing:** A language model writes by picking likely next words, so its output is text a language model finds easy to predict. People make odder, more specific word choices.

**What it can't see:** Who wrote it. It rewards common words in short, plain sentences, so a second-language writer, a younger writer or anyone writing plainly scores as machine-like. In calibration my own plain paragraphs had perplexity 22–27, much closer to AI (7–15) than to the lively human samples (52–84).

### Signal two — the style signal

**What it measures:** Three measures of the text's shape, each flipped so that higher means more AI-like and ramped onto 0–1 between two calibration points:
- **Sentence-length spread**: the coefficient of variation of sentence lengths. A CV of 0.65 or more scores fully human, 0.20 or less fully AI. Weight 0.45.
- **Vocabulary variety**: a moving-average type-token ratio over 50-word windows, so length doesn't skew it. 0.85 scores human, 0.65 scores AI. Weight 0.20.
- **Expressive punctuation**: `; : ! ? ( ) ' " -` and dashes per 100 words. 6.0 scores human, 0.5 scores AI. Weight 0.35.

Texts with fewer than 3 sentences get a neutral 0.5 for spread.

**Why that might differ between human and AI writing:** Generated prose marches in even, mid-length sentences with few contractions or asides. Human writing is lumpier: a three-word sentence next to a forty-word one, plus contractions, questions and dashes.

**What it can't see:** Meaning. Anything that changes the shape without changing the words moves it: chopped-up sentences, added dashes and question marks, contractions, a pasted quote. And a person who naturally writes even sentences with no contractions looks exactly like a model.

### The combining rule

**The rule:** A weighted average, with one exception: an accusation needs both signals to agree. If the two scores differ by more than 0.4, the combined score is capped just below the AI threshold. A split can come out "unsure" (or human), but never "high-confidence AI".

**The numbers:** `combined = 0.6 × model_score + 0.4 × style_score`. If `|model − style| > 0.4`, then `combined = min(combined, AI_THRESHOLD − 0.01)`. The model signal gets more weight because it separated my calibration sets more cleanly. The style signal is cheap to game, so it shouldn't drive the score on its own.

**Where it lives:** `scoring.py::combine_signals` (constants in `config.py`: `WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`, `DISAGREEMENT_GAP`)

**A case where my two signals split, and what my rule does with it:**
A pasted-quotation attack (QP01: an AI paragraph about volunteering, with a chatty neighbour's quote added at the end) scored model 0.798 (very predictable) but style 0.000, because the quote brought in contractions, a dash and an uneven sentence. The weighted average is 0.479. The gap is 0.80, so the cap also applies, and it lands as **unsure**. The rule doing exactly what I meant still lets that AI text escape an AI label, and I'd rather lose that one than accuse someone on a single signal.


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was most likely written by a person. |
| unsure | 0.35 – 0.85 *(0.35 – 0.65 in unit 7)* | We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it. |
| high-confidence AI | 0.85 – 1.00 *(0.65 – 1.00 in unit 7)* | This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it. |

All three are reachable. In calibration, lively human text scored 0.17–0.28 (human), my own plain writing mostly 0.49–0.58 (unsure), and generated text 0.76–0.90 (AI). After the unit 8 threshold change, the AI label is still reachable (the AI controls score 0.86, and repeated boilerplate scores 0.998), but much harder to reach. See **The Improvement**.

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The person reading it most likely wrote every word, so it puts the blame on our checks ("hard to read") rather than on them. It also says outright that nothing happens as a result. "We can't tell either way" is honest without hinting that we suspect them.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I started learning to code last year because I wanted to build a little app for my mom'\''s bakery. It didn'\''t go well at first. I spent a whole weekend on one bug and it turned out I had spelled a variable wrong. But I kept going, and now the app actually takes orders.", "creator_id": "adaya"}'
```

```json
{"confidence":0.5701,"content_id":"bb8c79afdc25","guess":"unsure","label":"We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.","model_score":0.7051,"status":"decided","style_score":0.3675}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "bb8c79afdc25", "reasoning": "I wrote this myself about my own project. I just write plainly."}'
```

```json
{"content_id":"bb8c79afdc25","message":"Thanks — your appeal is recorded and a person will review this piece. The label won't be used against you while it's under review.","original_label":"We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.","status":"under_review"}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{"count":2,"entries":[{"combined_score":0.5701,"content_id":"bb8c79afdc25","creator_id":"adaya","guess":"unsure","label":"We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it.","model_score":0.7051,"status":"decided","style_score":0.3675,"timestamp":"2026-11-04T05:03:24+00:00"},{"content_id":"bb8c79afdc25","creator_id":"adaya","event":"appeal","reasoning":"I wrote this myself about my own project. I just write plainly.","status":"under_review","timestamp":"2026-11-04T05:03:24+00:00"}]}
```

An appeal against a `content_id` that doesn't exist returns `404 content_not_found`. Missing, empty or too-short `text` returns `400`, and the rejection is logged.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I used Claude Code (an AI coding agent) to implement the three style measures and the `/submit` route from the starter's TODOs.
- *What came back:* Working code: a sentence-length CV, a plain type-token ratio and a count of all punctuation.
- *What I changed:* Plain TTR falls as text gets longer, so it was swapped for a 50-word moving-average TTR. Punctuation was narrowed to "expressive" marks (no full stops or commas), because everyone uses those. The ramp endpoints were then set from the calibration scores, not guessed.

**Moment 2**

- *What I asked for:* A combining rule and label wording.
- *What came back:* A plain 50/50 weighted average and labels that showed the numeric confidence.
- *What I changed:* The weights moved to 0.6/0.4, and a disagreement cap was added so a split between the signals can never produce an AI label. The labels were rewritten with no numbers or "threshold" language. The unsure label now explicitly says it isn't a judgement about the writer.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A real writer submits a few pieces an hour, maybe a handful of quick re-tries after an edit, so 5 a minute never touches them. 50 a day is several times more than any honest writer needs. Someone probing my thresholds needs hundreds of near-identical variations, and 50 a day per caller makes that take weeks rather than seconds.

**What a caller counts as:** Per `creator_id`, falling back to the IP address when there isn't one (the key function in `app.py`). This is fair to a household sharing one IP, but a script that invents a new `creator_id` for every request gets a fresh limit each time. The attack set shows this: 45 attacks from 45 ids never tripped it. A real deployment would add a second, looser per-IP limit on top.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

(`results/flood_2026-11-04_0004.md`). Each 429 is logged as a `rejected` entry with `reason: "rate_limited"` (see FL06 below).

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

> **About the attack set.** The staff attack set wasn't in the starter repo, so I built one in the same format: `attack_set/attacks.csv` and `attack_set/attacks_malformed_requests.csv`, 45 attacks in 13 families. It runs with `python run_attacks.py --set attack_set`. If the course set is released, it drops into the same command.

Full report: `results/attack_run_2026-11-04_0005_before.md`. Thresholds at this point: human ≤ 0.35, AI ≥ 0.65.

**How I judged them:** an evasion attack (AI text in disguise) **held** if it was still labelled AI and **broke** if it escaped to unsure or human. A false-positive attack (real human writing) **held** if it was *not* labelled AI. A malformed request held if it got a clean 4xx (or was handled safely). The flood held if it hit 429.

| ID | Family | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|
| CA01 | control_ai | 200 | ai | 0.859 | HELD |
| CA02 | control_ai | 200 | ai | 0.856 | HELD |
| CH01 | control_human | 200 | human | 0.276 | HELD |
| EV01 | evasion_typos | 200 | ai | 0.700 | HELD |
| EV02 | evasion_typos | 200 | unsure | 0.601 | BROKE |
| EV03 | evasion_typos | 200 | ai | 0.652 | HELD |
| EV04 | evasion_casual | 200 | unsure | 0.424 | BROKE |
| EV05 | evasion_casual | 200 | unsure | 0.543 | BROKE |
| SC01 | sentence_chop | 200 | unsure | 0.517 | BROKE |
| SC02 | sentence_chop | 200 | ai | 0.666 | HELD |
| PS01 | punctuation_stuffing | 200 | unsure | 0.372 | BROKE |
| PS02 | punctuation_stuffing | 200 | unsure | 0.507 | BROKE |
| QP01 | quote_padding | 200 | unsure | 0.479 | BROKE |
| QP02 | quote_padding | 200 | unsure | 0.636 | BROKE |
| HG01 | homoglyph | 200 | unsure | 0.602 | BROKE |
| HG02 | homoglyph | 200 | ai | 0.805 | HELD |
| RP01 | repetition | 200 | ai | 0.998 | HELD |
| SH01 | short_text | 400 | — | — | HELD (refused, 19 words) |
| SH02 | short_text | 400 | — | — | HELD |
| FP01 | false_positive | 200 | ai | 0.811 | **BROKE** |
| FP02 | false_positive | 200 | ai | 0.809 | **BROKE** |
| FP03 | false_positive | 200 | ai | 0.792 | **BROKE** |
| FP04 | false_positive | 200 | ai | 0.730 | **BROKE** |
| FP05 | false_positive | 200 | ai | 0.841 | **BROKE** |
| FP06 | false_positive | 200 | ai | 0.842 | **BROKE** |
| MR01 | malformed_body (empty body) | 400 | — | — | HELD |
| MR02 | malformed_body (bad JSON) | 400 | — | — | HELD |
| MR03 | malformed_body (JSON list) | 400 | — | — | HELD |
| MR04 | malformed_body (text is a list) | 400 | — | — | HELD |
| MR05 | malformed_body (whitespace text) | 400 | — | — | HELD |
| MR06 | malformed_body (creator_id is an object) | 200 | ai | 0.859 | HELD (scored as `anonymous`, no crash) |
| MR07 | malformed_body (54 KB text) | 413 | — | — | HELD |
| MR08 | malformed_body (text/plain) | 400 | — | — | HELD |
| FL01–FL05 | flood_same_creator | 200 ×5 | ai | 0.843 | — |
| FL06–FL12 | flood_same_creator | 429 ×7 | — | — | HELD |

**Totals:** 0 crashes or 5xx. 15 broke: 9 evasions and all 6 false positives.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

From `logs/audit.jsonl` (also in `results/audit_extract_before.json`). Label text shortened to `…` for space; the full text is in the log.

```json
{"timestamp": "2026-11-04T05:05:32+00:00", "content_id": "90dbb951129e", "creator_id": "attacker_FP01", "guess": "ai", "model_score": 0.8724, "style_score": 0.7184, "combined_score": 0.8108, "label": "This piece has a lot in common with AI-generated writing…", "status": "decided"}
{"timestamp": "2026-11-04T05:05:32+00:00", "content_id": "2437bec2a444", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.88, "style_score": 0.782, "combined_score": 0.8408, "label": "This piece has a lot in common with AI-generated writing…", "status": "decided"}
{"timestamp": "2026-11-04T05:05:32+00:00", "content_id": "99054b402772", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8344, "style_score": 0.5739, "combined_score": 0.7302, "label": "This piece has a lot in common with AI-generated writing…", "status": "decided"}
{"timestamp": "2026-11-04T05:05:29+00:00", "content_id": "33c958351f39", "creator_id": "attacker_EV04", "guess": "unsure", "model_score": 0.7013, "style_score": 0.0094, "combined_score": 0.4245, "label": "We can't tell either way for this piece…", "status": "decided"}
{"timestamp": "2026-11-04T05:05:30+00:00", "content_id": "500af70fe3d5", "creator_id": "attacker_PS01", "guess": "unsure", "model_score": 0.6108, "style_score": 0.0138, "combined_score": 0.372, "label": "We can't tell either way for this piece…", "status": "decided"}
{"timestamp": "2026-11-04T05:05:31+00:00", "content_id": "904e041fceff", "creator_id": "attacker_QP01", "guess": "unsure", "model_score": 0.7984, "style_score": 0.0, "combined_score": 0.479, "label": "We can't tell either way for this piece…", "status": "decided"}
{"timestamp": "2026-11-04T05:05:31+00:00", "content_id": "c62da59ee3c7", "creator_id": "attacker_HG01", "guess": "unsure", "model_score": 0.3842, "style_score": 0.9274, "combined_score": 0.6015, "label": "We can't tell either way for this piece…", "status": "decided"}
{"timestamp": "2026-11-04T05:05:29+00:00", "content_id": "025133b40d32", "creator_id": "attacker_EV01", "guess": "ai", "model_score": 0.6717, "style_score": 0.7422, "combined_score": 0.6999, "label": "This piece has a lot in common with AI-generated writing…", "status": "decided"}
{"timestamp": "2026-11-04T05:05:33+00:00", "content_id": null, "creator_id": "attacker_MR07", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "text_too_long", "http_status": 413}
{"timestamp": "2026-11-04T05:05:34+00:00", "content_id": null, "creator_id": "flood_bot", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP01: a paragraph by someone who came to the country three years ago, writing in simple English about being proud of learning it, labelled high-confidence AI at 0.81. Both signals agreed, so my disagreement safeguard never kicked in. It's the writer with the least room to argue back being told their own story about learning the language looks machine-made.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled AI | ≤ 1 of 10 | 3 of 10 | 3 of 10 | 3 of 10 | **MISS** |
| 2. All three labels reached | each label ≥ 1 per trial | ai, human, unsure | ai, human, unsure | ai, human, unsure | MET |
| 3. AI mean − human mean | ≥ 0.30 | 0.602 | 0.602 | 0.602 | MET |
| 4. Bad input: 5xx / clean 4xx | 0 / 5 of 5 | 0 / 5 | 0 / 5 | 0 / 5 | MET |
| 5. Appeals work + unknown id 404 | 6 of 6 | 6 / 6 | 6 / 6 | 6 / 6 | MET |

Criteria 1–4 come from `run_eval.py --label before` (`results/run_2026-11-04_0005_before.md`). Criterion 5 can't be sent as plain text, so I extended the test with `check_appeals.py`: it submits five pieces, appeals each one, checks the log, then appeals a bogus id. Output is in `results/appeals_2026-11-04_0005_before.md`. The three trials are identical because GPT-2 scoring here is deterministic (no sampling), so repeats only guard against flakiness in the route.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Produced by `run_eval.py::main` against `app.py::submit`, scenario "my own writing", trial 1 (first 3 of 10 results, label text shortened):

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.5701, "model_score": 0.7051, "style_score": 0.3675, "label": "We can't tell either way for this piece…", "sent": "I started learning to code last year because I wanted to build a littl"},
  {"status": 200, "guess": "unsure", "confidence": 0.5063, "model_score": 0.7631, "style_score": 0.1212, "label": "We can't tell either way for this piece…", "sent": "My favorite place in the city is the library on the corner near my old"},
  {"status": 200, "guess": "ai", "confidence": 0.7097, "model_score": 0.7441, "style_score": 0.6581, "label": "This piece has a lot in common with AI-generated writing…", "sent": "Last summer I worked at a grocery store. The work was boring but the pe"}
]
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

**Diagnosis A: criterion 1 miss + FP01–FP06 (9 failures, one problem). Stage: signal one and signal two together, then the label mapping.**
All nine are plain human writing: short sentences, common words, no contractions. Signal one put them at perplexity 13–27, which the logistic maps to model scores of 0.72–0.88, right next to real AI text (perplexity 7–15, scores 0.86–0.95). Signal two agreed, for two reasons: plain writers use almost no expressive punctuation (density 0–2, which scores fully AI), and their vocabulary is *less* varied than generated text (TTR 0.73–0.79 vs 0.79–0.91), so my TTR measure points the wrong way for them. Because the signals agreed, the disagreement cap never fired, and with the AI band starting at 0.65 they all became accusations.

**Diagnosis B: style-only evasions, EV04, EV05, SC01, PS01, PS02, QP01 (6 broke). Stage: signal two, then the combining rule.**
Each one changes shape, not words: contractions, `?`, dashes, parentheses, chopped sentences or a pasted quote. Punctuation density jumped to 6–20 per 100 words (for SC01, sentence spread jumped to 1.20 instead), so the style score fell to 0.00–0.19 while the model score stayed at 0.61–0.83. With style weighted at 0.4, a style score near zero takes up to 0.4 off the combined score, which put these at 0.37–0.54. The disagreement cap would have held them under the AI band anyway: every one of them has a gap over 0.4. So the safeguard I built for writers would let these through even with different weights.

**Diagnosis C: model-signal evasions, EV02, QP02, HG01 (3 broke). Stage: signal one.**
Typos (EV02), a rare-word quotation (QP02) and Cyrillic look-alike letters (HG01) all raise GPT-2's perplexity, to 48, 25 and 60. That pulled the model score down to 0.38–0.72, and QP02 missed the AI band by 0.014 (0.636). HG01 is the clearest case: the text is unreadable to the tokenizer, so model 0.38 vs style 0.93 is a split, and the cap keeps it at "unsure".


---

## The Improvement

**What I changed:** I raised `AI_THRESHOLD` in `config.py` from **0.65 to 0.85**. The unsure band is now 0.35–0.85. That's one line, and nothing else changed. The disagreement cap follows it automatically, since it's defined as `AI_THRESHOLD − 0.01`.

**Which diagnosis pointed at it:** Diagnosis A. The plain-writing false positives all scored 0.71–0.84 with *both* signals agreeing, so no rule about disagreement could help. The only stage that could stop those accusations without rebuilding a signal was the label mapping. Before committing, I compared other options offline: moving the detector midpoint from 45 to 20, dropping the backwards TTR measure, and thresholds of 0.80 and 0.85. 0.85 was the only one that took both my own writing and the false-positive set to zero AI labels.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Full report: `results/attack_run_2026-11-04_0007_after.md`. Scores are identical to before; only the label mapping moved.

| ID | Family | Status | Guess | Score | Verdict | Changed? |
|---|---|---|---|---|---|---|
| CA01 | control_ai | 200 | ai | 0.859 | HELD | |
| CA02 | control_ai | 200 | ai | 0.856 | HELD | |
| CH01 | control_human | 200 | human | 0.276 | HELD | |
| EV01 | evasion_typos | 200 | unsure | 0.700 | BROKE | held → broke |
| EV02 | evasion_typos | 200 | unsure | 0.601 | BROKE | |
| EV03 | evasion_typos | 200 | unsure | 0.652 | BROKE | held → broke |
| EV04 | evasion_casual | 200 | unsure | 0.424 | BROKE | |
| EV05 | evasion_casual | 200 | unsure | 0.543 | BROKE | |
| SC01 | sentence_chop | 200 | unsure | 0.517 | BROKE | |
| SC02 | sentence_chop | 200 | unsure | 0.666 | BROKE | held → broke |
| PS01 | punctuation_stuffing | 200 | unsure | 0.372 | BROKE | |
| PS02 | punctuation_stuffing | 200 | unsure | 0.507 | BROKE | |
| QP01 | quote_padding | 200 | unsure | 0.479 | BROKE | |
| QP02 | quote_padding | 200 | unsure | 0.636 | BROKE | |
| HG01 | homoglyph | 200 | unsure | 0.602 | BROKE | |
| HG02 | homoglyph | 200 | unsure | 0.805 | BROKE | held → broke |
| RP01 | repetition | 200 | ai | 0.998 | HELD | |
| SH01, SH02 | short_text | 400 | — | — | HELD | |
| FP01 | false_positive | 200 | unsure | 0.811 | HELD | broke → held |
| FP02 | false_positive | 200 | unsure | 0.809 | HELD | broke → held |
| FP03 | false_positive | 200 | unsure | 0.792 | HELD | broke → held |
| FP04 | false_positive | 200 | unsure | 0.730 | HELD | broke → held |
| FP05 | false_positive | 200 | unsure | 0.841 | HELD | broke → held |
| FP06 | false_positive | 200 | unsure | 0.842 | HELD | broke → held |
| MR01–MR08 | malformed_body | 400 / 413 (MR06: 200) | — | — | HELD | |
| FL01–FL12 | flood_same_creator | 200 ×5, 429 ×7 | — | — | HELD | |

**Totals:** 0 crashes. 13 broke (was 15): all 6 false positives now hold, but 4 evasions that used to be caught (EV01, EV03, SC02, HG02) now get through.

**Criteria after** (`results/run_2026-11-04_0007_after.md`, `results/appeals_2026-11-04_0007_after.md`):

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled AI | ≤ 1 of 10 | 0 of 10 | 0 of 10 | 0 of 10 | MET (was miss) |
| 2. All three labels reached | each ≥ 1 per trial | human, unsure only | human, unsure only | human, unsure only | **MISS** (was met) |
| 3. AI mean − human mean | ≥ 0.30 | 0.602 | 0.602 | 0.602 | MET |
| 4. Bad input: 5xx / clean 4xx | 0 / 5 of 5 | 0 / 5 | 0 / 5 | 0 / 5 | MET |
| 5. Appeals work + unknown id 404 | 6 of 6 | 6 / 6 | 6 / 6 | 6 / 6 | MET |

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

It helped with what I care most about, and it cost something real. Wrong accusations went from 3/10 of my own writing and 6/6 plain-writing attacks to **0 in both**, across all three trials. But the AI label is now nearly unreachable for ordinary generated text: only 1 of my 5 clearly-AI samples (0.898) and the two controls still get it. My coverage input (0.756) now lands in unsure, so criterion 2 went from met to missed. I'm keeping criterion 2 as written rather than lowering it, since the miss is the honest cost of the change.


---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

- **Criterion 2 (label coverage) — now missed.** My own writing tops out at 0.73 and generated text starts at 0.76, so no single threshold separates them on these signals. The real fix is a better signal one: a stronger model than GPT-2, or perplexity *variance* across sentences ("burstiness") instead of the mean. I stopped because that's a rebuild of a signal, not a tuning change.
- **Style-only evasions (EV04, EV05, SC01, PS01, PS02, QP01).** Signal two can't read, so adding contractions or dashes beats it every time. I'd cap how far any single style measure can pull the score, or drop punctuation density, which is the cheapest measure to game. I didn't, because punctuation is also what separates lively human writing from AI in my data, so removing it would raise false positives again.
- **Model-signal evasions (EV02, QP02, HG01, HG02, EV01, EV03).** Typos and homoglyphs raise perplexity. I'd normalise text before scoring: map Cyrillic and other look-alikes to Latin, strip zero-width characters, maybe spell-correct. Normalisation is cheap and doesn't hurt real writers, so it'd be the next thing I'd do. I stopped at one change so the before/after comparison stays clean.
- **SC02, EV01, EV03 and HG02 now escape** only because of my new threshold; they score 0.65–0.81. That's the accepted cost of the change above.
- **Rate limiting by `creator_id` is easy to dodge** by inventing new ids. I'd add a per-IP limit alongside it.
- **Criterion 2's evidence is thin.** It rests on one AI input. A fairer test would use several, which I'd add before re-running.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I'd keep the high AI threshold and accept that most AI text gets "unsure" instead of "AI", because a wrong accusation lands on one real writer, often a plain or second-language writer with the least ability to push back. The cost is paid by the site and its honest readers, who see more undetected AI text, and that cost is spread thin, which is a better place for it than on one person.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [x] criteria.md has five numbered criteria, each naming a target
       [x] Each has a reason underneath
       [x] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [x] Two signals that measure DIFFERENT things, each with a named blind spot
       [x] Three label variants, all reachable, written out in full
       [x] POST /appeal changes status and writes to the log
       [x] Signals and Scoring names scoring.py::combine_signals
       [x] Sample Run: a submission AND an appeal, as pasted text
       [x] At least four new commits
       [x] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [x] Rate limiting on /submit, with your numbers justified
       [x] The pasted run of status codes showing 429
       [x] Audit log with all nine fields, recording rejections too
       [x] The attack set run IN FULL, every input with an outcome
       [x] Ten audit log entries pasted as text
       [x] Five criteria across three trials
       [x] A diagnosis for every miss and every broken attack — stage AND mechanism
       [x] One improvement, with Attack Run — After
       [x] What's Still Broken, including the production trade
       [x] At least four new commits
       [x] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
