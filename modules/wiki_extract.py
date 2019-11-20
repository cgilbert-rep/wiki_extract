from modules.download_functions import get_wikidump_url,\
    get_list_downloads_wikidump, get_file_from_url
from modules.preprocess_functions import split_articles
import os


def run(argv=None):
    # List of files to download
    # # Get the dump url
    dump_url = get_wikidump_url()
    # # Get the list of file of the dump, sorted by ascending size
    list_downloads_wikidump = sorted(
        get_list_downloads_wikidump(
            dump_url=dump_url),
        key=lambda x: x[1],
        reverse=False
    )
    # print(list_downloads_wikidump)
    # Download files
    temp_folder = 'temp_files/'
    for file in list_downloads_wikidump[:1]:
        get_file_from_url(
            url=file[0],
            target_folder=temp_folder
        )
    # Preprocess files
    list_preprocess_files = [
        os.path.join(temp_folder, file)
        for file in os.listdir(temp_folder) if file.endswith(".bz2")]
    for file in list_preprocess_files:
        split_articles(file, folder_output="output_files/")
