import os


def build_folder(folder):
    '''
    Build a folder if it doesn't exist

    param folder: folder to build
    type output_folder: string

    return: None
    rtype: None
    '''
    if not(os.path.isdir(folder)) and (folder != ""):
        print("%s does not exist, making it..." % folder)
        os.mkdir(folder)
    return
