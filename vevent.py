from datetime import datetime
import re

"""
vevent.py
=========

github: https://github.com/redmechanic/vevent.py

Extracts basic info on all events in an iCalendar file (.ics).
For example, to get the summary of the first event on 2017-1-18:
    
    calendar = vevent.Calendar(TEXT_FROM_FILE)
    events_on_day = calendar.events[2017][1][18]
    print(events_on_day[0].summary)

Or:

    calendar = vevent.Calendar(TEXT_FROM_FILE)
    events_on_day = calendar.get_events_on_day(datetime.datetime(2017, 1, 18))
    print(events_on_day[0].summary)

The start date of an event is always used as the key.
Does not deal with timezones.
"""

class Calendar:
    """
    Extracts simple events from the contents of a .ics (icalendar) file.
    Calendar.events is in the form of a nested dictionary:
        events = {2017:{1:{18:[Event(), Event(), Event()]}}}
    """
    
    def __init__(self, contents):
        self.__parse(self.__unwrap(contents))
    
    def __stamp_to_datetime(self, stamp):
        return datetime.strptime(stamp, "%Y%m%dT%H%M%S")
    
    def __unwrap(self, content):
        lines = content.splitlines()
        for i in range(len(lines) - 1, 0, -1):
            if lines[i][0] == " ":
                lines[i - 1] += lines[i][1:]
                lines.pop(i)
        return "\n".join(lines)
    
    def __unformat(self, s):
        replacements = {r"\n":"\n", r"\,":","}
        for k in replacements:
            s = s.replace(k, replacements[k])
        return s
    
    def __parse(self, content):
        self.events = {}
        event = None
        for line in content.splitlines():
            
            if line == "BEGIN:VEVENT":
                event = Calendar.Event()
                
            elif line == "END:VEVENT":
                if event.start.year not in self.events:
                    self.events[event.start.year] = {}
                if event.start.month not in self.events[event.start.year]:
                    self.events[event.start.year][event.start.month] = {}
                if event.start.day not in self.events[event.start.year][event.start.month]:
                    self.events[event.start.year][event.start.month][event.start.day] = []
                
                self.events[event.start.year][event.start.month][event.start.day].append(event)
                event = None
                
            elif event is not None:
                if re.match("^.+:([0-9]{8}T[0-9]{6})Z?$", line):
                    matches = re.search("^(?:DT)?([A-Z\-]+)(?:;[^:]+)?:([0-9]{8}T[0-9]{6})Z?$", line)
                    setattr(event, matches.group(1).lower(), self.__stamp_to_datetime(matches.group(2)))
                    
                elif re.match("^[A-Z\-]+(;[^:]+)?:.+$", line):
                    matches = re.search("^([A-Z\-]+)(?:;[^:]+)?:(.+)$", line)
                    setattr(event, matches.group(1).lower(), self.__unformat(matches.group(2)))
    
    def get_events_on_day(self, date):
        if date.year in self.events:
            if date.month in self.events[date.year]:
                if date.day in self.events[date.year][date.month]:
                    return self.events[date.year][date.month][date.day]
        return []
    
    def get_current_event(self):
        date = datetime.today()
        for event in self.get_events_on_day(date):
            if event.start < date and event.end > date:
                return event
        return None
    
    def get_next_event(self):
        date = datetime.today()
        for event in self.get_events_on_day(date)[::-1]:
            if event.start > date and event.end > date:
                return event
        return None
    
    class Event:
        def __init__(self):
            self.summary = ""
            self.description = ""
            self.location = ""
            self.start = None
            self.end = None
        
        def get_time_string(self):
            return "{} - {}".format(self.start.strftime("%H:%M"), self.end.strftime("%H:%M"))
        
        def __str__(self):
            return "{}\n{}\n{}".format(self.get_time_string(), self.summary, self.location)
