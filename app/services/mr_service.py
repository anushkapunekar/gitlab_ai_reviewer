import os
from app.gitlab.client import GitLabClient
from app.agent.reviewer import review_merge_request_llm

def handle_merge_request(payload: dict) -> dict:
    project_id = payload["project"]["id"]
    mr_iid = payload["object_attributes"]["iid"]

    token = os.getenv("GITLAB_TOKEN")
    client = GitLabClient(token)

    changes = client.get_merge_request_changes(project_id, mr_iid)

    # ✅ DEFINE the variable
    review_text = review_merge_request_llm(changes)

    # ✅ USE the same variable
    client.post_merge_request_comment(
        project_id,
        mr_iid,
        review_text
    )

    return {"status": "review_posted"}
