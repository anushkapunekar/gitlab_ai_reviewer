import os
import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth/gitlab", tags=["auth"])

GITLAB_AUTH_URL = "https://gitlab.com/oauth/authorize"
GITLAB_TOKEN_URL = "https://gitlab.com/oauth/token"


@router.get("/login")
def gitlab_login():
    params = {
        "client_id": os.getenv("GITLAB_CLIENT_ID"),
        "redirect_uri": os.getenv("GITLAB_REDIRECT_URI"),
        "response_type": "code",
        "scope": "read_api read_repository write_repository"
    }

    url = f"{GITLAB_AUTH_URL}?" + "&".join(
        [f"{k}={v}" for k, v in params.items()]
    )

    return RedirectResponse(url)


@router.get("/callback")
def gitlab_callback(code: str):
    data = {
        "client_id": os.getenv("GITLAB_CLIENT_ID"),
        "client_secret": os.getenv("GITLAB_CLIENT_SECRET"),
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": os.getenv("GITLAB_REDIRECT_URI")
    }

    response = requests.post(GITLAB_TOKEN_URL, data=data)
    response.raise_for_status()

    return response.json()
