from datetime import datetime, timedelta
from dateparser import parse
import re

def extract_dates(text):
    found = []
    patterns = [
        r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b',
        r'\b\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b',
        r'\b(?:mon|tue|wed|thu|fri|sat|sun)[a-z]*\b',
        r'\b\d{1,2}:\d{2}\b'
    ]
    for p in patterns:
        for m in re.findall(p, text, flags=re.IGNORECASE):
            dt = parse(m)
            if dt:
                found.append(dt)
    search = parse(text, settings={'PREFER_DATES_FROM': 'future'})
    if search:
        found.append(search)
    return found

def build_weekly_timetable(notices):
    now = datetime.now()
    week = {i: [] for i in range(7)}
    for n in notices:
        text = n.get("text") or n.get("summary") or ""
        dates = extract_dates(text)
        if not dates:
            continue
        dates = [d for d in dates if d >= now - timedelta(hours=1)]
        if not dates:
            continue
        d = min(dates)
        weekday = d.weekday()
        event = {
            "title": (n.get("summary") or text)[:120],
            "priority": n.get("priority", "Normal"),
            "time": d.strftime("%Y-%m-%d %H:%M")
        }
        week[weekday].append(event)
    names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    return {names[i]: week[i] for i in range(7) if week[i]}
