# Add your Notion tasks to your Google Calendar!

This Python script synchronizes tasks from a Notion database to a Google Calendar. It retrieves tasks from a specified Notion database, checks if each task already exists in the Google Calendar, and if not, adds it as an event.

An extra tutorial down is added down below to help you create a schedule that runs the code automatically on regular intervals. 

## Prerequisites

- Python 3.x
- `notion_client` library
- `google-auth` library
- `google-auth-oauthlib` library
- `google-api-python-client` library

## Installation

1. Install the required Python libraries using pip:

```bash
pip install notion_client google-auth google-auth-oauthlib google-api-python-client
```

2. Clone the repo:
```bash
git clone git@github.com:Imrandiva/notion-to-gcal.git
```   

## Usage

1. Set your Notion API token and database ID by creating a developer account and building an integration using Notion [API](https://developers.notion.com/docs/create-a-notion-integration) :



2. Replace the NOTION_TOKEN and DATABASE_ID variables in the code with your Notion token and database ID respectively. 

3. Create a google developer account to use the Google Calendar [API](https://developers.google.com/calendar/api/v3/reference/events)
3. Run the script:

```bash
python notion_to_gcal.py
```

4. Follow the authorization flow to authenticate with Google Calendar.The script will prompt you to authorize access to your Google Calendar.
5. The script will fetch tasks from the Notion database, check if they exist in the Google Calendar, and add them as events if necessary.


## Features

Retrieves tasks from a Notion database.
Checks if tasks already exist in the Google Calendar.
Adds new tasks as events in the Google Calendar.
Handles synchronization for tasks with start time, end time, summary, location, and description.


### Note

Adjust the time zone and other parameters according to your requirements.
Ensure the Notion database schema matches the expected properties used in the script.

For more information, please refer to the official Notion API documentation and Google Calendar API documentation.



## Extra tutorial: Schedule the script to run automatically on a regular basis with Cronjob


1. Move to the directory where your python script is located.
2. Open a crontab file.
 
   ```
   crontab -e
   ```

3. Click on key "A" to edit the new file.
4. Add the script for how frequent the script should run using this format:
   
   ```bash
   [minute: 0-59] [hour: 0-23] [day: 1-31] [months: 1-12] [weekday: 0-6] [path-to-script]
   ```

In my example, I want the script to run at 18:00 on Mondays, Wednesdays, and Fridays:
```bash
0 18 * * 1,3,5 /Users/scripts/notion_script/notion_to_gcal.py
```

For even more examples for using cronjob, click on this [link](https://crontab.guru/examples.html).
