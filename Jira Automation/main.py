import browser_cookie3
import requests
import pandas as pd
import json

JIRA_URL = "https://servicedesk.fadv.com"
JIRA_DOMAIN = "servicedesk.fadv.com"

# import requests

# JIRA_URL = "https://servicedesk.fadv.com"
# COOKIE_NAME = "JSESSIONID"
# COOKIE_VALUE = "F2E8BE54882773F8160F3820FD93C1FB"

# session = requests.Session()
# session.cookies.set(COOKIE_NAME, COOKIE_VALUE, domain="servicedesk.fadv.com")

# # Example: Get your profile (just to test)
# resp = session.get(f"{JIRA_URL}/rest/api/2/myself")

# if resp.status_code == 200:
#     print("Session is valid!")
#     # print(resp.json())
# else:
#     print(f"Auth failed: {resp.status_code}")

# def load_roster():
#     try:
#         df = pd.read_excel("roster.xlsx")
#         return dict(zip(df["Ticket Tag"].str.lower(), df["Assignee Username"]))
#     except Exception as e:
#         print(f"Error loading roster: {e}")
#         return {}

def get_jira_session_cookie():
    try:
        cj = browser_cookie3.chrome(domain_name=JIRA_DOMAIN)
    except Exception as e:
        print(f"Error reading browser cookies: {e}")
        return None

    cookies = {}
    for cookie in cj:
        if cookie.domain.endswith(JIRA_DOMAIN) and cookie.name.upper() in ["JSESSIONID", "atlassian.xsrf.token"]:
            cookies[cookie.name] = cookie.value

    if cookies:
        print("✅ Found Jira session cookies.")
        for cookie in cookies:
            print("cookie Key: " + cookie)
            print("cookie Value: " + cookies[cookie])
        return cookies
    else:
        print("❌ No valid session cookies found.")
        return None


def fetch_unassigned_tickets(session):
    # Adjust this JQL query as per your project
    jql =  "" #"project = \"Global IT Support\" AND status in (\"In Progress", "To DO\")"
    params = {"jql": jql, "maxResults": 50}
    # print(f"{JIRA_URL}/rest/api/2/search" params=params)
    resp = session.get(f"{JIRA_URL}/rest/api/2/search", params=params)

    print("Response : ", resp)

    if resp.status_code == 200:
        issues = resp.json().get("issues", [])
        with open("ticket_list.txt", "w", encoding="utf-8") as f:
            for issue in issues:
                key = issue["key"]
                summary = issue["fields"]["summary"]
                f.write(f"{key}: {summary}\n")
        return resp.json().get("issues", [])
    else:
        print(f"Error fetching tickets: {resp.status_code}")
        return []

def assign_tickets(session, issues, roster):
    for issue in issues:
        key = issue["key"]
        summary = issue["fields"]["summary"].lower()

        matched = False
        for tag, assignee in roster.items():
            if tag in summary:
                print(f"🎯 {key}: '{summary}' matched with '{tag}' → Assigning to {assignee}")
                assign_issue(session, key, assignee)
                matched = True
                break

        if not matched:
            print(f"⚠️ No match for {key}: '{summary}'")

def assign_issue(session, issue_key, assignee_name):
    url = f"{JIRA_URL}/rest/api/2/issue/{issue_key}/assignee"
    data = {"name": assignee_name}
    resp = session.put(url, json=data)
    if resp.status_code == 204:
        print(f"✅ Assigned {issue_key} to {assignee_name}")
    else:
        print(f"❌ Failed to assign {issue_key}: {resp.status_code} | {resp.text}")
        
def main():
    cookies = get_jira_session_cookie()
    if not cookies:
        return

    session = requests.Session()
    for name, value in cookies.items():
        session.cookies.set(name, value, domain=JIRA_DOMAIN)

    # roster = load_roster()
    # if not roster:
    #     print("⚠️ No valid roster loaded. Aborting.")
    #     return

    issues = fetch_unassigned_tickets(session)
    print(f"📋 Found {len(issues)} unassigned tickets.")
    # assign_tickets(session, issues, roster)

if __name__ == "__main__":
    main()                            