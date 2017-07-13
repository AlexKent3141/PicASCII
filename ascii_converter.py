from PIL import Image

# Convert the specified image to ascii using the ascii map.
# The ascii map is a list of characters ordered by intensity.
def image_to_ascii(image_path, max_char_width, ascii_map):
    img = Image.open(image_path).convert('RGB')
    s = img.size
    char_width = min(max_char_width, s[0])
    char_height = int((s[1] * char_width / 2) / s[0])

    pixel_width = s[0] / float(char_width)
    pixel_height = s[1] / float(char_height)

    # Compute average intensity over each region.
    intensities = []
    for r in range(char_height):
        for c in range(char_width):
            intensities.append(region_intensity(img, c, r, pixel_width, pixel_height))

    # Normalise the intensities so that they conveniently index into the ascii_map.
    min_intensity = min(intensities)
    max_intensity = max(intensities)
    intensity_range = max_intensity - min_intensity

    normed = [len(ascii_map)*(i-min_intensity) / intensity_range for i in intensities]

    out = ""
    for r in range(char_height):
        for c in range(char_width):
            idx = r*char_width + c
            i = normed[idx]
            out += ascii_map[int(i)] if i < len(ascii_map) else ascii_map[-1]
        out += '\n'

    return out

# Compute the intensity value for a region
def region_intensity(img, region_left, region_top, pixel_width, pixel_height):
    s = 0.0
    rstart = region_left*pixel_width
    cstart = region_top*pixel_height
    for r in range(int(pixel_width)):
        for c in range(int(pixel_height)):
            p = img.getpixel((r+rstart, c+cstart))
            s += intensity(p)

    return s / (pixel_width*pixel_height)

# Compute the intensity of a pixel.
def intensity(rgb):
    return sum(rgb)

if __name__ == "__main__":
    print image_to_ascii('TestImages/Dog.jpg', 100, " .,:;ox%#@")
