# file: s3_client.py
# description: Connects to Amazon S3 server using a client credential and
#              copies a local file to the server.
# author: Cristiano Nascimento, cristnascimento@gmail.com
# date: Jan 13th, 2013

from boto.s3.connection import S3Connection
from boto.s3.key import Key

def upload_file_to_s3(file_to_save,
                      file_saved,
                      bucket_name,
                      api_key,
                      secret_key):
    """
    file_to_save: full filename path in local host
    file_saved: filename to be saved in S3 server
    bucket_name: Amazon S3 bucket name
    api_key: Amazon user api key
    secret_key: Amazon user secret key
    """
    conn = S3Connection(api_key, secret_key)
    bucket = conn.get_bucket(bucket_name)
    k = Key(bucket)
    k.key = file_saved
    k.set_contents_from_filename(file_to_save)
    # Makes the file available public. Something like this:
    # https://s3.amazonaws.com/cristnascimento-bucket/sample.mp4
    k.make_public()
