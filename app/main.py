import os
from fastapi import FastAPI
from app.gitlab.client import GitLabClient
from app.agent.reviewer import review_merge_request

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GitLab AI Reviewer")

@app.get("/test-mr")
def test_mr():
    token = os.getenv("GITLAB_TOKEN")

    client = GitLabClient(token)

    project_id = 75985254
    mr_iid = 2

    changes = client.get_merge_request_changes(project_id, mr_iid)

    review = review_merge_request(changes)

    return review
