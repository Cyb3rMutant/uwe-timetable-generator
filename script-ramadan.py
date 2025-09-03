from datetime import datetime, timedelta

from pylatex.utils import bold

from script import get_csv, get_formatted_data

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


def gen_doc(df):
    from pylatex import Center, Command, Document, Figure, LineBreak, Tabular

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
