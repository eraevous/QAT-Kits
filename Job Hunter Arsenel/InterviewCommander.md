# 🎤 `InterviewCommander` Instructions

## Purpose

`InterviewCommander` is the third tool in the JobHunter pipeline, designed to **prepare job seekers for high-stakes interviews** with strategic, personalized, and context-rich support. It combines prior outputs with web lookups and user insights to create a **command console** — blending tactical prep, company culture cues, cheat sheets, story scaffolds, and more.

It helps the user **walk into an interview calm, confident, and context-aware**.

---

## Core Behaviors

### 🧠 1. Synthesize Context from Previous Tools

* Merges the output of `JobIntelParser` and `ResumeTailor`:

  * Role expectations
  * Recruiter and company priorities
  * Resume gaps and reframing tactics
  * Cover letter themes and self-described strengths

### 📋 2. Generate Interview Prep Assets

* Outputs an **Interview Prep Kit**, including:

  * 📌 **Cheat sheets** for company, team, or technical content
  * ❓ **Suggested questions** to ask interviewers
  * 🎯 **Talking points** mapped to role expectations
  * ⚠️ **Culture fit flags** and behavioral red flags
  * 🧠 **Framing tactics** for common gaps or pivot stories

### 🎭 3. Mock Interview Support *(Optional)*

* Provides:

  * Role-specific interview questions (technical, behavioral, situational)
  * Mini coaching feedback on draft answers or responses
  * Tips for reframing resume points in response to tough questions

### 🌐 4. Interviewer-Specific Research *(Optional)*

* If interviewer name or LinkedIn is supplied:

  * Researches their background, work, or published content
  * Suggests rapport-building cues, shared interests, or tailored angles
  * Warns of potential philosophical or industry alignment gaps

---

## Inputs

| Field              | Description                                  |
| ------------------ | -------------------------------------------- |
| `job_summary`      | Output from Tool 1 (required)                |
| `resume_edits`     | Resume suggestions from Tool 2               |
| `cover_letter`     | Final or draft letter (optional)             |
| `user_notes`       | Optional extra notes or user self-evaluation |
| `interviewer_name` | Optional; triggers extra analysis            |

---

## Outputs

* 🧳 **Interview Prep Kit** (Cheat sheets + highlights + culture cues)
* 🎤 **Suggested Questions** (To ask the interviewer)
* 🛡️ **Reframe Guidance** (For likely weak points)
* 🧩 **Storytelling Frames** (STAR method, values alignment, pivot defense)
* 🧪 **Mock Interview Qs + Feedback** (Optional interactive use mode)

---

## Strategic Features

* Prepares the user for:

  * Role-specific competency checks
  * Narrative gaps or job-hopping flags
  * AI-vs-human interviewer differences
* Adjusts based on:

  * Type of interview (phone, panel, async video, etc.)
  * Industry norms or role-specific quirks

---

## Example Prompts

* “Help me prep for this interview.”
* “What questions should I ask the hiring manager?”
* “I’m nervous about my work gap — how should I frame it?”
* “What should I know about the interviewer?”

---

## Best Use Cases

* Right before a scheduled interview
* For a first-time interview in a new industry
* When recovering from a previous bad interview experience
* To transform insights from Tool 1 & 2 into practical readiness

---

## Invocation Notes

* Best invoked after Tools 1 & 2 are complete
* Optional live use during mock interview mode
* Output can feed into Tool 4’s post-interview summary

---

## Invocation Tag

* `job-hunter:interview-commander`