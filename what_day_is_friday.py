from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request 
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import urllib.request
import datetime
import os.path
import base64
import sys

#?
SCOPES = ["https://www.googleapis.com/auth/calendar"]

#test connection so if no internet you no get long confusing error, just no internet error
def test_internet_connection() -> bool:
    try:
        urllib.request.urlopen('http://calendar.google.com', timeout=0.5)
        return True
    except urllib.error.URLError:
        return False
    
def checker_thingy(service) -> None:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("R.I.P. your social life")
      return
  
#Don't you just love dealing with time
def get_rfc_3323_or_something_time(time_str, day_of_week=0) -> str:
    #Fun fact: today = today, but Today != today, it equals today is not defined
    today = datetime.date.today()
    days_difference = day_of_week - today.weekday()

    # thing and math and stuff idk ask chatgtp
    if days_difference < 0:
        days_difference += 7
    desired_date = today + datetime.timedelta(days=days_difference)
    desired_time = datetime.datetime.strptime(time_str, "%H:%M").time()
    desired_datetime = datetime.datetime.combine(desired_date, desired_time)

    #Make if right format or else google will send assasin
    rfc3339_format = desired_datetime.isoformat(timespec='seconds')

    return rfc3339_format

#i am not good at naming things
def function(thing):
    if thing == "d1":
        return "Day 1"
    if thing == "d2":
        return "Day 2"

def day():

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
            calendarId=base64.b64decode("d2NzLWcuY29tX2szcDNwbWdnbnNvcmc4MDVjMXJ2cGgwa2lnQGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20=").decode("ascii"),
            timeMin=now,
            maxResults=30,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("Paget is dead or something")
      return 
    
    for event in events:
        # Update this section in your main function
        if event["summary"] in ['d1', 'd2']:
            return event["summary"]
        
  except HttpError as error:
    print(f"Something went wrong: {error}")

#the feeder main is broken again
def main() -> None:

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
            calendarId=base64.b64decode("d2NzLWcuY29tX2szcDNwbWdnbnNvcmc4MDVjMXJ2cGgwa2lnQGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20=").decode("ascii"),
            timeMin=now,
            maxResults=30,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("Paget is dead or something")
      return
    
    for event in events:
        # Update this section in your main function
        if event["summary"] in ['d1', 'd2']:
            print("The next friday is " + function(event["summary"]))
            break


  except HttpError as error:
    print(f"Something went wrong: {error}")
    
#python boilerplate is real
#forget public static void main(string args[]) just use if __name == "__main__"
if __name__ == "__main__":
  main()