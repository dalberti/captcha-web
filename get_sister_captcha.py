import requests
from uuid import uuid4
from tqdm import tqdm
from pathlib import Path
import sys

URL = "https://geoportale.cartografia.agenziaentrate.gov.it/age-inspire/srv/ita/Captcha"


def get_captcha(n: int, dir_path: Path):
    for _ in tqdm(range(n)):
        response = requests.get(URL, params={'type': 'image'})
        myme_type = response.headers['Content-Type'].partition(';')[0]
        if response.ok and myme_type.partition('/')[0] == 'image':
            ext = myme_type.split('/')[1]
            curr_file = dir_path / f"{uuid4()}.{ext}"
            _ = curr_file.write_bytes(response.content)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 get_captcha.py <dir_path> <n>")
        sys.exit(1)

    DIR_PATH = Path(sys.argv[1])
    if not DIR_PATH.exists() or not DIR_PATH.is_dir():
        print(f"{sys.argv[1]} is not a valid directory")
        sys.exit(1)
    try:
        n = int(sys.argv[2])
    except ValueError:
        print("n must be an integer")
        sys.exit(1)

    get_captcha(n, DIR_PATH)
    print("Done")
