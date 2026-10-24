import json
import os
import urllib.error
import urllib.request
from flask import Flask, render_template, request

app = Flask(__name__)
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")


def ask_local_model(notes: str) -> dict:
    prompt = f"""
You are SlothBrief, a calm, practical productivity assistant.
Turn the user's notes into a concise plan. Do not invent dates, commitments, or facts.
Return ONLY valid JSON with exactly these keys:
{{"summary":"one or two short sentences","tasks":[{{"title":"clear action","priority":"High|Medium|Low","why":"brief reason"}}],"gentle_tip":"one short, kind suggestion"}}
Include 3 to 6 tasks if the notes support them. Keep wording simple and useful.
If the notes are vague, say so rather than inventing details.

USER NOTES:
{notes}
"""
    payload = json.dumps({
        "model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
        "format": "json", "options": {"temperature": 0.2}
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as response:
        raw = json.loads(response.read().decode("utf-8"))
    result = json.loads(raw["response"])
    if not isinstance(result.get("summary"), str) or not isinstance(result.get("tasks"), list):
        raise ValueError("The model returned JSON in an unexpected format.")
    tasks = []
    for item in result["tasks"][:8]:
        if not isinstance(item, dict):
            continue
        priority = item.get("priority", "Medium")
        if priority not in ("High", "Medium", "Low"):
            priority = "Medium"
        tasks.append({"title": str(item.get("title", "Review this item"))[:180],
                      "priority": priority, "why": str(item.get("why", ""))[:240]})
    return {"summary": result["summary"][:1200], "tasks": tasks,
            "gentle_tip": str(result.get("gentle_tip", "Take one small step at a time."))[:400]}


@app.route("/", methods=["GET", "POST"])
def index():
    notes, result, error = "", None, None
    if request.method == "POST":
        notes = request.form.get("notes", "").strip()
        if not notes:
            error = "Add a few notes first, and I'll help organize them."
        elif len(notes) > 12000:
            error = "Please keep your notes under 12,000 characters."
        else:
            try:
                result = ask_local_model(notes)
            except urllib.error.URLError as exc:
                error = ("I couldn't reach Ollama on this computer. Start Ollama and confirm "
                         f"'{OLLAMA_MODEL}' is installed. Details: {getattr(exc, 'reason', exc)}")
            except (ValueError, KeyError, json.JSONDecodeError) as exc:
                error = f"The local model returned an unexpected response. Try again. Details: {exc}"
            except Exception as exc:
                error = f"Something went wrong while processing your notes: {exc}"
    return render_template("index.html", notes=notes, result=result, error=error, model=OLLAMA_MODEL)


if __name__ == "__main__":
    # Local-only by default; do not expose this development server publicly.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
