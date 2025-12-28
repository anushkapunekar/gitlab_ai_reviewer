def review_merge_request(changes: dict) -> dict:
    """
    Simple AI Review Agent (v1 – no LLM yet)

    Takes GitLab MR changes JSON and returns a structured review.
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
    """
    Converts review dict into a human-readable GitLab MR comment.
    """
    return f"""
🤖 **AI Code Review**

**Files Changed:** {", ".join(review["files_changed"])}
**Total Files:** {review["total_files"]}
**Additions:** {review["additions"]}
**Deletions:** {review["deletions"]}

📝 **Verdict:**  
{review["verdict"]}
"""
