"""
data_preparation_M2.py

MATH1604 Modelling for Big Data
Team Member 2 – Download & Collation Module

This module provides tools for preparing the raw Python quiz response data.
It contains two main functions required by the group project specification:

1. download_answer_files(cloud_url, path_to_data_folder, total_respondents)
   Downloads raw respondent files named a1.txt, a2.txt, ..., aN.txt from a
   cloud location and saves them locally using the required naming convention:
   answers_respondent_1.txt, answers_respondent_2.txt, ..., answers_respondent_N.txt.

2. collate_answer_files(data_folder_path)
   Collates the downloaded respondent files into one file called
   collated_answers.txt inside an output folder. Each respondent section is
   separated by a line containing a single asterisk (*).

The code is designed to be robust, readable, and suitable for use as a Python
module within the full project pipeline.
"""

from __future__ import annotations

import socket
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def download_answer_files(
    cloud_url: str,
    path_to_data_folder: str,
    total_respondents: int
) -> list[int]:
    """
    Download respondent answer files from a cloud location.

    This function attempts to download files named a1.txt, a2.txt, ..., aN.txt
    from the given base URL, where N is equal to total_respondents. Each file
    successfully downloaded is saved in the local data folder using the required
    project naming convention:

        answers_respondent_1.txt
        answers_respondent_2.txt
        ...
        answers_respondent_N.txt

    The function is intentionally robust when files are missing. For example,
    if total_respondents is 70 but only files a1.txt to a64.txt exist, the
    function downloads the available files and skips the missing ones without
    stopping the whole program.

    Parameters
    ----------
    cloud_url : str
        The base URL of the cloud dataset. The URL should contain files named
        a1.txt, a2.txt, ..., aN.txt.

        Example:
        "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"

    path_to_data_folder : str
        The local folder where the downloaded files should be saved. The folder
        is created automatically if it does not already exist.

        Example:
        "data"

    total_respondents : int
        The number of respondent files to attempt to download. The function
        tries to retrieve files from a1.txt up to aN.txt.

    Returns
    -------
    list[int]
        A list of respondent numbers that were downloaded successfully.

        Example:
        [1, 2, 3, ..., 64]

    Raises
    ------
    TypeError
        If cloud_url or path_to_data_folder is not a string.

    ValueError
        If cloud_url is empty, path_to_data_folder is empty, or
        total_respondents is not a positive integer.

    Notes
    -----
    Missing files are not treated as fatal errors. They are reported to the
    user and skipped so that the function can continue downloading later files.
    This behaviour is useful for robustness testing.
    """
    if not isinstance(cloud_url, str):
        raise TypeError("cloud_url must be a string.")

    if not isinstance(path_to_data_folder, str):
        raise TypeError("path_to_data_folder must be a string.")

    if cloud_url.strip() == "":
        raise ValueError("cloud_url must not be empty.")

    if path_to_data_folder.strip() == "":
        raise ValueError("path_to_data_folder must not be empty.")

    if not isinstance(total_respondents, int) or total_respondents <= 0:
        raise ValueError("total_respondents must be a positive integer.")

    base_url = cloud_url.rstrip("/")
    data_folder = Path(path_to_data_folder)
    data_folder.mkdir(parents=True, exist_ok=True)

    downloaded_files: list[int] = []
    failed_files: list[int] = []

    for respondent_id in range(1, total_respondents + 1):
        source_url = f"{base_url}/a{respondent_id}.txt"
        destination_file = data_folder / f"answers_respondent_{respondent_id}.txt"

        try:
            with urlopen(source_url, timeout=10) as response:
                file_content = response.read().decode("utf-8")

            destination_file.write_text(file_content, encoding="utf-8")
            downloaded_files.append(respondent_id)

            print(
                f"Downloaded a{respondent_id}.txt "
                f"as {destination_file.name}"
            )

        except HTTPError as error:
            failed_files.append(respondent_id)

            if error.code == 404:
                print(
                    f"File a{respondent_id}.txt was not found "
                    f"at the cloud location. Skipping."
                )
            else:
                print(
                    f"HTTP error {error.code} while downloading "
                    f"a{respondent_id}.txt. Skipping."
                )

        except URLError as error:
            failed_files.append(respondent_id)
            print(
                f"Network error while downloading a{respondent_id}.txt: "
                f"{error}. Skipping."
            )

        except socket.timeout:
            failed_files.append(respondent_id)
            print(
                f"Download timed out for a{respondent_id}.txt. Skipping."
            )

        except UnicodeDecodeError:
            failed_files.append(respondent_id)
            print(
                f"Could not decode a{respondent_id}.txt as UTF-8. Skipping."
            )

        except OSError as error:
            failed_files.append(respondent_id)
            print(
                f"File system error while saving respondent "
                f"{respondent_id}: {error}. Skipping."
            )

    print("\nDownload summary")
    print("----------------")
    print(f"Files requested: {total_respondents}")
    print(f"Files downloaded successfully: {len(downloaded_files)}")
    print(f"Files skipped or failed: {len(failed_files)}")

    if failed_files:
        print(f"Skipped respondent IDs: {failed_files}")

    return downloaded_files


def collate_answer_files(data_folder_path: str) -> str:
    """
    Collate downloaded respondent answer files into one output file.

    This function searches the given data folder for files named according to
    the required convention:

        answers_respondent_1.txt
        answers_respondent_2.txt
        answers_respondent_3.txt
        ...

    The files are sorted by respondent number, not alphabetically. This avoids
    the common ordering problem where answers_respondent_10.txt could otherwise
    appear before answers_respondent_2.txt.

    The contents of all respondent files are written into a single file named
    collated_answers.txt inside an output folder located next to the data folder.
    Each respondent section is separated by a line containing one asterisk (*).

    Parameters
    ----------
    data_folder_path : str
        Path to the folder containing the downloaded respondent answer files.

        Example:
        "data"

    Returns
    -------
    str
        The path to the created collated_answers.txt file.

        Example:
        "output/collated_answers.txt"

    Raises
    ------
    TypeError
        If data_folder_path is not a string.

    ValueError
        If data_folder_path is an empty string.

    FileNotFoundError
        If the data folder does not exist or if no respondent answer files are
        found inside it.

    NotADirectoryError
        If data_folder_path exists but is not a folder.

    UnicodeDecodeError
        If one of the respondent files cannot be decoded as UTF-8.

    Notes
    -----
    The output folder is created automatically if it does not already exist.
    Existing collated_answers.txt files are overwritten so that the output
    always reflects the current contents of the data folder.
    """
    if not isinstance(data_folder_path, str):
        raise TypeError("data_folder_path must be a string.")

    if data_folder_path.strip() == "":
        raise ValueError("data_folder_path must not be empty.")

    data_folder = Path(data_folder_path)

    if not data_folder.exists():
        raise FileNotFoundError(f"Data folder does not exist: {data_folder}")

    if not data_folder.is_dir():
        raise NotADirectoryError(f"Path is not a folder: {data_folder}")

    respondent_files: list[tuple[int, Path]] = []

    for file_path in data_folder.glob("answers_respondent_*.txt"):
        try:
            respondent_number = int(file_path.stem.split("_")[-1])
            respondent_files.append((respondent_number, file_path))
        except ValueError:
            print(
                f"Ignoring file with unexpected name format: {file_path.name}"
            )

    if not respondent_files:
        raise FileNotFoundError(
            f"No files named answers_respondent_*.txt were found in {data_folder}"
        )

    respondent_files.sort(key=lambda item: item[0])

    output_folder = data_folder.parent / "output"
    output_folder.mkdir(parents=True, exist_ok=True)

    collated_file = output_folder / "collated_answers.txt"

    collated_sections: list[str] = []

    for _, file_path in respondent_files:
        try:
            text = file_path.read_text(encoding="utf-8").rstrip()
            collated_sections.append(text)
        except UnicodeDecodeError as error:
            raise UnicodeDecodeError(
                error.encoding,
                error.object,
                error.start,
                error.end,
                f"Could not decode {file_path} as UTF-8."
            ) from error

    collated_text = "\n*\n".join(collated_sections) + "\n"
    collated_file.write_text(collated_text, encoding="utf-8")

    print("\nCollation summary")
    print("-----------------")
    print(f"Number of files collated: {len(respondent_files)}")
    print(f"First respondent file: answers_respondent_{respondent_files[0][0]}.txt")
    print(f"Last respondent file: answers_respondent_{respondent_files[-1][0]}.txt")
    print(f"Collated file created at: {collated_file}")

    return str(collated_file)


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    BASE_URL = (
        "https://raw.githubusercontent.com/"
        "fc-leeds/MATH1604_2025_2026_data/main"
    )

    data_path = PROJECT_ROOT / "data"

    downloaded_ids = download_answer_files(
        cloud_url=BASE_URL,
        path_to_data_folder=str(data_path),
        total_respondents=70
    )

    print(f"\nSuccessfully downloaded respondent IDs: {downloaded_ids}")

    output_path = collate_answer_files(str(data_path))
    print(f"\nFinal collated file path: {output_path}")
