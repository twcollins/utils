import requests
from requests.auth import HTTPBasicAuth

# Jira API information
BASE_URL = "https://your-jira-instance.atlassian.net"
EPIC_KEY = "EPIC-123"  # Replace with the key of the epic you want to clone
NEW_EPIC_NAME = "Cloned Epic"  # Replace with the desired name for the new epic

# Jira credentials; todo - externalise 
USERNAME = "your-username"
PASSWORD = "your-password"


def clone_epic(epic_key, new_epic_name):
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    headers = {
        "Content-Type": "application/json"
    }
    
    # Get epic details
    epic_url = f"{BASE_URL}/rest/api/3/issue/{epic_key}"
    response = requests.get(epic_url, headers=headers, auth=auth)
    epic_data = response.json()
    
    # Create new epic
    new_epic_data = {
        "fields": {
            "project": {"key": epic_data['fields']['project']['key']},
            "summary": new_epic_name,
            "issuetype": {"id": epic_data['fields']['issuetype']['id']}
        }
    }
    create_epic_url = f"{BASE_URL}/rest/api/3/issue"
    create_response = requests.post(create_epic_url, json=new_epic_data, headers=headers, auth=auth)
    new_epic_key = create_response.json()['key']
    
    # Get stories in the epic
    epic_stories = epic_data['fields']['customfield_12345']  # Replace with your custom field ID for epic stories
    
    for story in epic_stories:
        # Get story details
        story_url = f"{BASE_URL}/rest/api/3/issue/{story['key']}"
        story_response = requests.get(story_url, headers=headers, auth=auth)
        story_data = story_response.json()
        
        # Create new story
        new_story_data = {
            "fields": {
                "project": {"key": story_data['fields']['project']['key']},
                "summary": story_data['fields']['summary'],
                "issuetype": {"id": story_data['fields']['issuetype']['id']},
                "customfield_12345": [{"key": new_epic_key}]  # Link to the new epic
            }
        }
        create_story_url = f"{BASE_URL}/rest/api/3/issue"
        requests.post(create_story_url, json=new_story_data, headers=headers, auth=auth)
    
    print("Epic cloned successfully!")

if __name__ == "__main__":
    clone_epic(EPIC_KEY, NEW_EPIC_NAME)
