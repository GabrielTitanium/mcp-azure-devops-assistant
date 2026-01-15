from dotenv import load_dotenv
load_dotenv()

import os
import base64
import requests

class AzureDevOpsClient:
    def __init__(self):
        self.org = os.getenv("AZDO_ORG")
        self.project = os.getenv("AZDO_PROJECT")
        self.pat = os.getenv("AZDO_PAT")

        if not self.org or not self.project or not self.pat:
            raise ValueError("Missing Azure DevOps environment variables")

        self.base_url = f"https://dev.azure.com/{self.org}/{self.project}"

        token = base64.b64encode(f":{self.pat}".encode()).decode()

        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }

    def list_pipelines(self):
        url = f"{self.base_url}/_apis/pipelines?api-version=7.1-preview.1"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
