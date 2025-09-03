from datetime import datetime, timedelta

from script import get_csv, get_formatted_data

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
    doc = Document(geometry_options=geometry_options, font_size="Large")
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
        with doc.create(Tabular("|c|c|c|c|c|c|c|", row_height=1.2)) as table:
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

    # Save the document to a PDF file
    doc.generate_pdf("ahmad")


get_csv(1)
get_csv(2)

data = get_formatted_data()
data = data.drop(columns=["Asr Hanafi", "Sunrise"])

gen_doc(data)

data.to_csv("prayers.csv", index=False)
