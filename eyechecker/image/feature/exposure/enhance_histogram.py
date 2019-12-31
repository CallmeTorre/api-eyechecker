import numpy as np

NR_OF_GREY = 2 ** 8  # number of grayscale levels to use in CLAHE algorithm


def equalize_adapthist(img, kernel_size=None, clip_limit=0.01, nbins=256):
    img = __rescale_intensity(img)

    if kernel_size is None:
        kernel_size = (img.shape[0] // 8, img.shape[1] // 8)
    kernel_size = [int(k) for k in kernel_size]
    img = __clahe(img, kernel_size, clip_limit * nbins, nbins)
    return __rescale_intensity(img)


def __rescale_intensity(img):
    imin, imax = np.min(img), np.max(img)
    omin, omax = 0, 255

    if imin != imax:
        img = (img - imin) / float(imax - imin)
    return np.asarray(img * (omax - omin) + omin, dtype=np.uint8)


def __clahe(img, kernel_size, clip_limit, nbins=128):
    if clip_limit == 1.0:
        return img  # is OK, immediately returns original image.

    nr = int(np.ceil(img.shape[0] / kernel_size[0]))
    nc = int(np.ceil(img.shape[1] / kernel_size[1]))

    row_step = int(np.floor(img.shape[0] / nr))
    col_step = int(np.floor(img.shape[1] / nc))

    bin_size = 1 + NR_OF_GREY // nbins
    lut = np.arange(NR_OF_GREY)
    lut //= bin_size

    map_array = np.zeros((nr, nc, nbins), dtype=int)

    # Calculate greylevel mappings for each contextual region
    for r in range(nr):
        for c in range(nc):
            sub_img = img[r * row_step: (r + 1) * row_step,
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

            __interpolate(img, cslice, rslice,
                          mapLU, mapRU, mapLB, mapRB, lut)

            cstart += c_offset  # set pointer on next matrix */

        rstart += r_offset

    return img


def __clip_histogram(hist, clip_limit):
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
    out = np.cumsum(hist).astype(float)
    scale = ((float)(max_val - min_val)) / n_pixels
    out *= scale
    out += min_val
    out[out > max_val] = max_val
    return out.astype(int)


def __interpolate(img, xslice, yslice,
                  mapLU, mapRU, mapLB, mapRB, lut):
    norm = xslice.size * yslice.size  # Normalization factor
    # interpolation weight matrices
    x_coef, y_coef = np.meshgrid(np.arange(xslice.size),
                                 np.arange(yslice.size))
    x_inv_coef, y_inv_coef = x_coef[:, ::-1] + 1, y_coef[::-1] + 1

    view = img[int(yslice[0]):int(yslice[-1] + 1),
           int(xslice[0]):int(xslice[-1] + 1)]
    im_slice = lut[view]
    new = ((y_inv_coef * (x_inv_coef * mapLU[im_slice]
                          + x_coef * mapRU[im_slice])
            + y_coef * (x_inv_coef * mapLB[im_slice]
                        + x_coef * mapRB[im_slice]))
           / norm)
    view[:, :] = new
    return img
