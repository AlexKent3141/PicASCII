from image_finder import *
import urllib2
import random

# Find images on the google website.
class GoogleFinder(ImageFinder):
    def find(self, search_terms):
        google_query = "https://www.google.co.in/search?q=*&source=lnms&tbm=isch"
        query = "+".join(search_terms)
        google_query = google_query.replace("*", query)

        # Setup a dummy user agent.
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36' }
        req = urllib2.Request(google_query, headers=headers)
        res = urllib2.urlopen(req)
        content = res.read()

        # Parse the content.
        paths = [s for s in content.split("\"") if s[:4] == 'http' and s[-4:] == ".jpg"]
        return random.choice(paths) if len(paths) > 0 else ""

if __name__ == "__main__":
    finder = GoogleFinder()
    f = finder.find(["mountain", "alps"])
    finder.download(f, "mount.jpg")
