import time
from datetime import timedelta
from datetime import datetime as dt


def hour_rounder(t):
    """
    Round the time to the nearest hour

    Parameters
    ----------
    t : datetime
        The time to be rounded

    Returns
    -------
    datetime
        The rounded time
    """
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + timedelta(hours=t.minute // 30))