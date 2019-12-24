import numpy as np

NR_OF_GREY = 2 ** 8  # number of grayscale levels to use in CLAHE algorithm


def equalize_adapthist(image, kernel_size=None, clip_limit=0.01, nbins=256):
    image = __rescale_intensity(image)

    if kernel_size is None:
        kernel_size = (image.shape[0] // 8, image.shape[1] // 8)
    kernel_size = [int(k) for k in kernel_size]
    image = __clahe(image, kernel_size, clip_limit * nbins, nbins)
    return __rescale_intensity(image)


def __rescale_intensity(image):
    """"
    image = np.array([51, 102, 153], dtype=np.uint8)
    rescale_intensity(image)
    array([  0, 127, 255], dtype=uint8)
    """
    imin, imax = np.min(image), np.max(image)
    omin, omax = 0, 255

    if imin != imax:
        image = (image - imin) / float(imax - imin)
    return np.asarray(image * (omax - omin) + omin, dtype=np.uint8)


def __clahe(image, kernel_size, clip_limit, nbins=128):
    if clip_limit == 1.0:
        return image  # is OK, immediately returns original image.

    nr = int(np.ceil(image.shape[0] / kernel_size[0]))
    nc = int(np.ceil(image.shape[1] / kernel_size[1]))

    row_step = int(np.floor(image.shape[0] / nr))
    col_step = int(np.floor(image.shape[1] / nc))

    bin_size = 1 + NR_OF_GREY // nbins
    lut = np.arange(NR_OF_GREY)
    lut //= bin_size

    map_array = np.zeros((nr, nc, nbins), dtype=int)

    # Calculate greylevel mappings for each contextual region
    for r in range(nr):
        for c in range(nc):
            sub_img = image[r * row_step: (r + 1) * row_step,
                      c * col_step: (c + 1) * col_step]

            if clip_limit > 0.0:  # Calculate actual cliplimit
                clim = int(clip_limit * sub_img.size / nbins)
                if clim < 1:
                    clim = 1
            else:
                clim = NR_OF_GREY  # Large value, do not clip (AHE)

            hist = lut[sub_img.ravel()]
            hist = np.bincount(hist)
            hist = np.append(hist, np.zeros(nbins - hist.size, dtype=int))
            hist = __clip_histogram(hist, clim)
            hist = __map_histogram(hist, 0, NR_OF_GREY - 1, sub_img.size)
            map_array[r, c] = hist

    # Interpolate greylevel mappings to get CLAHE image
    rstart = 0
    for r in range(nr + 1):
        cstart = 0
        if r == 0:  # special case: top row
            r_offset = row_step / 2.0
            rU = 0
            rB = 0
        elif r == nr:  # special case: bottom row
            r_offset = row_step / 2.0
            rU = nr - 1
            rB = rU
        else:  # default values
            r_offset = row_step
            rU = r - 1
            rB = rB + 1

        for c in range(nc + 1):
            if c == 0:  # special case: left column
                c_offset = col_step / 2.0
                cL = 0
                cR = 0
            elif c == nc:  # special case: right column
                c_offset = col_step / 2.0
                cL = nc - 1
                cR = cL
            else:  # default values
                c_offset = col_step
                cL = c - 1
                cR = cL + 1

            mapLU = map_array[rU, cL]
            mapRU = map_array[rU, cR]
            mapLB = map_array[rB, cL]
            mapRB = map_array[rB, cR]

            cslice = np.arange(cstart, cstart + c_offset)
            rslice = np.arange(rstart, rstart + r_offset)

            __interpolate(image, cslice, rslice,
                          mapLU, mapRU, mapLB, mapRB, lut)

            cstart += c_offset  # set pointer on next matrix */

        rstart += r_offset

    return image


def __clip_histogram(hist, clip_limit):
    """Perform clipping of the histogram and redistribution of bins.
    The histogram is clipped and the number of excess pixels is counted.
    Afterwards the excess pixels are equally redistributed across the
    whole histogram (providing the bin count is smaller than the cliplimit).
    Parameters
    ----------
    hist : ndarray
        Histogram array.
    clip_limit : int
        Maximum allowed bin count.
    Returns
    -------
    hist : ndarray
        Clipped histogram.
    """
    # calculate total number of excess pixels
    excess_mask = hist > clip_limit
    excess = hist[excess_mask]
    n_excess = excess.sum() - excess.size * clip_limit

    # Second part: clip histogram and redistribute excess pixels in each bin
    bin_incr = int(n_excess / hist.size)  # average binincrement
    upper = clip_limit - bin_incr  # Bins larger than upper set to cliplimit

    hist[excess_mask] = clip_limit

    low_mask = hist < upper
    n_excess -= hist[low_mask].size * bin_incr
    hist[low_mask] += bin_incr

    mid_mask = (hist >= upper) & (hist < clip_limit)
    mid = hist[mid_mask]
    n_excess -= mid.size * clip_limit - mid.sum()
    hist[mid_mask] = clip_limit

    prev_n_excess = n_excess

    while n_excess > 0:  # Redistribute remaining excess
        index = 0
        while n_excess > 0 and index < hist.size:
            under_mask = hist < 0
            step_size = int(hist[hist < clip_limit].size / n_excess)
            step_size = max(step_size, 1)
            indices = np.arange(index, hist.size, step_size)
            under_mask[indices] = True
            under_mask = (under_mask) & (hist < clip_limit)
            hist[under_mask] += 1
            n_excess -= under_mask.sum()
            index += 1
        # bail if we have not distributed any excess
        if prev_n_excess == n_excess:
            break
        prev_n_excess = n_excess

    return hist


def __map_histogram(hist, min_val, max_val, n_pixels):
    """Calculate the equalized lookup table (mapping).
    It does so by cumulating the input histogram.
    Parameters
    ----------
    hist : ndarray
        Clipped histogram.
    min_val : int
        Minimum value for mapping.
    max_val : int
        Maximum value for mapping.
    n_pixels : int
        Number of pixels in the region.
    Returns
    -------
    out : ndarray
       Mapped intensity LUT.
    """
    out = np.cumsum(hist).astype(float)
    scale = ((float)(max_val - min_val)) / n_pixels
    out *= scale
    out += min_val
    out[out > max_val] = max_val
    return out.astype(int)


def __interpolate(image, xslice, yslice,
                  mapLU, mapRU, mapLB, mapRB, lut):
    """Find the new grayscale level for a region using bilinear interpolation.
    Parameters
    ----------
    image : ndarray
        Full image.
    xslice, yslice : array-like
       Indices of the region.
    map* : ndarray
        Mappings of greylevels from histograms.
    lut : ndarray
        Maps grayscale levels in image to histogram levels.
    Returns
    -------
    out : ndarray
        Original image with the subregion replaced.
    Notes
    -----
    This function calculates the new greylevel assignments of pixels within
    a submatrix of the image. This is done by a bilinear interpolation between
    four different mappings in order to eliminate boundary artifacts.
    """
    norm = xslice.size * yslice.size  # Normalization factor
    # interpolation weight matrices
    x_coef, y_coef = np.meshgrid(np.arange(xslice.size),
                                 np.arange(yslice.size))
    x_inv_coef, y_inv_coef = x_coef[:, ::-1] + 1, y_coef[::-1] + 1

    view = image[int(yslice[0]):int(yslice[-1] + 1),
           int(xslice[0]):int(xslice[-1] + 1)]
    im_slice = lut[view]
    new = ((y_inv_coef * (x_inv_coef * mapLU[im_slice]
                          + x_coef * mapRU[im_slice])
            + y_coef * (x_inv_coef * mapLB[im_slice]
                        + x_coef * mapRB[im_slice]))
           / norm)
    view[:, :] = new
    return image
