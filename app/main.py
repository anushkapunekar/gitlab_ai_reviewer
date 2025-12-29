import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.gitlab.client import GitLabClient
from app.agent.reviewer import multi_agent_review
from app.webhooks.gitlab import router as gitlab_webhook_router
from app.auth.gitlab_oauth import router as gitlab_auth_router
from app.ci.ai_review import router as ci_router

load_dotenv()

app = FastAPI(title="GitLab AI Reviewer")

# ✅ THIS is the correct way
app.include_router(gitlab_webhook_router)
app.include_router(gitlab_auth_router)
app.include_router(ci_router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "gitlab-ai-reviewer"}

@app.get("/test-mr")
def test_mr():
    token = os.getenv("GITLAB_TOKEN")

    client = GitLabClient(token)

    project_id = 75985254
    mr_iid = 2

    changes = client.get_merge_request_changes(project_id, mr_iid)

    review = multi_agent_review(changes)

    return review
