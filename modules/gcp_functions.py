from google.cloud import storage


def get_list_files_in_bucket(bucket_name, prefix=''):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    return [
        el.name.replace(prefix + '/', '')
        for el in bucket.list_blobs(prefix=prefix)]
    return list(bucket.list_blobs(prefix=prefix))


def file_to_bucket(file_name, bucket_name, prefix=''):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(prefix + file_name)
    blob.upload_from_filename(file_name)
    return file_name


def get_blob_dump(file_name, bucket_name, prefix=''):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(prefix + '/' + file_name)
    # convert to file
    blob.download_to_filename(file_name)
    return file_name


if __name__ == '__main__':
    print(get_list_files_in_bucket('wikipr2', 'wikidump'))
