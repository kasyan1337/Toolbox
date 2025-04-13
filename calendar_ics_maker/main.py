import re
from datetime import datetime, timedelta

import pytz
from icalendar import Calendar, Event, Alarm

# Define Bratislava timezone
bratislava_tz = pytz.timezone("Europe/Bratislava")

# Create a calendar
cal = Calendar()
cal.add("prodid", "-//Your Product//Your Calendar//EN")
cal.add("version", "2.0")

events_example = [
    {
        "name": "Someone's Birthday",  # Mandatory: Name of the event, a descriptive title for the event.
        "day": 13,  # Mandatory: Day of the event (1-31 depending on the month)
        "month": 5,  # Mandatory: Month of the event (1-12)
        "year": 2024,  # Mandatory: Year of the event (4-digit format, e.g., 2024)
        "start_time": "09:00",  # Optional: Event start time in HH:MM format, defaults to "09:00" if not specified
        "end_time": "12:00",  # Optional: Event end time in HH:MM format, defaults to "12:00" if not specified
        "recurrence": "YEARLY",  # Optional: Event recurrence frequency.
        # Options:
        #   - "YEARLY": Repeats every year on the same date.
        #   - "MONTHLY": Repeats every month on the same day.
        #   - "WEEKLY": Repeats every week on the same day.
        #   - "DAILY": Repeats every day.
        #   - None: No recurrence (default if not specified).
        "is_all_day": False,  # Optional: If True, sets the event as an all-day event without a specific start or end time.
        # Defaults to False. If set to True, "start_time" and "end_time" are ignored.
        "alerts": [
            "PT0M",
            "PT5M",
            "PT30M",
            "P1D",
        ],  # Optional: List of reminders for the event in ISO 8601 duration format.
        # Examples:
        #   - "PT0M": Alert at the exact time of the event.
        #   - "PT5M": Alert 5 minutes before the event.
        #   - "PT30M": Alert 30 minutes before the event.
        #   - "P1D": Alert 1 day before the event.
        #   - "P6M": Alert 6 months before the event.
        #   - "P2W3DT4H30M": Alert 2 weeks, 3 days, 4 hours, and 30 minutes before the event.
        #   - "PT45S": Alert 45 seconds before the event.
        # You can add multiple alerts as needed.
        # COUNTDOWN
        # "alerts": lambda: [f"PT{seconds}S" for seconds in range(10, 0, -1)],
    }
]

events = [
    {
        "name": "Test1",
        "day": 28,
        "month": 10,
        "year": 2024,
        "start_time": "20:00",
        "end_time": "22:00",
        "recurrence": "YEARLY",
        "alerts": ["PT0M", "PT5M", "PT30M", "P1D"],
        "is_all_day": False,
    },
    # Add more events as needed
]


# Function to parse ISO 8601 duration to timedelta
def parse_iso_duration(duration):
    # Supports durations like 'PT30M', 'P1D', 'PT1H30M', etc.
    pattern = re.compile(
        r"P"  # starts with 'P'
        r"(?:(?P<weeks>\d+)W)?"  # weeks
        r"(?:(?P<days>\d+)D)?"  # days
        r"(?:T"  # time part begins with 'T'
        r"(?:(?P<hours>\d+)H)?"  # hours
        r"(?:(?P<minutes>\d+)M)?"  # minutes
        r"(?:(?P<seconds>\d+)S)?"  # seconds
        r")?$"  # end of string
    )
    match = pattern.match(duration)
    if not match:
        return timedelta()
    parts = match.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            if name == "weeks":
                time_params["days"] = time_params.get("days", 0) + int(param) * 7
            else:
                time_params[name] = int(param)
    return timedelta(**time_params)


# Iterate over the events and add them to the calendar
for event in events:
    try:
        vevent = Event()
        vevent.add("summary", event["name"])

        # Handle all-day events
        if event.get("is_all_day", False):
            # Set the date without time or timezone for all-day events
            dt_start = datetime(event["year"], event["month"], event["day"]).date()
            vevent.add("dtstart", dt_start)
            vevent.add(
                "dtend", dt_start + timedelta(days=1)
            )  # All-day events end on the next day
        else:
            # Provide default start and end times if not present
            start_time = event.get("start_time", "09:00")
            end_time = event.get("end_time", "12:00")

            # Format the start and end times with the given year, month, and day in the Bratislava timezone
            start_datetime = datetime.strptime(
                f'{event["year"]}-{event["month"]:02d}-{event["day"]:02d} {start_time}',
                "%Y-%m-%d %H:%M",
            )
            end_datetime = datetime.strptime(
                f'{event["year"]}-{event["month"]:02d}-{event["day"]:02d} {end_time}',
                "%Y-%m-%d %H:%M",
            )

            # Set timezone to Bratislava
            start_datetime = bratislava_tz.localize(start_datetime)
            end_datetime = bratislava_tz.localize(end_datetime)

            vevent.add("dtstart", start_datetime)
            vevent.add("dtend", end_datetime)

        # Add recurrence if specified
        recurrence = event.get("recurrence")
        if recurrence:
            vevent.add("rrule", {"FREQ": recurrence.upper()})

        # Get alerts from the event
        alerts = event.get("alerts", [])
        # If 'alerts' is callable (e.g., lambda function), call it to get the list
        if callable(alerts):
            alerts = alerts()
        # Ensure 'alerts' is a list
        if not isinstance(alerts, list):
            alerts = [alerts]

        # Remove duplicates if any
        alerts = list(set(alerts))

        # Add alerts if specified
        for alert in alerts:
            # Parse the ISO 8601 duration
            trigger_timedelta = parse_iso_duration(alert)
            # Create an alarm
            alarm = Alarm()
            alarm.add("action", "DISPLAY")
            alarm.add("description", f'Reminder: {event["name"]}')
            # Set the trigger time (negative timedelta before the event)
            alarm.add("trigger", -trigger_timedelta)
            vevent.add_component(alarm)

        # Add the event to the calendar
        cal.add_component(vevent)
    except Exception as e:
        print(f"Error processing event '{event['name']}': {e}")

# Save to a .ics file
with open("output/Add_to_calendar.ics", "wb") as f:
    f.write(cal.to_ical())

print("Calendar saved with events and alerts.")
