"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.

Criterion 5 (the appeal path) can't be expressed as text alone — it needs a
submission, then an appeal against the content_id that came back. That one is
run by `check_appeals.py`, three trials, written to results/.
"""

AI_TEXTS = [
    "In today's fast-paced world, effective time management has become an "
    "essential skill for students and professionals alike. By prioritizing "
    "tasks, setting clear goals, and minimizing distractions, individuals can "
    "significantly improve their productivity. Furthermore, it is important to "
    "remember that time management is not just about working harder, but about "
    "working smarter. Ultimately, developing these habits can lead to greater "
    "success and a healthier work-life balance.",

    "Climate change is one of the most pressing challenges facing humanity "
    "today. Rising global temperatures are leading to more frequent extreme "
    "weather events, rising sea levels, and significant impacts on ecosystems "
    "around the world. Addressing this issue requires a coordinated effort from "
    "governments, businesses, and individuals. By investing in renewable energy "
    "and adopting sustainable practices, we can work together to build a more "
    "sustainable future for generations to come.",

    "Social media has transformed the way people communicate and share "
    "information. On one hand, it allows individuals to connect with friends "
    "and family across the globe. On the other hand, it can contribute to the "
    "spread of misinformation and negatively impact mental health. It is "
    "important for users to be mindful of how they engage with these platforms. "
    "Overall, social media is a powerful tool that must be used responsibly.",

    "Artificial intelligence is rapidly changing many aspects of modern life. "
    "From healthcare to transportation, AI technologies are being used to "
    "improve efficiency and solve complex problems. However, it is important to "
    "consider the ethical implications of these technologies, including issues "
    "related to privacy, bias, and accountability. As AI continues to evolve, "
    "it will be essential to strike a balance between innovation and "
    "responsibility.",

    "Reading is one of the most valuable habits a person can develop. It not "
    "only expands knowledge and vocabulary but also improves concentration and "
    "critical thinking skills. In addition, reading can provide a sense of "
    "relaxation and reduce stress. Whether it is fiction or nonfiction, reading "
    "regularly can have a positive impact on both personal and professional "
    "growth. Therefore, it is important to make time for reading every day.",
]

HUMAN_TEXTS = [
    "Okay so the dishwasher flooded again. Third time this month! I put a towel "
    "down, then another towel, then gave up and just stood there in my socks "
    "staring at it like it owed me money. The landlord says he'll 'take a look' "
    "Thursday — which, if history's any guide, means sometime in March.",

    "My grandmother never measured anything. Flour went in by the fistful, salt "
    "by the pinch (her pinch, which was enormous), and the oven was hot when it "
    "smelled hot. I've tried to write her recipes down for years. They don't "
    "survive the trip onto paper; something always goes missing.",

    "We lost 4-1. Not close. Coach made us run laps afterwards, which felt "
    "personal, and then on the bus home Danny fell asleep on my shoulder and "
    "drooled on my jacket. Great day. Ten out of ten. Would absolutely not do "
    "again, except we play them again in two weeks, so I guess I will?",

    "There's a crow outside my window who has figured out that if he taps on "
    "the glass at 6:40, I'll throw him a cracker. I did this once. Once! Now "
    "he's here every morning, tapping, glaring, and honestly I respect the "
    "hustle. My alarm clock is a bird with a business plan.",

    "The thing nobody tells you about moving is the boxes multiply. You pack "
    "twelve; you unpack forty. Where did they come from? Who packed a box with "
    "nothing but one spatula, a single sock, and a phone charger for a phone I "
    "haven't owned since 2019? Past me, apparently. Past me was not well.",
]

# Writing in my own voice — the criterion that matters most. Plain and
# ordinary on purpose: that's the writing signal one is most likely to accuse.
MY_WRITING = [
    "I started learning to code last year because I wanted to build a little "
    "app for my mom's bakery. It didn't go well at first. I spent a whole "
    "weekend on one bug and it turned out I had spelled a variable wrong. But I "
    "kept going, and now the app actually takes orders.",

    "My favorite place in the city is the library on the corner near my old "
    "school. It's not fancy. The chairs are old and the wifi barely works. But "
    "it's quiet, the people there are kind, and I've probably read half the "
    "books on the second floor by now.",

    "Last summer I worked at a grocery store. The work was boring but the "
    "people were funny. There was one regular who came in every day at noon to "
    "buy one banana and one lottery ticket. He never won, as far as I know, but "
    "he always said today was the day.",

    "I think group projects are hard because everyone has a different idea of "
    "what done means. For me, done means it works and it's tested. For my "
    "teammate last semester, done meant it ran once on his laptop. We figured "
    "it out eventually, mostly by talking more.",

    "When I was a kid we drove to my aunt's house every Thanksgiving. It was "
    "six hours each way. My brother and I would fight in the back seat for the "
    "first hour, sleep for the next three, and then fight again. My dad played "
    "the same CD the whole time. I still know every song.",

    "Cooking for myself was a big change when I moved out. The first month I "
    "ate pasta almost every night. Then a friend showed me how to make a simple "
    "stir fry, and that opened things up. Now I cook maybe four nights a week "
    "and I actually enjoy it most of the time.",

    "I don't really like running, but I like how I feel after. So I run three "
    "times a week, usually early before it gets hot. I listen to podcasts, not "
    "music, because music makes me go too fast and then I'm tired after one "
    "mile. Slow and steady works better for me.",

    "My phone screen has been cracked for almost a year. I keep saying I'll fix "
    "it, but it still works, so I never do. My friends make fun of me. At this "
    "point the crack is kind of part of the phone. If I fixed it, I think I "
    "would miss it a little.",

    "The hardest class I took was statistics. The teacher was good, but the "
    "ideas didn't click for me until the very end. What helped was doing the "
    "problems with real data I cared about, like basketball stats. After that "
    "the numbers felt like they meant something.",

    "On weekends I help my uncle at his car repair shop. I mostly hand him "
    "tools and clean up, but sometimes he lets me change the oil or rotate the "
    "tires. He doesn't talk much while he works. I like that. It's calm, and I "
    "learn a lot just by watching him.",
]

BORDERLINE_TEXTS = [
    # Lightly edited AI: contractions and one aside added, otherwise as generated.
    "Time management is honestly one of the most important skills you can "
    "have. If you prioritize your tasks and set clear goals, you'll get a lot "
    "more done. It's not about working harder (I learned that the hard way). "
    "It's about working smarter and building good habits over time.",
    # Plain human writing that reads predictably.
    "I like my job. I work at a store. I help people find things. Some days are "
    "busy and some days are slow. I like the busy days more because time goes "
    "faster. My manager is nice. I want to learn more and maybe be a manager "
    "one day too.",
]

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": MY_WRITING,
    },
    {
        "name": "label coverage",
        "criterion": 2,
        # One clearly AI, one clearly human, and the borderline pair.
        "texts": [AI_TEXTS[0], HUMAN_TEXTS[0]] + BORDERLINE_TEXTS,
    },
    {
        "name": "score spread",
        "criterion": 3,
        # First five are AI, last five are human — compare the two means.
        "texts": AI_TEXTS + HUMAN_TEXTS,
    },
    {
        "name": "bad input",
        "criterion": 4,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": 12345, "creator_id": "eval_bad_number"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
