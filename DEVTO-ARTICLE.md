---
title: "SlothBrief: Let Local AI Turn My Brain Dump Into a Calm Plan"
published: false
description: "A tiny offline-first productivity helper built with Qwen2.5 3B, Ollama, and Flask for the Slow and Steady open-source AI challenge."
tags: opensource, ai, python, productivity
---

# SlothBrief: Less sorting. More breathing room. 🦥

I often have a list of tasks in my head, but turning that list into a clear plan can feel like another task. For the DEV Community's **Slow and Steady** challenge, I built **SlothBrief**: a small productivity assistant that turns messy notes into a short summary, prioritized next steps, and a gentle reminder.

The idea is simple: let AI do the organizing so a person can spend less energy getting started.

## What I built

SlothBrief is a local web app. Paste a brain dump—reminders, meeting notes, errands, or unfinished tasks—and it asks a local language model to return:
- A concise summary
- Suggested next steps, when the notes support them
- High, Medium, and Low priority labels
- One gentle suggestion for getting started

## Demo

**Local demo:** [Add your screen-recording link here]

**Code:** [Add your GitHub repository URL here]

The app runs on my computer at `http://127.0.0.1:5000`. Record the notes going in and the model-generated plan coming out. Use real output from the local model.

## How I built it

- **Qwen2.5 3B** — the open-weight model
- **Ollama** — runs the model locally
- **Flask** — connects the interface to the local model API
- **HTML, CSS, and JavaScript** — a responsive interface without a frontend build step

The browser submits the notes to Flask. Flask calls Ollama on the same computer, asks for structured JSON, and renders the response as a summary and prioritized list.

## Why open innovation matters here

For a tool that handles personal notes, where the model runs matters. With this setup, prompts go to the local Ollama service rather than a hosted AI API. After downloading the model and installing dependencies, the app can generate results without an internet connection. That gives users more control over where their text is processed.

The model is also replaceable: users can install a compatible model and change the `OLLAMA_MODEL` environment variable. They are not tied to one hosted inference provider.

There are trade-offs. Local inference uses the computer's memory and processing power, and a smaller model can misunderstand context or produce imperfect priorities. SlothBrief treats its suggestions as a starting point, not an unquestionable source of truth.

## What I learned

The interesting part wasn't adding a chat box. It was making the model's output predictable enough to be useful: requesting a small JSON structure, validating the response, handling Ollama connection errors, and keeping the interface focused on one job.

I also learned that a local-first app and a cloud deployment are not the same thing. A cloud server cannot reach Ollama running on my laptop at `localhost`. I chose to demonstrate the real local inference path rather than present canned demo output as live AI.

## What's next

- Export the plan as Markdown
- Let users mark tasks complete in the current session
- Add prompt styles such as “gentle,” “deadline-focused,” and “meeting follow-up”
- Test compatible open-weight models

SlothBrief is a small experiment in a different kind of productivity: less pressure to move faster, and less friction to take the next step.

**What repetitive organizing task would you want local AI to take off your plate?**

---

### Before publishing
- Replace the GitHub and demo placeholders.
- Run the app and record a real demo.
- Confirm offline generation by disconnecting from the internet after setup.
- Make sure the repository and README match the code you submit.
- Do not claim features or tests you have not verified.
