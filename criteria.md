# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

<!-- Your criterion. It must name a number. -->

Of 10 pieces of writing I wrote myself, **at most 1** is labelled high-confidence AI in any single trial.

**Why this target:**

On a writing site a wrong accusation costs the writer far more than a missed detection costs the site, so false positives get the tightest target. One in ten is strict but not zero, because perplexity on short plain writing is genuinely noisy.

---

## 2.

<!-- Your criterion. -->

All three labels are reachable: across my label-coverage inputs, **each of the three labels (human, unsure, AI) appears at least once** in every trial.

**Why this target:**

A label no score can produce is a gap in the ranges, and the whole point of an "unsure" band is that it actually gets used. If any label is missing in any trial, the thresholds or the signals are broken.

---

## 3.

<!-- Your criterion. -->

Score spread: the mean combined score of my clearly-AI inputs is **at least 0.30 higher** than the mean combined score of my clearly-human inputs, in every trial.

**Why this target:**

If clear cases don't separate by about a third of the scale, the thresholds are just slicing noise and the labels mean nothing. 0.30 is roughly the width of my unsure band, so clear cases should land on opposite sides of it.

---

## 4.

<!-- Your criterion. -->

Bad input never crashes the service: **0 of 5** malformed requests (empty text, missing text, null text, non-string text, enormous text) return a 5xx, and **all 5** return a 4xx with a JSON error message.

**Why this target:**

A crash on malformed input is one of the most common real failures and there is no threshold that makes it acceptable. Every bad request should get a clear 4xx so the caller knows what they did wrong.

---

## 5.

<!-- Your criterion. -->

The appeal path always works: for **5 of 5** submissions appealed, `/appeal` returns 200 with status `under_review` and the audit log gains an appeal entry for that content_id; an appeal against an unknown content_id returns **404** every time.

**Why this target:**

The appeal is the only thing between a wrong accusation and nothing at all, so it has to work every single time, not most of the time. A typo'd id silently "succeeding" would be worse than an error, so that case is tested too.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
