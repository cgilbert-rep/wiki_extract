from modules.download_functions import get_wikidump_url,\
    get_list_downloads_wikidump


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
    print(list_downloads_wikidump)
    # Download files
    # Preprocess files
    return True
