from app.gitlab.client import GitLabClient
from app.auth.token_store import gitlab_token_store
from app.agent.reviewer import multi_agent_review

def handle_merge_request(payload: dict, post_comment: bool = True):
    project_id = payload["project"]["id"]
    mr_iid = payload["object_attributes"]["iid"]

    token = gitlab_token_store.get("default_user")
    if not token:
        raise RuntimeError("No GitLab OAuth token found. Please login first.")

    client = GitLabClient(token)

    # 1️⃣ Fetch MR changes
    changes = client.get_merge_request_changes(project_id, mr_iid)

    # 2️⃣ Run AI (multi-agent)
    review_text = multi_agent_review(changes)

    # 3️⃣ Post comment ONLY if allowed
    if post_comment:
        client.post_merge_request_comment(
            project_id,
            mr_iid,
            review_text
        )

    # 4️⃣ Always return review
    return {
        "review": review_text
    }
