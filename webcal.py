import urllib.request
import icalendar
with urllib.request.urlopen('https://calendar.google.com/calendar/ical/wcs-g.com_k3p3pmggnsorg805c1rvph0kig%40group.calendar.google.com/public/basic.ics') as f:
    html = f.read().decode('utf-8')
    calendar = icalendar.Calendar.from_ical(html)

for event in calendar.walk('VEVENT'):
    if event.get("SUMMARY") in ['d1', 'd2']:
        print(event.get("SUMMARY"))