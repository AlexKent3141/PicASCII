from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math

class RegionIntensities:
    DIVISION_RATIO = 0.1

    def __init__(self, img, l, t, w, h):
        self.horiz_weight = 0.2
        self.vert_weight = 0.1
        self.centre_weight = 0.7

        # Calculate regional intensities for the image.
        sw = math.floor(w * self.DIVISION_RATIO)
        sh = math.floor(h * self.DIVISION_RATIO)
        self.li = self.region_intensity(img, l, t+sh, sw, w-2*sh)
        self.ri = self.region_intensity(img, l+w-sw, t+sh, sw, w-2*sh)
        self.ti = self.region_intensity(img, l, t, w, sh)
        self.bi = self.region_intensity(img, l, t+h-sh, w, sh)
        self.ci = self.region_intensity(img, l+sw, t+sh, w-2*sw, h-2*sh)

    # Compute the intensity value for a region
    def region_intensity(self, img, pixel_left, pixel_top, pixel_width, pixel_height):
        s = 0.0
        for r in range(int(pixel_width)):
            for c in range(int(pixel_height)):
                p = img.getpixel((r+pixel_left, c+pixel_top))
                s += self.intensity(p)

        d = pixel_width * pixel_height
        return s / d if d != 0 else s

    # Compute the perceived intensity of a pixel.
    def intensity(self, rgb):
        return 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]

    def Compare(self, other):
        # Compare the intensities and compute the error.
        return self.horiz_weight*(pow(self.li-other.li, 2) + pow(self.ri-other.ri, 2)) + \
               self.vert_weight*(pow(self.ti-other.ti, 2) + pow(self.bi-other.bi, 2)) + \
               self.centre_weight*pow(self.ci-other.ci, 2)

# This class describes the shape of the character in terms of intensity.
class CharacterIntensity:
    def __init__(self, c):
        self.c = c

        # Render the character.
        # Use a large font size for greater accuracy.
        font = ImageFont.truetype("UbuntuMono-B.ttf", 50)
        s = font.getsize(c)
        img = Image.new("RGB", s, (0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), c, (255, 255, 255), font=font)

        # Compute the regional intensities.
        w = s[0]
        h = s[1]
        self.region = RegionIntensities(img, 0, 0, w, h)

def image_to_ascii(image_path, max_char_width):

    # Compute the intensities for each character.
    char_intensities = []
    for i in range(32, 127):
        its = CharacterIntensity(chr(i))
        char_intensities.append(its)

    img = Image.open(image_path).convert('RGB')
    s = img.size
    char_width = min(max_char_width, s[0])
    char_height = int((s[1] * char_width / 2) / s[0])

    pixel_width = s[0] / float(char_width)
    pixel_height = s[1] / float(char_height)

    # Compute average intensity over each region.
    ris = []
    for r in range(char_height):
        for c in range(char_width):
            ri = RegionIntensities(img, c*pixel_width, r*pixel_height, pixel_width, pixel_height)
            ris.append(ri)

    # Find the most suitable character for each region.
    out = ""
    for r in range(char_height):
        for c in range(char_width):
            ri = ris[c+r*char_width]
            min_error = 1000000
            best = None
            for ci in char_intensities:
                err = ci.region.Compare(ri)
                if err < min_error:
                    min_error = err
                    best = ci.c

            out += best if best else ' '

        out += '\n'

    return out

if __name__ == "__main__":
    print image_to_ascii('TestImages/Dog.jpg', 100)
