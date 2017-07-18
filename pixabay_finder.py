from image_finder import *
import urllib2
import random

# Find images on the pixabay website.
class PixabayFinder(ImageFinder):
    # The "pixabay.com" website is used as the source of images. At the time of writing these are
    # completely free to use and distribute.
    def find(self, search_terms):
        pixabay_query = "https://pixabay.com/en/photos/?hp=&image_type=&cat=&min_width=&min_height=&q=*&order=popular"
        query = "+".join(search_terms)
        pixabay_query = pixabay_query.replace("*", query)
        res = urllib2.urlopen(pixabay_query)
        content = res.read()
        paths = [s for s in content.split("\"") if s[-3:] == "jpg"]
        return random.choice(paths) if len(paths) > 0 else ""

if __name__ == "__main__":
    finder = PixabayFinder()
    f = finder.find(["mountain", "alps"])
    finder.download(f, "mount.jpg")
