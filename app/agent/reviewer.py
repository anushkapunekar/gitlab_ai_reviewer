from groq import Groq
import os


def review_merge_request(changes: dict) -> dict:
    """
    Simple AI Review Agent (v1 – no LLM yet)
    """

    files = []
    additions = 0
    deletions = 0

    for change in changes.get("changes", []):
        files.append(change.get("new_path"))

        diff = change.get("diff", "")
        additions += diff.count("\n+")
        deletions += diff.count("\n-")

    return {
        "files_changed": files,
        "total_files": len(files),
        "additions": additions,
        "deletions": deletions,
        "verdict": "Initial review completed"
    }


def format_review_comment(review: dict) -> str:
    return f"""
🤖 **AI Code Review**

**Files Changed:** {", ".join(review["files_changed"])}
**Total Files:** {review["total_files"]}
**Additions:** {review["additions"]}
**Deletions:** {review["deletions"]}

📝 **Verdict:**  
{review["verdict"]}
"""


def review_merge_request_llm(changes: dict) -> str:
    """
    LLM-powered AI code review agent
    """

    # ✅ CREATE CLIENT HERE (after env is loaded)
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    diffs_text = ""

    for change in changes.get("changes", []):
        diffs_text += f"\nFile: {change['new_path']}\n{change.get('diff', '')}\n"

    prompt = f"""
You are a senior software engineer reviewing a GitLab Merge Request.

Analyze the following code changes and provide:
1. Summary of what changed
2. Potential bugs or risks
3. Code quality improvements
4. Security or performance concerns (if any)

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
