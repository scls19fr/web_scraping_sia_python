import click
from pathlib import Path
import pandas as pd
from airac import airac_date
from download_sia_vac import download_sia_vac
from pdf2image import convert_from_path


def sia_vac_to_xcsoar():
    """Create LANDING.txt file with SIA VAC."""
    dt_airac = airac_date()
    vac_path = Path(__file__).parent / dt_airac.isoformat()
    df = pd.read_excel(vac_path / "AD.xlsx")
    df = df.set_index("code")
    print(df)

    wpt_details_path = vac_path / "wpt_details"
    wpt_details_path.mkdir(parents=True, exist_ok=True)

    with open(wpt_details_path / "WPT_DETAILS.txt", "w") as fd:
        for i, code in enumerate(df.index):
            print(f"proceed {code} {i+1}/%d" % len(df.index), end="")
            # ToDo : copy vac pdf file

            print(f"[{code}]", file=fd)
            # print("COUNTRY: France", file=fd)
            # print("", file=fd)
            # print("RUNWAYS:", file=fd)
            # print("", file=fd)
            # print("COMMUNICATIONS:", file=fd)
            # print("", file=fd)
            # print("REMARKS:", file=fd)
            # print("", file=fd)
            print(f"ICAO: {code}", file=fd)
            print("", file=fd)
            filename_vac = f"AD-2.{code}"
            print(f"image=wpt_details/{filename_vac}" + ".pdf", file=fd)
            images = convert_from_path(vac_path / (filename_vac + ".pdf"))
            (wpt_details_path / code).mkdir(parents=True, exist_ok=True)
            pages = len(images)
            print(f" with {pages} page(s)")
            for j, image in enumerate(images):
                picture_filename = f"AD-2.{code}-%02d.jpg" % (j + 1)
                page_path = wpt_details_path / code / picture_filename
                print(f"image=wpt_details/{code}/{picture_filename}", file=fd)
                image.save(page_path, "JPEG")
            print("", file=fd)
        
    # convert -density 150 presentation.pdf -quality 90 output-%3d.jpg


if __name__ == "__main__":
    sia_vac_to_xcsoar()
