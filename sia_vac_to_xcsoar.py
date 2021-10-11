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
        for code in df.index:
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
            images = convert_from_path(vac_path / (filename_vac + ".pdf"))
            for i, image in enumerate(images):
                image.save(wpt_details_path / f"page{i}.jpg", "JPEG")

            print(f"image={filename_vac}", file=fd)
            print("", file=fd)
        
    # convert -density 150 presentation.pdf -quality 90 output-%3d.jpg


if __name__ == "__main__":
    sia_vac_to_xcsoar()
