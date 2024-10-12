from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import urllib.request
import datetime
import os.path
import sys

#why are the tabs a space?
#idk, but it works so idgaf

#?
SCOPES = ["https://www.googleapis.com/auth/calendar"]

#test connection so if no internet you no get long confusing error, just no internet error
def test_internet_connection() -> bool:
    try:
        urllib.request.urlopen('http://calendar.google.com', timeout=0.5)
        return True
    except urllib.error.URLError:
        return False

#the feeder main is broken again
def main():

  if test_internet_connection() == False:
      #Rip internet
      print("No internet connection")
      print("Exiting...")
      sys.exit(69)
      
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
      #funny webiste
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())
      #oh yeah now this is security

  try:
    service = build("calendar", "v3", credentials=creds)
 
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    events_result = (
        service.events()
        .list(
            calendarId="wcs-g.com_k3p3pmggnsorg805c1rvph0kig@group.calendar.google.com",
            timeMin=now,
            maxResults=10000,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("Paget is dead or something")
    
    for event in events:
      try:
        if event["summary"] in ['d1', 'd2', 'no school', 'november break']:
            print(event["start"]["date"])
            print(event["summary"])
            if event["summary"] == 'd1':
                summary = "Day 1"
            if event["summary"] == 'd2':
                summary = "Day 2"
            if event["summary"] in "no school":
              summary = "No School"
            if event["summary"] in "november break":
              summary = "November Break"
            
            event = {
                'summary': summary,
                'location': 'Westmount Charter School',
                'start': {
                    'date': event["start"]["date"]
                },
                'end': {
                    'date': event["end"]["date"] #(next_friday + datetime.timedelta(days=1)).isoformat()
                },
            }

            event = service.events().insert(calendarId=/'@group.calendar.google.com', body=event).execute()
      except Exception as f:
        pass
  except HttpError as error:
    print(f"Something went wrong: {error}")

#python boilerplate is real
#forget public static void main(string args[]) just use if __name == "__main__"
if __name__ == "__main__":
  main()