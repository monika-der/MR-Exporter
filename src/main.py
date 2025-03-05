import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_thirty_days_ago():
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    return datetime.datetime.combine(
        thirty_days_ago, datetime.time(8, 0)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_tab_name():
    return datetime.date.today().strftime("%m.%Y").replace(".", "")


def get_merge_request(url, headers):
    response = requests.get(url, headers=headers)
    return response.json()


def post_to_sheet(url, body, headers):
    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    return response.text


def main():
    thirty_days_ago_formatted = get_thirty_days_ago()
    tab_name = get_tab_name()

    sheety_base_url = os.getenv("SHEETY_BASE_URL")
    gitlab_base_url = os.getenv("GITLAB_BASE_URL")
    gitlab_headers = {"Private-Token": os.getenv("GITLAB_PRIVATE_TOKEN")}
    sheety_headers = {
        "Authorization": f"Bearer {os.getenv('SHEETY_BEARER_TOKEN')}",
        "Content-Type": "application/json"
    }
    author_username = os.getenv("AUTHOR_USERNAME")

    sheety_url = f"{sheety_base_url}{tab_name}"
    gitlab_url = (
        f"{gitlab_base_url}?created_after={thirty_days_ago_formatted}"
        f"&author_username={author_username}&per_page=100"
    )

    merge_requests = get_merge_request(gitlab_url, gitlab_headers)

    for mr in merge_requests:
        if "Develop" in mr["title"] or "master" in mr["title"]:
            continue
        body = {
            tab_name: {
                "title": mr["title"],
                "date": mr["created_at"].split("T")[0],
                "giturl": mr["web_url"],
            }
        }
        response_text = post_to_sheet(sheety_url, body, sheety_headers)
        print(response_text)


if __name__ == "__main__":
    main()
