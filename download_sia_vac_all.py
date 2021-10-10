import click
from pathlib import Path
import pandas as pd
from airac import airac_date
from download_sia_vac import download_sia_vac


def download_sia_vac_all():
    """Download all VAC from SIA."""
    dt_airac = airac_date()
    path = Path(__file__).parent / dt_airac.isoformat()
    df = pd.read_excel(path / "AD.xlsx")
    df = df.set_index("code")
    print(df)
    for code in df.index:
        download_sia_vac(code)


if __name__ == "__main__":
    download_sia_vac_all()
