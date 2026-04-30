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
next_next_month = (today.month + 1) % 12
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

    doc.preamble.append(NoEscape(r"\usepackage{graphicx}"))
    # doc.preamble.append(NoEscape(r"\usepackage[hidelinks]{hyperref}"))
    doc.preamble.append(NoEscape(r"\usepackage{hyperref}"))

    doc.append(NoEscape(r"""
    \noindent
    \begin{minipage}[t]{0.33\textwidth}
        \raggedright
        \href{https://uwe.isoc.link/timetable-left-link}{
            \includegraphics[width=100px]{left-with-text.png}
        }
    \end{minipage}
    \begin{minipage}[t]{0.33\textwidth}
        \centering
        \includegraphics[width=100px]{logo.png}
    \end{minipage}
    \begin{minipage}[t]{0.33\textwidth}
        \raggedleft
        \href{https://uwe.isoc.link/timetable-right-link}{
            \includegraphics[width=100px]{right-with-text.png}
        }
    \end{minipage}

    \vspace{1cm}
    """))

    with doc.create(Center()):
        doc.append(NoEscape(r"\vspace{-40pt}"))
        doc.append(bold(f"{fd.strftime('%a %d %b %Y')} - {ld.strftime('%a %d %b %Y')}"))
        doc.append(LineBreak())

        doc.preamble.append(NoEscape(r"\setlength{\tabcolsep}{12pt}"))
        # Add a table to the document
        with doc.create(Tabular("|c|c|c|c|c|c|c|c|c|", row_height=1.35)) as table:
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
                utils.ClassRow(
                    "Quran circles - Mondays 18:00 - Ustadh Abu Malik - Brothers only in prayer room"
                ),
                utils.ClassRow(
                    "Seerah class - Tuesdays 18:00 - Ustadh Amin - Brothers in 3E39, sisters online"
                ),
                utils.ClassRow(
                    "Al-Aqsa series - Wednesdays 17:30 - Ustadh Abu Malik - Brothers and Sisters in 2X112"
                ),
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
