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

CALENDAR = '1499bd19b08c7d97abf3d908425280d1e7ce4e6d1200cc6191e87d716ca64ae4@group.calendar.google.com'

#?
SCOPES = ["https://www.googleapis.com/auth/calendar"]

#test connection so if no internet you no get long confusing error, just no internet error
def test_internet_connection() -> bool:
    try:
        urllib.request.urlopen('http://calendar.google.com', timeout=0.5)
        return True
    except urllib.error.URLError:
        return False
      
def build_event(summary, start_time, end_time, start_day, end_day = None, location = "Westmount Charter School"):
  if end_day == None:
    end_day = start_day
    
  event = {
            'summary': summary,
            'location': location,
            'start': {
                'dateTime': get_rfc_3323_or_something_time(start_time, start_day),
                'timeZone': 'America/Edmonton',
            },
            'end': {
                'dateTime': get_rfc_3323_or_something_time(end_time, end_day),
                'timeZone': 'America/Edmonton',
            },
            'reminders': {
                'useDefault': False, 
                'overrides': [
                {'method': 'popup', 'minutes': 10},
                {'method': 'popup', 'minutes': 5},
                ],
            },
            'colorId' : "10"
            }
  return event
        
def get_rfc_3323_or_something_time(time_str, day_of_week = 0, offset_day = 0):
    #Fun fact: today = today, but Today != today, it equals today is not defined
    today = datetime.date.today()
    days_difference = day_of_week - today.weekday()

    # thing and math and stuff idk ask chatgtp
    if days_difference < 0:
        days_difference += 7
    desired_date = today + datetime.timedelta(days=days_difference) + datetime.timedelta(offset_day)
    desired_time = datetime.datetime.strptime(time_str, "%H:%M").time()
    desired_datetime = datetime.datetime.combine(desired_date, desired_time)

    #Make if right format or else google will send assasin
    rfc3339_format = desired_datetime.isoformat(timespec='seconds')

    return rfc3339_format

#the feeder main is broken again
def main():

  if test_internet_connection() == False:
      #Rip internet
      print("No internet connection")
      print("Exiting...")
      sys.exit(int(datetime.datetime.now().strftime("%H%M")))

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
        if event["summary"] in ['d1', 'd2']:
          print(event["start"]["date"])
          print(event["summary"])
          if event["summary"] == 'd1':
              summary = "Day 1"
          if event["summary"] == 'd2':
              summary = "Day 2"
          
          event = {
              'summary': summary,
              'location': 'Westmount Charter School',
              'start': {
                  'date': event["start"]["date"]
              },
              'end': {
                  'date': event["end"]["date"] #(next_friday + datetime.timedelta(days=1)).isoformat()
              },
              'colorId': "10"
          }

          event = service.events().insert(calendarId=CALENDAR, body=event).execute()
          if summary == "Day 1":
            event = {
            'summary': "Innovations",
            'location': 'Westmount Charter School',
            'start': {
                'dateTime': get_rfc_3323_or_something_time("8:30", 4),
                'timeZone': 'America/Edmonton',
            },
            'end': {
                'dateTime': get_rfc_3323_or_something_time("9:40", 4),
                'timeZone': 'America/Edmonton',
            },
            'reminders': {
                'useDefault': False, 
                'overrides': [
                {'method': 'popup', 'minutes': 10},
                {'method': 'popup', 'minutes': 5},
                ],
            },
            'colorId' : "10"
            }
            event = service.events().insert(calendarId=CALENDAR, body=event).execute()
            service.events().insert(calendarId=CALENDAR, body=build_event("Math", "9:44", "10:55", 4)).execute()
            
          if summary == "Day 2":
            event = {
            'summary': "IMBY",
            'location': 'Westmount Charter School',
            'start': {
                'dateTime': get_rfc_3323_or_something_time("8:30", 4),
                'timeZone': 'America/Edmonton',
            },
            'end': {
                'dateTime': get_rfc_3323_or_something_time("9:40", 4),
                'timeZone': 'America/Edmonton',
            },
            'reminders': {
                'useDefault': False, 
                'overrides': [
                {'method': 'popup', 'minutes': 10},
                {'method': 'popup', 'minutes': 5},
                ],
            },
            'colorId' : "10"
            }
            event = service.events().insert(calendarId=CALENDAR, body=event).execute()
            service.events().insert(calendarId=CALENDAR, body=build_event("Gym", "12:50", "2:00", 4)).execute()
          
        if event["summary"] in "no school":
          print(event["start"]["date"])
          print(event["summary"])
          summary = "No School"
          event = {
              'summary': summary,
              'location': 'Westmount Charter School',
              'start': {
                  'date': event["start"]["date"]
              },
              'end': {
                  'date': event["end"]["date"]
              },
              'colorId': "10"
          }

          event = service.events().insert(calendarId=CALENDAR, body=event).execute()
            
      except Exception as f:
        # print(f)
        pass

  except HttpError as error:
    print(f"Something went wrong: {error}")

#python boilerplate is real
#forget public static void main(string args[]) just use if __name == "__main__"
if __name__ == "__main__":
  main()