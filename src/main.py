import tkinter as tk
import webbrowser
from tkinter import messagebox
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


def run_script():
    try:
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

        messagebox.showinfo("Success", "Script executed successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_google_sheet(event):
    webbrowser.open_new(os.getenv("GOOGLE_SHEET_URL"))


def open_sheety_dashboard(event):
    webbrowser.open_new(os.getenv("SHEETY_DASHBOARD_URL"))


root = tk.Tk()
root.title("MR Exporter")
large_font = ("Helvetica", 14)

instructions = (
    "1. Create a "
)
text_widget = tk.Text(root, wrap="word", height=10, width=60, font=large_font)
text_widget.insert(tk.END, instructions)
text_widget.insert(tk.END, "Google Sheet", ("link_google_sheet",))
text_widget.insert(tk.END, " with a tab named in the format `MM.YYYY` (e.g., `11.2023`) "
                           "and headers: `giturl`, `date`, `title`.\n\n"
                           "2. Refresh the project in ")
text_widget.insert(tk.END, "Sheety", ("link_sheety_dashboard",))
text_widget.insert(tk.END, " after creating the tab.\n\n"
                           "3. Press 'Run Script' to execute the code.")
text_widget.tag_config("link_google_sheet", foreground="blue", underline=True)
text_widget.tag_bind("link_google_sheet", "<Button-1>", open_google_sheet)
text_widget.tag_config("link_sheety_dashboard", foreground="blue", underline=True)
text_widget.tag_bind("link_sheety_dashboard", "<Button-1>", open_sheety_dashboard)
text_widget.config(state=tk.DISABLED)
text_widget.grid(row=0, column=0, padx=10, pady=10)

run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=1, column=0, pady=10)

root.mainloop()
