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
| unsure | 0.35 – 0.65 | We can't tell either way for this piece. Plenty of people write in a style our checks find hard to read, so this isn't a judgement about you or your work, and nothing happens because of it. |
| high-confidence AI | 0.65 – 1.00 | This piece has a lot in common with AI-generated writing, and both of our checks agree on that. This is an automated estimate, not proof. If you wrote it yourself, you can appeal and a person will review it. |

All three are reachable. In calibration, lively human text scored 0.17–0.28 (human), my own plain writing mostly 0.49–0.58 (unsure), and generated text 0.76–0.90 (AI).

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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
