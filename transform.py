"""
Python Image Manipulation Empty Template by Kylie Ying (modified from MIT 6.865)

YouTube Kylie Ying: https://www.youtube.com/ycubed 
Twitch KylieYing: https://www.twitch.tv/kylieying 
Twitter @kylieyying: https://twitter.com/kylieyying 
Instagram @kylieyying: https://www.instagram.com/kylieyying/ 
Website: https://www.kylieying.com
Github: https://www.github.com/kying18 
Programmer Beast Mode Spotify playlist: https://open.spotify.com/playlist/4Akns5EUb3gzmlXIdsJkPs?si=qGc4ubKRRYmPHAJAIrCxVQ 
"""

from image import Image


def brighten(image, factor):
    # when we brighten, we just want to make each channel higher by some amount 
    # factor is a value > 0, how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    x_pixels, y_pixels, num_channels = image.array.shape  # get x, y pixels of image, # channels
    # make an empty image so we don't actually modify the original one
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                   num_channels=num_channels)  # mutating new image to not override original

    #  non_vectorized method
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             new_im.array[x, y, c] = image.array[x, y, c] * factor

    # vectorized method
    new_im.array = image.array * factor
    return new_im


def adjust_contrast(image, factor, mid=0.5):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x , y pixels of image, # channels is R G B
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # makes a new array to copy values to
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image.array[x, y, c] - mid) * factor + mid

    return new_im


def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    # kernel size should always be an *odd* number
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    neighbor_range = kernel_size // 2  # how many neighbors to one side we need to look at

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                # we are going to use a naive implementation of iterating through each neighbor
                # and summing 
                # there is a faster way but this is more straightforward to understand
                total = 0
                for x_i in range(max(0, x - neighbor_range), min(x_pixels - 1, x + neighbor_range) + 1):
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels - 1, y + neighbor_range) + 1):
                        total += image.array[x_i, y_i, c]
                new_im.array[x, y, c] = total / (kernel_size ** 2)  # average

    return new_im


def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simiplicity of this implementation, let's assume that the kernel is SQUARE
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    kernel_size = kernel.shape[0]
    neighbor_range = kernel_size // 2
    # how many neighbors to one side we need to look at

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0, x - neighbor_range), min(x_pixels - 1, x + neighbor_range) + 1):
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels - 1, y + neighbor_range) + 1):
                        # we need to find which value of the kernel this corresonds to
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_im.array[x, y, c] = total

    return new_im


def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    x_pixels, y_pixels, num_channels = image1.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image1.array[x, y, c] ** 2 + image2.array[x, y, c] ** 2) ** 0.5

    return new_im


if __name__ == '__main__':
    # test
    # maybe become seperated test cases in the future

    # lake = Image(filename='lake.png')
    # city = Image(filename='city.png')
    mario = Image(filename='mario.png')

    # test brighten feature
    # brightened_im = brighten(lake, 1.7)
    # brightened_im.write_image('brightened.png')
    #
    # darkened_im = brighten(lake, 0.1)
    # darkened_im.write_image('darkened.jpg')
    #

    # test contrast
    # incr_contrast = adjust_contrast(mario, 2, 0.5)
    # incr_contrast.write_image('increased_contrast.png')
    #
    # decr_contrast = adjust_contrast(mario, 0.5, 0.5)
    # decr_contrast.write_image('decreased_contrast.png')

    # test blur
    blured_im = blur(mario, 3)
    blured_im.write_image('blur_k3.png')

    # blured_im = blur(mario, 15)
    # blured_im.write_image('blur_k15.png')

    # apply a sobel edge detection kernel on the x-axis and y-axis
    # sobel_x_kernel = np.array([
    #     [1, 2, 1],
    #     [0, 0, 0],
    #     [-1, -2, -1]
    # ])
    #
    # sobel_y_kernel = np.array([
    #     [1, 0, -1],
    #     [2, 0, -2],
    #     [1, 0, -1]
    # ])
    #
    # sobel_x = apply_kernel(city, sobel_x_kernel)
    # sobel_x.write_image('edge_x.png')
    # sobel_y = apply_kernel(city, sobel_y_kernel)
    # sobel_y.write_image('edge_y.png')
    #
    # sobel_xy = combine_images(sobel_x, sobel_y)
    # sobel_xy.write_image('edge_xy.png')
