import urllib2
import random

# Find the URL for an image which matches the specified search terms.
# The "pixabay.com" website is used as the source of images. At the time of writing these are
# completely free to use and distribute.
def find_image(search_terms):
    pixabay_query = "https://pixabay.com/en/photos/?hp=&image_type=&cat=&min_width=&min_height=&q=*&order=popular"
    query = "+".join(search_terms)
    pixabay_query = pixabay_query.replace("*", query)
    res = urllib2.urlopen(pixabay_query)
    content = res.read()
    paths = [s for s in content.split("\"") if s[-3:] == "jpg"]
    return random.choice(paths) if len(paths) > 0 else ""

# Download and save the specified file locally.
def download_image(url, file_name):
    download = urllib2.urlopen(url)
    with open(file_name, 'wb') as target:
        target.write(download.read())

if __name__ == "__main__":
    f = find_image(["mountain", "alps"])
    download_image(f, "mount.jpg")
