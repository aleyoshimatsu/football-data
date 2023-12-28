from datetime import datetime


def get_last_mod_date(link):
    date = link.nextSibling.strip()[:11]
    date = str(datetime.strptime(date, "%d-%b-%Y").date())
    return date


def get_upper_level(url):
    base = url[:-1].split("/")
    head = "/".join(base[:3])
    tail = base[-1]
    upper_level = url[:-1].replace(head, "").replace(tail, "")
    return upper_level
