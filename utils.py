from pylatex.utils import bold


class ClassRow:
    def __init__(self, text, bold=False):
        self.text = text
        self.bold = bold


def add_class(t, c, b=False):
    if b:
        c = bold(c)
    t.add_hline()
    t.add_row([c])


def add_classes(t, classes):
    for c in classes:
        add_class(t, c.text, c.bold)
    t.add_hline()
    return t


def get_csv(t, fd, ld):
    import requests

    if t == 1:
        hlm = "4"
        acm = "1"
        file_name = "s.csv"
    elif t == 2:
        hlm = "3"
        acm = "2"
        file_name = "h.csv"
    else:
        exit()
    url = "https://downloads.salahtimes.com/api/prayerDownload"
    headers = {
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
    }

    params = {
        "format": "csv",
        "country": "uk",
        "place": "bristol",
        "hlm": hlm,
        "pcm": "5",
        "acm": acm,
        "ds": fd.strftime("%Y-%m-%d"),
        "de": ld.strftime("%Y-%m-%d"),
        "as24": "true",
    }

    response = requests.get(url, headers=headers, params=params)

    with open(file_name, "wb") as file:
        file.write(response.content)


def get_formatted_data():
    import pandas as pd

    s_data = pd.read_csv("s.csv")
    h_data = pd.read_csv("h.csv")
    s_data.insert(loc=5, column="Asr Hanafi", value=h_data["Asar"])
    s_data = s_data.rename(columns={"Asar": "Asr Shafi"})
    x = s_data["Date"].str.split(" ", expand=True)[[0, 1]]
    s_data[["Date"]] = x[[1]]
    s_data.insert(loc=1, column="Day", value=x[[0]])
    s_data[["Isha"]] = h_data[["Isha"]]
    return s_data


def add_ramadan_columns(dt):
    dt.insert(loc=0, column="Hijri", value=[x for x in range(1, 31)])
    dt.insert(
        loc=10,
        column="Taraweeh",
        value=["19:20"] * 10 + ["19:40"] * 10 + ["20:00"] * 9 + ["N/A"],
    )
    return dt
