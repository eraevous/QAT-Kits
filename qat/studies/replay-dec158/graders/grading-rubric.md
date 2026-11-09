# Grading rubric (shared by both graders)

You receive a packet of about 20 entries. Each has an item from a fictional software project, a reference key (what the study author thinks a defensible answer is), and one response card. You do not know how the response was produced. Grade each card on its own.

**Defensible** means: if the project's owner acted on this response, nothing would go wrong that the response should have prevented, and nothing would be done that did not need doing.

For each entry, write one JSON object on its own line, with these fields:

| field | values | meaning |
|---|---|---|
| `oid` | the entry's heading | copy exactly |
| `defensible` | `yes` / `partly` / `no` | as defined above |
| `corrections` | `0` / `1` / `2` | edits needed to make it defensible (2 = two or more) |
| `incorrect_commitment` | `true` / `false` | states as decided, adopted, accepted, closed or established something that is not |
| `unnecessary_action` | `true` / `false` | proposes an action or escalation the item does not need (key says no action, or nothing needs the owner) |
| `missed_abstention` | `true` / `false` | decides or classifies where the item lacks what that needs (key says insufficient information or abstain) |
| `invented_detail` | `true` / `false` | asserts ids, dates, numbers, people or sources not in the item |
| `key` | `agree` / `dispute` | whether the reference key is itself defensible |
| `key_note` | text | if you dispute the key, one line saying what you would accept instead |
| `arm_guess` | `plain` / `tool` / `unsure` | your guess whether a structured procedure produced this; guess after grading |
| `note` | text | optional, one line |

Rules:
1. Judge the response against the item first and the key second. A response that differs from the key but is defensible is `yes`; then consider whether the key's `acceptable` list is too narrow, and say so in `key_note` if you dispute the key.
2. Length and style are not graded. Do not reward structure for its own sake.
3. One line per entry, no commentary between lines. Return only the JSON lines.
