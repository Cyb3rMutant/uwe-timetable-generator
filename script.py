from datetime import datetime, timedelta

# Get the current date, 20 days ago
today = datetime.now() - timedelta(days=20)

# Calculate the first day of the next month
# Handle year and month overflow (e.g., December to January)
next_month = today.month % 12 + 1
next_year = today.year + (today.month // 12)
fd = datetime(next_year, next_month, 1)

# Calculate the last day of the next month
# Handle year and month overflow
next_next_month = (today.month + 1) % 12 + 1
next_next_year = today.year + ((today.month + 1) // 12)
ld = datetime(next_next_year, next_next_month, 1) - timedelta(days=1)


def get_csv(t: int):
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

    # Read data from "s.csv" and "h.csv"
    s_data = pd.read_csv("s.csv")
    h_data = pd.read_csv("h.csv")
    s_data.insert(loc=5, column="Asr Hanafi", value=h_data["Asar"])
    s_data = s_data.rename(columns={"Asar": "Asr Shafi"})
    x = s_data["Date"].str.split(" ", expand=True)[[0, 1]]
    s_data[["Date"]] = x[[1]]
    s_data.insert(loc=1, column="Day", value=x[[0]])
    s_data[["Isha"]] = h_data[["Isha"]]
    # Save the final data to "f.csv"
    return s_data


def gen_doc(df):
    from pylatex import Center, Command, Document, Figure, LineBreak, Tabular
    from pylatex.utils import NoEscape, bold

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
        image_filename = "./logo.png"
        with doc.create(Figure(position="th")) as logo:
            logo.add_image(image_filename, width="69px")
        doc.append(NoEscape(r"\vspace{-10pt}"))  # Inserting the vertical space
        doc.append(bold(f"{fd.strftime('%a %d %b %Y')} - {ld.strftime('%a %d %b %Y')}"))
        doc.append(LineBreak())

        doc.preamble.append(NoEscape(r"\setlength{\tabcolsep}{12pt}"))
        # Add a table to the document
        with doc.create(Tabular("|c|c|c|c|c|c|c|c|c|", row_height=1.4)) as table:
            table.add_hline()
            table.add_row(df.columns)
            table.add_hline()
            for _, row in df.iterrows():
                table.add_hline()
                c = None
                if row.iloc[1] == "Fri":
                    c = "lightgray"
                table.add_row(row, color=c)
            table.add_hline()

        doc.append(LineBreak())
        with doc.create(Tabular("|c|", row_height=1.4)) as t2:
            t2.add_hline()
            t2.add_row(
                [
                    bold(
                        "Jumuah prayer 13:00, UWE Centre for Sport, BS16 1ZL, open to Brothers and Sisters"
                    )
                ]
            )
            t2.add_hline()
            t2.add_row(
                [
                    "Seerah Class: The Sealed Nectar - Every Tuesday, 18:00 - Brothers in-person (3E39), Sisters online"
                ]
            )
            t2.add_hline()

        doc.append(LineBreak())
        doc.append(LineBreak())
        doc.append("Prayer times provided by https://www.salahtimes.com")
        doc.append(LineBreak())
        doc.append(bold("https://uwe.isoc.link/timetable"))

    # Save the document to a PDF file
    doc.generate_pdf("prayer_time")


get_csv(1)
get_csv(2)

data = get_formatted_data()

gen_doc(data)

data.to_csv("prayers.csv", index=False)
