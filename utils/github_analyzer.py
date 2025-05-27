import requests
from urllib.parse import urlparse
import base64

def is_github_url(url):
    parsed = urlparse(url)
    return "github.com" in parsed.netloc and len(parsed.path.strip("/").split("/")) >= 2

def get_repo_info(repo_url):
    try:
        owner, repo = repo_url.strip("/").split("/")[-2:]
        repo = repo.replace(".git", "")
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        readme_url = f"{api_url}/readme"

        repo_data = requests.get(api_url).json()
        readme_data = requests.get(readme_url).json()

        if "content" in readme_data and readme_data["content"]:
            readme_content = base64.b64decode(readme_data["content"]).decode("utf-8", errors="ignore")
        else:
            readme_content = ""

        return {
            "readme": readme_content,
            "description": repo_data.get("description", "No description available."),
            "language": repo_data.get("language", "Unknown")
        }

    except Exception as e:
        return {"error": f"Error fetching repo info: {str(e)}"}
