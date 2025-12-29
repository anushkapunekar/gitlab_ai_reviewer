import os
from groq import Groq

# -----------------------------
# Helper: get LLM client safely
# -----------------------------
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")
    return Groq(api_key=api_key)

# -----------------------------
# LLM Review Agent (Main)
# -----------------------------
def review_merge_request_llm(changes: dict) -> str:
    client = get_groq_client()

    diffs_text = ""
    for change in changes.get("changes", []):
        diffs_text += f"\nFile: {change['new_path']}\n{change.get('diff', '')}\n"

    prompt = f"""
You are a senior software engineer reviewing a GitLab Merge Request.

Respond in the following EXACT structure:

### Summary
(short summary of changes)

### Issues
(list potential bugs, edge cases, or risks)

### Suggestions
(improvements in code quality, readability, or design)

### Security / Performance
(any security or performance concerns, or say "None")

### Code Quality Score
(give a score out of 10, can be decimal)

Code changes:
{diffs_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a strict but helpful senior code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

# -----------------------------
# Specialized Agents
# -----------------------------
def security_review_agent(diffs_text: str) -> str:
    client = get_groq_client()

    prompt = f"""
You are a security engineer reviewing code changes.

Identify:
- security vulnerabilities
- unsafe patterns
- missing validations
If none, say "No major security concerns."

Code changes:
{diffs_text}
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


def performance_review_agent(diffs_text: str) -> str:
    client = get_groq_client()

    prompt = f"""
You are a performance-focused engineer.

Check for:
- inefficient loops
- unnecessary computations
- scalability concerns
If none, say "No performance issues detected."

Code changes:
{diffs_text}
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


def style_review_agent(diffs_text: str) -> str:
    client = get_groq_client()

    prompt = f"""
You are a senior engineer enforcing clean code standards.

Review for:
- readability
- naming
- structure
- maintainability

Code changes:
{diffs_text}
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# -----------------------------
# Aggregator
# -----------------------------
def multi_agent_review(changes: dict) -> str:
    diffs_text = ""
    for change in changes.get("changes", []):
        diffs_text += f"\nFile: {change['new_path']}\n{change.get('diff', '')}\n"

    summary = review_merge_request_llm(changes)
    security = security_review_agent(diffs_text)
    performance = performance_review_agent(diffs_text)
    style = style_review_agent(diffs_text)

    return f"""
🤖 **AI Code Review (Multi-Agent)**

## General Summary
{summary}

## 🔐 Security Review
{security}

## ⚡ Performance Review
{performance}

## 🎨 Code Style Review
{style}
"""
