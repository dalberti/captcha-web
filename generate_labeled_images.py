import requests
from uuid import uuid4
from tqdm import tqdm
from pathlib import Path
import sys
import shutil


def save_labeled_images(images_path: Path, solutions_path: Path, labeled_images_path: Path):
    for solution_file in tqdm(solutions_path.iterdir()):
        with solution_file.open("r") as f:
            solution = f.read().strip().lower()
        image_file_path = images_path / solution_file.name.rsplit(".", 1)[0]
        solution_num = 0
        while (labeled_images_path / f"{solution}-{solution_num:03}.jpeg").exists():
            solution_num += 1
        shutil.copy(image_file_path, labeled_images_path / f"{solution}-{solution_num:03}.jpeg")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 generate_labeled_images.py <images_path> <solutions_path> <labeled_images_path>")
        sys.exit(1)

    IMAGES_PATH = Path(sys.argv[1])
    if not IMAGES_PATH.exists() or not IMAGES_PATH.is_dir():
        print(f"{sys.argv[1]} is not a valid directory")
        sys.exit(1)
    SOLUTIONS_PATH = Path(sys.argv[2])
    if not SOLUTIONS_PATH.exists() or not SOLUTIONS_PATH.is_dir():
        print(f"{sys.argv[2]} is not a valid directory")
        sys.exit(1)
    LABELED_IMAGES_PATH = Path(sys.argv[3])
    if not LABELED_IMAGES_PATH.exists() or not LABELED_IMAGES_PATH.is_dir():
        print(f"{sys.argv[3]} is not a valid directory")
        sys.exit(1)

    save_labeled_images(IMAGES_PATH, SOLUTIONS_PATH, LABELED_IMAGES_PATH)

    print("Done")
