from datetime import datetime, timedelta

from pylatex.utils import bold

# Get the current date
today = datetime.now()

# Calculate the first day of the next month
fd = datetime(today.year, today.month, today.day)

# Calculate the last day of the next month
# if today.month == 12:
#     ld = datetime(today.year + 1, 1, 1) - timedelta(days=1)
# else:
#     ld = datetime(today.year, today.month + 2, 1) - timedelta(days=1)
ld = datetime(today.year, today.month, 30)


def get_csv(t: int):
    import requests

    if t == 1:
        acm = "1"
        file_name = "s.csv"
    elif t == 2:
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
        "hlm": "4",
        "pcm": "5",
        "acm": acm,
        "ds": fd.strftime("%Y-%m-%d"),
        "de": ld.strftime("%Y-%m-%d"),
        "as24": "true",
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
    else:
        print(f"Error: {response.status_code} - {response.text}")


def get_formatted_data():
    import pandas as pd

    # Read data from "s.csv" and "h.csv"
    s_data = pd.read_csv("s.csv")
    h_data = pd.read_csv("h.csv")
    # print(s_data)
    s_data.insert(loc=5, column="Asr Hanafi", value=h_data["Asar"])
    s_data = s_data.rename(columns={"Asar": "Asr Shafi"})
    x = s_data["Date"].str.split(" ", expand=True)[[0, 1]]
    s_data[["Date"]] = x[[0]]
    s_data.insert(loc=0, column="Day", value=x[[1]])
    s_data.insert(
        loc=9,
        column="Tarawih",
        value=["20:00"] * 15 + ["20:30"] * 14 + ["N/A"],
    )
    return s_data


def gen_doc(df):
    from pylatex import (
        Center,
        Command,
        Document,
        Figure,
        LineBreak,
        Tabular,
    )

    # Create a LaTeX document
    geometry_options = {
        "tmargin": "0in",
        "lmargin": "0in",
        "bmargin": "0in",
        "rmargin": "0in",
    }
    doc = Document(geometry_options=geometry_options, font_size="large")
    doc.append(Command("pagenumbering", "gobble"))
    with doc.create(Center()):
        image_filename = "/home/yazeed/salah-time/logo.png"
        with doc.create(Figure(position="t")) as logo:
            logo.add_image(image_filename, width="69px")

        doc.append(bold("Ramadan timetable"))
        doc.append(LineBreak())
        doc.append(bold(f"{fd.strftime('%a %d %b %Y')} - {ld.strftime('%a %d %b %Y')}"))
        doc.append(LineBreak())
        doc.append("High Latitude Method: Angle Based Rule")
        doc.append(LineBreak())
        doc.append("Prayer Calculation Method: Islamic Society of North America")
        doc.append(LineBreak())

        # Add a table to the document
        with doc.create(
            Tabular("|c|c|c|c|c|c|c|>{\columncolor[gray]{0.9}}c|c|c|", row_height=1.4)
        ) as table:
            table.add_hline()
            table.add_row(df.columns)
            # d = 1
            for i, row in df.iterrows():
                if i % 10 == 0:
                    table.add_hline()
                table.add_hline()
                c = None
                if row[1] == "Fri":
                    c = "lightgray"
                # row[0] = d
                # d += 1
                table.add_row(row, color=c)
            table.add_hline()

        doc.append(LineBreak())
        doc.append(LineBreak())
        doc.append("Prayer times provided by https://www.salahtimes.com")
        doc.append(LineBreak())
        doc.append(bold("uwe.isoc.link/timetable"))

    # Save the document to a PDF file
    doc.generate_pdf("prayer_time")


get_csv(1)
get_csv(2)

data = get_formatted_data()

gen_doc(data)
