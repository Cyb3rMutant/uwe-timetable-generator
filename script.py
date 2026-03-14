from datetime import datetime, timedelta

import utils

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
ld = datetime(next_next_year, next_month + 1, 1) - timedelta(days=1)
print(fd, ld)


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
        with doc.create(Figure(position="th")) as logo:
            logo.add_image("./logo.png", width="69px")
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
        t = utils.add_classes(
            Tabular("|c|", row_height=1.4),
            [
                utils.ClassRow(
                    "Jumuah prayer 13:00, UWE Centre for Sport, BS16 1ZL, open to Brothers and Sisters",
                    True,
                ),
                # utils.ClassRow(
                #     "Quran circles - Mondays - Brothers 18:00 in Br. prayer room - Sisters 18:15 in Sis. prayer room"
                # ),
                # utils.ClassRow(
                #     "Seerah class - Tuesdays at 18:00 - Ustadh Amin - Brothers in 3E39, sisters online"
                # ),
                # utils.ClassRow(
                #     "Roots - Wednesdays at 17:30 - Ustadh Abu Malik - Brothers and Sisters in 2X112"
                # ),
            ],
        )

        doc.append(t)
        doc.append(LineBreak())
        doc.append(LineBreak())
        doc.append(bold("https://uwe.isoc.link/timetable"))

    # Save the document to a PDF file
    doc.generate_pdf("prayer_time", clean_tex=True)


utils.get_csv(1, fd, ld)
utils.get_csv(2, fd, ld)

data = utils.get_formatted_data()

gen_doc(data)

data.to_csv("prayers.csv", index=False)
