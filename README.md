# vevent.py

Extracts basic info on all events in an iCalendar file (.ics).
For example, to get the summary of the first event on 2017-1-18:
```python 
import vevent
calendar = vevent.Calendar(TEXT_FROM_FILE)
events_on_day = calendar.events[2017][1][18]
print(events_on_day[0].summary)
```
Or:
```python
events_on_day = calendar.get_events_on_day(datetime.datetime(2017, 1, 18))
```
The start date of an event is always used as the key.
Does not deal with timezones.
