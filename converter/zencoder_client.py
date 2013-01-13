# file: server.py
# description: Web server that provides a file upload form
# author: Cristiano Nascimento, cristnascimento@gmail.com
# date: Jan 13th, 2013

import urllib2
import json

zencoder_url = "https://app.zencoder.com/api/v2/jobs"

def convert_to_mp4(api_key, s3_file_url):
    """
    Converts a video file stored in Amazon S3 to a mp4 file that will be stored in Zencoder Amazon S3.
    Returns a URL of the converted file stored in Zencoder Amazon S3 place.
    api_key: Zencoder api key
    s3_file_url: a string like this
          'https://s3.amazonaws.com/cristnascimento-bucket/sample.avi'
    """
    zencoder_data = { "api_key": api_key, "input": s3_file_url}
    jdata = json.dumps(zencoder_data)
    response = urllib2.urlopen(zencoder_url, jdata)
    response_obj = json.loads(response.read())
    response_url = response_obj["outputs"][0]["url"]

    return response_url
