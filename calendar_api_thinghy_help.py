from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from what_day_is_friday import day
import urllib.request
import datetime
import os.path

#why are the tabs a space?
#idk, but it works so idgaf

#scheduley thingy
times = [[0, '9:50', '10:30', 'Monday SOURCE'], [0, '10:30', '11:50', 'Monday Block 2'], [0, '12:35', '13:55', 'Monday Block 3'],
         [1, '9:50', '10:30', 'Tuesday SOURCE'], [1, '12:35', '15:20', 'Tuesday Block 3+4'],
         [2, '9:50', '10:30', 'Wednesday SOURCE'], [2, '10:30', '11:50', 'Wednesday Block 2'], [2, '12:35', '13:55', 'Wednesday Block 3'],
         [3, '8:30', '9:50', 'Thursday Block 1'], [3, '9:50', '10:30', 'Thursday SOURCE'], [3, '10:30', '11:50', 'Thursday Block 2']]

friday = day()

if friday == "d1":
  times.append( [4, '9:44', '10:55', 'Friday Block 2'], [4, '11:35', '12:46', 'Friday Block 3'])


#?
SCOPES = ["https://www.googleapis.com/auth/calendar"]

#test connection so if no internet you no get long confusing error, just no internet error
def test_internet_connection():
    try:
        urllib.request.urlopen('http://google.com', timeout=0.1)
        return True
    except urllib.error.URLError as e:
        print(f"Error testing internet connection: {e.reason}")
        return False
    
def checker_thingy(service):
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

    for event in events:
     print(event["summary"])
    
#Don't you just love dealing with time
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
      raise TimeoutError("No Internet Connection")
      #Rip internet
      
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
    
    checker_thingy(service)
    
    print("\n")
    
    for block in times:

        title = input(block[3] + " Title: ") 
        if title.lower() != "":
            event = {
            'summary': title,
            'location': 'Westmount Charter School',
            'description': input(block[3] + " Description: "),
            'start': {
                'dateTime': get_rfc_3323_or_something_time(block[1], block[0]),
                'timeZone': 'America/Edmonton',
            },
            'end': {
                'dateTime': get_rfc_3323_or_something_time(block[2], block[0]),
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

            event = service.events().insert(calendarId='d7b7f5a00e33139545a6d2bb34ee14c79f06612a86907e24bc7a657b98348b52@group.calendar.google.com', body=event).execute()


  except HttpError as error:
    print(f"Something went wrong: {error}")

#python boilerplate is real
#forget public static void main(string args[]) just use if __name == "__main__"
if __name__ == "__main__":
  main()