# file: server.py
# description: Web server that provides a file upload form
# author: Cristiano Nascimento, cristnascimento@gmail.com
# date: Jan 13th, 2013

import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options

from s3_client import upload_file_to_s3
from zencoder_client import convert_to_mp4
import time

define("port", default=8888, help="run on the given port", type=int)

# directory where files will be written
path_to_save = "/tmp/videos/"
default_filename = "sample"
s3_api_key = ''
s3_secret_key = ''
s3_bucket_name = 'cristnascimento-bucket'
s3_server = 'https://s3.amazonaws.com/'
zencoder_api_key = ''

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadHandler),
	    (r'/videos/(.*)', tornado.web.StaticFileHandler, {'path': path_to_save})
        ]
        tornado.web.Application.__init__(self, handlers)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_form.html")

class UploadHandler(tornado.web.RequestHandler):
    def save_file(self, request, path):
	"""
	Saves file uploaded by a HTML form in a server directory.
	"""
        file1 = request.files['file1'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        final_filename= default_filename + extension
        output_file = open(path + final_filename, 'w')
        output_file.write(file1['body'])
        return final_filename

    def post(self):
	"""
	Handles POST action from a HTML upload form.
	It saves file content to a local file in the server.
	Then, it sends the file to Amazon S3 storage service.
	Next, it calls Zencoder API to convert the file
        (that must be a video to) to MP4 format. The converted
        file is stored in Zencoder S3 server.
	This method returns an HTML page that includes a video
 	player linking to the MP4 file in Zencoder S3 Server.
	"""
	filename = self.save_file(self.request, path_to_save)
        upload_file_to_s3(path_to_save + filename,
                          filename,
                          s3_bucket_name,
                          s3_api_key,
                          s3_secret_key)
	s3_file_url = s3_server + s3_bucket_name + "/" + filename
        zencoder_url_converted = convert_to_mp4(zencoder_api_key, s3_file_url)

	self.render("player.html", entry=zencoder_url_converted)

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

