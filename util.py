from datetime import datetime, timedelta


def truncate_string(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    else:
        return text[: max_length - 3] + "..."


# Not efficient at all, but I'm done trying to find efficient ways to do this
# Nothing on the internet when I try to search up "Python pay day on monday
# every two weeks" without it turning into something like today -> next
# monday + 14 days
# Either way, it's bounded by 52 weeks so it's actually probably going to be good enough
def next_payday(day=datetime.now()) -> datetime:
    first_monday = datetime(day.year, 1, 1)
    if first_monday.weekday() != 0:
        days_until_next_monday = (7 - first_monday.weekday()) % 7
        first_monday += timedelta(days=days_until_next_monday)
        first_monday += timedelta(days=7)

    next_payday = first_monday

    # Calculate the next payday within a 14-day period
    while next_payday <= day:
        next_payday += timedelta(days=7)
        if next_payday.weekday() != 0:
            days_until_next_monday = (7 - next_payday.weekday()) % 7
            next_payday += timedelta(days=days_until_next_monday - 1)
        else:
            next_payday += timedelta(days=7)
    next_payday -= timedelta(days=1)

    return next_payday


def rgb_tuple_to_hex(rgb_tuple):
    # Ensure the values are within the valid range
    color = [min(max(0, x), 1) for x in rgb_tuple]
    color = [format(int(x * 255), "02x") for x in color]
    rgb_hex = f"#{color[0]}{color[1]}{color[2]}"
    return rgb_hex
