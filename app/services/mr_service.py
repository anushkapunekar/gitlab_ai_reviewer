import os
from app.gitlab.client import GitLabClient
from app.agent.reviewer import review_merge_request, format_review_comment

def handle_merge_request(payload: dict) -> dict:
    project_id = payload["project"]["id"]
    mr_iid = payload["object_attributes"]["iid"]

    token = os.getenv("GITLAB_TOKEN")
    client = GitLabClient(token)

    changes = client.get_merge_request_changes(project_id, mr_iid)

    review = review_merge_request(changes)
    comment = format_review_comment(review)

    client.post_merge_request_comment(project_id, mr_iid, comment)

    return review
