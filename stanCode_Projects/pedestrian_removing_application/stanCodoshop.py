"""
File: stanCodoshop.py
Name: Harry Kuo
----------------------------------------------
SC101_Assignment3 Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.
"""

import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns a value that refers to the "color distance" between a pixel and a mean RGB value.

    Input:
        pixel (Pixel): the pixel with RGB values to be compared
        red (int): the average red value of the pixels to be compared
        green (int): the average green value of the pixels to be compared
        blue (int): the average blue value of the pixels to be compared

    Returns:
        dist (float): the "color distance" of a pixel to the average RGB value of the pixels to be compared.
    """
    img_rgb = [pixel.red, pixel.green, pixel.blue]
    avg_point_rgb = [red, green, blue]
    color_distance_squared = 0
    for i in range(len(img_rgb)):
        ans = (img_rgb[i] - avg_point_rgb[i]) ** 2      # to compare the RGB value with the average
        color_distance_squared += ans
    color_distance = color_distance_squared ** 0.5
    return color_distance


def get_average(pixels):
    """
    Given a list of pixels, finds their average red, blue, and green values.

    Input:
        pixels (List[Pixel]): a list of pixels to be averaged

    Returns:
        rgb (List[int]): a list of average red, green, and blue values of the pixels
                        (returns in order: [red, green, blue])
    """
    rgb = []
    pixel_r, pixel_g, pixel_b = 0, 0, 0
    for pixel in pixels:
        pixel_r += pixel.red
        pixel_g += pixel.green
        pixel_b += pixel.blue
    rgb.append(pixel_r // len(pixels))
    rgb.append(pixel_g // len(pixels))
    rgb.append(pixel_b // len(pixels))
    return rgb


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest "color distance", which has the closest color to the average.

    Input:
        pixels (List[Pixel]): a list of pixels to be compared
    Returns:
        best (Pixel): the pixel which has the closest color to the average
    """
    avg_rgb = get_average(pixels)
    min_d = float('Inf')
    min_pixel = 0
    for pixel in pixels:
        color_distance = get_pixel_dist(pixel, avg_rgb[0], avg_rgb[1], avg_rgb[2])
        if color_distance < min_d:              # to determine the pixel which has the closest color to the average
            min_d = color_distance
            min_pixel = pixel
    return min_pixel


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    
    # ----- YOUR CODE STARTS HERE ----- #

    for y in range(height):
        for x in range(width):                                  # loop over the pixels at (x, y)
            pixels = []
            result_p = result.get_pixel(x, y)                   # get the pixel from (x, y) in blank image
            for i in range(len(images)):
                pixels += [images[i].get_pixel(x, y)]           # to store the pixels at (x, y) in each image
            result_p.red = get_best_pixel(pixels).red           # assign the best pixel's RGB value to the result
            result_p.green = get_best_pixel(pixels).green
            result_p.blue = get_best_pixel(pixels).blue

    # ----- YOUR CODE ENDS HERE ----- #

    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
