#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Stefan Hagmann

import os

import cv2

import numpy as np


class OpenCV():
    """
    for inspiration have a look at
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html
    """

    def read(self, img):
        """ Read an image, preserver all channels """
        return cv2.imread(img, cv2.IMREAD_UNCHANGED)

    def resizeTo(self, img, width, height):
        """ resize the Mat to this width and height in px """
        h, w = img.shape[:2]
        fac_w = width / w
        fac_h = height / h
        # print("%s x %s" % (fac_w * w, fac_h * h))
        return cv2.resize(img, (int(fac_w * w), int(fac_h * h)), interpolation=cv2.INTER_CUBIC)

    def getSize(self, imgpath):
        """ 
        get the size of an image
        :param imgpath: full path to the image
        """
        im = cv2.imread(imgpath)
        height, width = im.shape[:2]
        return [width, height]

    def transparentOverlay(self, src, overlay, x, y):
        """
        Place a overlay PNG Image onto background on position x, y
        :param src: Input Color Background Image
        :param overlay: transparent Image
        :param pos:  position where the image to be
        :return: Resultant Image
        """
        overlay = cv2.cvtColor(overlay, cv2.COLOR_RGB2BGRA)  # important
        src = cv2.cvtColor(src, cv2.COLOR_RGB2BGRA)
        # Convert overlay to it to 8-bit
        self.map_uint16_to_uint8(overlay)  # important

        # Size of foreground
        h, w, _ = overlay.shape
        # Size of background Image
        rows, cols, _ = src.shape
        # loop over all pixels and apply alpha
        for i in range(h):
            for j in range(w):
                if (x + i) >= rows or (y + j) >= cols:
                    continue
                # read the alpha channel
                alpha = float(overlay[i][j][3] / 255.0)
                try:
                    src[x + i][y + j] = alpha * overlay[i][j] + \
                        (1 - alpha) * src[x + i][y + j]
                except ValueError:
                    print("Pixeldata mismatch, e.g. RGB and RGBA")
        return src

    def createVignette(self, imgpath):
        """
        Create a vignette effect to an image 
        :param imgpath: full path to the image
        """
        input_image = cv2.imread(imgpath)
        rows, cols = input_image.shape[:2]
        # generating vignette mask using Gaussian
        # resultant_kernels
        X_resultant_kernel = cv2.getGaussianKernel(cols, 2000)
        Y_resultant_kernel = cv2.getGaussianKernel(rows, 2000)

        # generating resultant_kernel matrix
        resultant_kernel = Y_resultant_kernel * X_resultant_kernel.T

        # creating mask and normalising by using np.linalg
        # function
        mask = 255 * resultant_kernel / np.linalg.norm(resultant_kernel)
        output = np.copy(input_image)

        # applying the mask to each channel in the input image
        for i in range(3):
            output[:,:, i] = output[:,:, i] * mask

        newfile = os.path.join(os.path.dirname(imgpath), "mod_" + os.path.basename(imgpath))
        if not cv2.imwrite(newfile, output):
            raise Exception("Could not write image")
        
        return newfile

        # debug output
        """
        cv2.imshow('vignette', output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        """
