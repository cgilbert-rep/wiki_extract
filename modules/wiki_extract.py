from modules.download_functions import get_wikidump_url,\
    get_list_downloads_wikidump, get_file_from_url
from modules.preprocess_functions import split_articles
from multiprocessing import Pool
from functools import partial
import os
import time


def run(argv=None):
    # # List of files to download
    # # # Get the dump url
    # dump_url = get_wikidump_url()
    # # # Get the list of file of the dump, sorted by ascending size
    # list_downloads_wikidump = sorted(
    #     get_list_downloads_wikidump(
    #         dump_url=dump_url),
    #     key=lambda x: x[1],
    #     reverse=False
    # )
    # # Download files
    # print("Downloading dump")
    # start_time = time.time()
    temp_folder = 'temp_files/'
    # for file in list_downloads_wikidump:
    #     get_file_from_url(
    #         url=file[0],
    #         target_folder=temp_folder
    #     )
    # print("Dump downloaded in %s s" % (time.time() - start_time))
    # Preprocess files
    print("Preprocessing files")
    start_time = time.time()
    list_preprocess_files = [
        os.path.join(temp_folder, file)
        for file in os.listdir(temp_folder) if file.endswith(".bz2")]
    output_folder = "output_files"
    list_already_done = [
        file
        for file in os.listdir(output_folder) if file.endswith(".ndjson")]
    list_preprocess_files = [file for file in list_preprocess_files
        if file.split('/')[1].replace('.bz2','.ndjson').replace('.xml','-xml') not in list_already_done]
    print(list_already_done)
    print(list_preprocess_files)
    # split_articles_partial = partial(
    #     split_articles,
    #     folder_output=output_folder)
    # pool = Pool(processes=16)
    # pool.map(split_articles_partial, list_preprocess_files)
    # print("Files preprocessed in %s s" % (time.time() - start_time))
