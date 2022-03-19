from datetime import datetime
from typing import Optional

import pytz


def make_timezone_aware_datetime(timestamp: Optional[datetime] = datetime.utcnow(), tz_name: Optional[str] = "Etc/GMT") -> datetime:
    timezone = pytz.timezone(tz_name)
    return timezone.localize(timestamp)
