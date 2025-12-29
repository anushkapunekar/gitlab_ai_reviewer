import requests

class GitLabClient:
    def __init__(self, token: str):
        self.base_url = "https://gitlab.com/api/v4"
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def get_merge_request_changes(self, project_id: int, mr_iid: int):
        url = f"{self.base_url}/projects/{project_id}/merge_requests/{mr_iid}/changes"
        response = requests.get(url, headers=self.headers)

        # Debug (optional)
        print("GET CHANGES STATUS:", response.status_code)

        response.raise_for_status()
        return response.json()

    def post_merge_request_comment(self, project_id: int, mr_iid: int, comment: str):
        url = f"{self.base_url}/projects/{project_id}/merge_requests/{mr_iid}/notes"
        payload = {"body": comment}

        response = requests.post(url, headers=self.headers, json=payload)

        # 🔍 IMPORTANT DEBUG (this tells us WHY 403 happens)
        print("POST COMMENT URL:", url)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        response.raise_for_status()
        return response.json()
