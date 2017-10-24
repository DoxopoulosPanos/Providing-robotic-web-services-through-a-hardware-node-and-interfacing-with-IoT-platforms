#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function

import sys
import base64

if sys.version_info < (3, 0):
    from StringIO import StringIO as InMemoryBuffer
else:
    from io import BytesIO as InMemoryBuffer


class Image(object):
    """Image container class. Uses in-memory-buffer, thus it is an
    imlementation compatible with the PIL module.
    """

    def __init__(self, fpath=None, charbuffer=None, base64=False):
        """Default constructor.

        @type fpath str
        @param fpath: Path to image file.
        @param charbuffer: String buffer with image data. Useless if fpath
            is provided.
        @param base64: True if charbuffer contains a base64 encoded string,
            False otherwise. Default value is False.
        """
        self.__memoryBuffer = None

        if fpath is not None:
            self.load_from_file(fpath)
        elif charbuffer is not None:
            self.load_from_charbuffer(charbuffer)

    @property
    def memoryBuffer(self):
        """Returns a reference of the in-memory buffer. Can be used to
        create PIL Images.

        @returns: StringIO instance. Can be used with PIL Image module.
        """
        return self.__memoryBuffer

    def load_from_file(self, fpath):
        """Load image in memory buffer from file.

        @type fpath str
        @param fpath: Path to the image file to load.
        """
        with open(fpath, 'rb') as fstream:
            self.__memoryBuffer = InMemoryBuffer(fstream.read())

    def load_from_charbuffer(self, charbuffer):
        self.__memoryBuffer = InMemoryBuffer(charbuffer)

    def load_from_base64(self, charbuffer):
        """Load image from base64 encoded string.

        @type charbuffer str
        @param charbuffer: The base64 encoded string.
        """
        self.__memoryBuffer = InMemoryBuffer(base64.b64decode(charbuffer))

    def write_to_file(self, fpath):
        """Write image data from in-memory buffer to file.

        @param fpath: The file path.

        @returns: None
        """
        with open(fpath, "wb") as fstream:
            fstream.write(self.__memoryBuffer.getvalue())

    def save(self, fpath):
        """Save data from in-memory buffer to a file.
        Alias to the write_to_file() member method.

        @param fpath: The file path
        """
        self.write_to_file(fpath)

    def stringify(self):
        """Returns a string representation of the data from the
        in-memory buffer.

        @returns str: String representation of image data
        """
        if self.__memoryBuffer is not None:
            return self.__memoryBuffer.getvalue()
        else:
            return None

    def stringify_base64(self):
        """Returns a string representation, encoded to base64,
        of the data from the in-memory buffer.

        @returns str: Base64 encoded string representation of image data.
        """
        if self.__memoryBuffer is not None:
            return base64.b64encode(self.__memoryBuffer.getvalue())
        else:
            return None

    def clear(self):
        """Clear and close the in-memory buffer"""
        if self.__memoryBuffer is not None and self.__memoryBuffer.closed is False:
            self.__memoryBuffer.close()

    def __str__(self):
        """Work / Compatible with print() function"""
        return self.stringify()

    def __len__(self):
        """Act like Set. Works with len build-in function."""
        return len(self.__memoryBuffer.getvalue())


if __name__ == "__main__":
    path = sys.argv[1]

    # Only for testing. This is not a script to be executed!!
    img = Image(fpath=path)
    print("Image Length in bytes: ", len(img))

    img.save("lenna2.jpe")

    imgStr = img.stringify()
    imgBase64 = img.stringify_base64()
    #img = Image_.Image("/home/panos/Desktop/Thesis/test/barcode/barcode10.png")
    #file = open('testfile.txt','w') 
    #file.write(imgBase64)
    #file.close()
    img.clear()

    img.load_from_base64(imgBase64)
    print("Image Length in bytes: ", len(img))
    img.save("lenna_base64.jpe")

    img.clear()

    img.load_from_charbuffer(imgStr)
    print("Image Length in bytes: ", len(img))

    img.clear()
