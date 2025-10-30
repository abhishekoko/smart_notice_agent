import os
from dateparser import parse
from datetime import datetime, timedelta
import pytz

DEFAULT_TZ = os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")

def extract_deadline(text):
    return parse(text, settings={
        'PREFER_DATES_FROM': 'future',
        'RELATIVE_BASE': datetime.now(pytz.timezone(DEFAULT_TZ))
    })

def get_priority_level(text, deadline=None):
    now = datetime.now(pytz.timezone(DEFAULT_TZ))
    priority = "Low"

    critical_kw = ["immediate", "mandatory", "must submit", "final warning", "asap", "deadline"]
    high_kw = ["urgent", "final notice", "important", "required", "strictly enforced"]

    txt = text.lower()
    if any(k in txt for k in critical_kw):
        priority = "Critical"
    elif any(k in txt for k in high_kw):
        priority = "High"

    if deadline:
        if not deadline.tzinfo:
            deadline = pytz.timezone(DEFAULT_TZ).localize(deadline)
        delta = deadline - now
        if delta.total_seconds() <= 0:
            return "CRITICAL (PASSED)"
        if delta < timedelta(hours=48):
            return "Critical"
        if delta < timedelta(days=7) and priority != "Critical":
            priority = "High"
        elif delta < timedelta(days=30) and priority not in ["Critical", "High"]:
            priority = "Medium"

    return priority
