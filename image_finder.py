import urllib2

# Base class for image finders.
class ImageFinder(object):
    # This method must be implemented in the derived class.
    def find(self, search_terms):
        raise NotImplementedError("ImageFinder::find not implemented!")

    # Download the file at the specified URL and save it.
    def download(self, url, file_name):
        download = urllib2.urlopen(url)
        with open(file_name, 'wb') as target:
            target.write(download.read())

if __name__ == "__main__":
    f = find_image(["mountain", "alps"])
    download_image(f, "mount.jpg")
