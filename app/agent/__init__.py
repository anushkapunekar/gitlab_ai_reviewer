def review_merge_request(changes: dict) -> dict:
    """
    AI REVIEW AGENT (v1)

    Input:
        - GitLab MR changes JSON

    Output:
        - Structured review result
    """

    files = []
    additions = 0
    deletions = 0

    for change in changes.get("changes", []):
        files.append(change["new_path"])

        diff = change.get("diff", "")
        additions += diff.count("\n+")
        deletions += diff.count("\n-")

    summary = {
        "files_changed": files,
        "total_files": len(files),
        "additions": additions,
        "deletions": deletions,
        "verdict": "Initial review completed"
    }

    return summary
