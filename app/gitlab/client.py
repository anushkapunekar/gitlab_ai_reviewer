import requests

print("✅ client.py loaded")


class GitLabClient:
    def __init__(self, token: str):
        self.base_url = "https://gitlab.com/api/v4"
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def get_merge_request_changes(self, project_id: int, mr_iid: int):
        url = f"{self.base_url}/projects/{project_id}/merge_requests/{mr_iid}/changes"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post_merge_request_comment(self, project_id: int, mr_iid: int, comment: str):
        url = f"{self.base_url}/projects/{project_id}/merge_requests/{mr_iid}/notes"

        payload = {
            "body": comment
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
