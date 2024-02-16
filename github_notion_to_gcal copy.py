# crontab -e


import os
from notion_client import Client
from datetime import datetime, timedelta
import requests

from collections import defaultdict


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Notion events -> Google Calendar
# Get all the database items from Notion
# See if the item is already in the Google Calendar
# If not, add it to the Google Calendar

NOTION_TOKEN =  # Add your Notion token
DATABASE_ID =  # Add your Notion database ID

SCOPES = ["https://www.googleapis.com/auth/calendar"]


notion_time =  datetime.now().strftime("%Y-%m-%dT%H:%M:%S-04:00") #has to be adjusted for when daylight savings is different

HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

class Task:
    def __init__(self, id, title, course, date):
        self.id = id
        self.title = title
        self.course = course
        self.date = date



# Get all the database items from Notion
# Parameters: 
        # num_pages - the number of pages of items to retrieve from the database
# Returns: a list of Task objects
def get_notion_data(num_pages=None):

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    get_all = num_pages is None
    
    
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=HEADERS)

    data = response.json()
    
    #print(data)
    all_tasks = []

    for task in data["results"]:

        task_id = task["properties"]["ID"]["unique_id"]["prefix"]+str(task["properties"]["ID"]["unique_id"]["number"])
        task_title = task["properties"]["Task name"]["title"][0]["text"]["content"]
        task_course = task["properties"]["Course name"]["multi_select"][0]["name"]
        task_date = task["properties"]["Final deadline"]["date"]["start"]

        
        all_tasks.append(Task(task_id, task_title, task_course, task_date))
    return all_tasks

# Create new events in the Google Calendar for all the tasks in the Notion database that don't already have an event
# Parameters: service - the Calendar API service object
#             notion_tasks - the list of tasks from the Notion database
#             existing_ids - a dictionary of task IDs that already have an event in the Google Calendar
# Returns: None
def create_events(service, notion_tasks, existing_ids):
    for task in notion_tasks:
        if existing_ids[task.id]:
            print(f"Event already exists for {task.title}")
            continue    
        # Parse the start time string
        end_time_str = task.date
        end_time = datetime.fromisoformat(end_time_str)

        # Calculate the end time to be an hour later than the start time
        start_time = end_time - timedelta(hours=1)
        # Format the end time as a string
        start_time_str = start_time.isoformat()

        event = {
            'summary': task.title,
            'location': task.course,
            'description': task.id, 
            'start': {
                'dateTime': start_time_str,
                'timeZone': 'Europe/Stockholm',
            },
            'end': {
                'dateTime': end_time_str,
                'timeZone': 'Europe/Stockholm',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        # Call the API to create the event
        event = service.events().insert(calendarId='primary', body=event).execute()
        print (f'Event created: {task.title} for course {task.course}')

    return 
# Get all the event IDs from the Google Calendar
# Parameters: 
        # service - the Calendar API service object
# Returns: a dictionary of event IDs
def get_gcal_event_ids(service):

    task_ids = defaultdict(lambda: False)


    now = datetime.utcnow()
    three_months_later = now + timedelta(days=30*4)

    # Format the dates as per RFC3339
    time_min = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    time_max = three_months_later.isoformat() + 'Z'

    # Call the API to retrieve events within the specified time range
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,  # Expand recurring events into instances
        orderBy='startTime'
    ).execute()

    # Extract the events from the response
    events = events_result.get('items', [])



    if events:
        for event in events:
            if 'description' in event:
                task_ids[event['description']] = True
            


    return task_ids


def main():
    # Load the credentials from the file token.json
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Calendar API service
    service = build('calendar', 'v3', credentials=creds)

    
    notion_data = get_notion_data()
    existing_gcal_events = get_gcal_event_ids(service)
    create_events(service, notion_data, existing_gcal_events)


if __name__ == "__main__":
     main()