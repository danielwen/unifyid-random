# Generate random bitmap image using Random.org for UnifyID coding challenge
# Daniel Wen (github.com/danielwen)

import requests
import numpy as np
from PIL import Image

# Image properties
ROWS = 128
COLS = 128
CHANNELS = 3

# Number of bits we need to request (pixel intensity is 0-256 which is 8 bits)
BITS_REQUIRED = ROWS * COLS * CHANNELS * 8
# Maximum number of integers we can request at once
MAX_NUM = 10000


# Check quota to make sure we don't get banned
def check_quota():
    r = requests.get("https://www.random.org/quota/?format=plain")
    if r.status_code == 200:
        quota = int(r.text.strip())
        if quota >= BITS_REQUIRED:
            return True
        else:
            print("Insufficient quota")
            return False

    print("Quota check failed")
    return False


# Make a request for n integers from Random.org
def request_ints(n):
    params = {
        "num" : n,
        "min" : 0,
        "max" : 255,
        "col" : 1,
        "base" : 10,
        "format" : "plain",
        "rnd" : "new"
    }

    r = requests.get("https://www.random.org/integers/", params=params)

    if r.status_code == 200:
        return [int(line) for line in r.text.strip().splitlines()]

    print("Request error")


# Get random integers from Random.org
def get_ints():
    result = []

    # Number of integers we need
    num_needed = ROWS * COLS * CHANNELS

    # Keep requesting up to MAX_NUM integers until we get enough
    while num_needed > 0:
        current_num = min(num_needed, MAX_NUM)
        ints = request_ints(current_num)

        if ints is None:
            return

        result.extend(ints)
        num_needed -= current_num

    return result


# Create image and save it
def make_image(ints):
    array = np.array(ints).reshape((ROWS * COLS, CHANNELS))
    image = Image.new("RGB", (ROWS, COLS))
    image.putdata([tuple(pixel) for pixel in array])
    image.save("image.bmp")


def main():
    # Check quota
    if not check_quota():
        return

    # Get random integers
    ints = get_ints()

    # Make and save image
    make_image(ints)


main()


# Tests

def test_make_image():
    test_ints = [128]*(128*128*3)
    make_image(test_ints)

def test_get_ints_request_ints(n):
    return [128]*n
