# MIT License
#
# Copyright (c) 2020 Jacques Parker  copyright@judyandjacques.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
from typing import List


import exif


class PicMeta:
    """ Simple Metadata reader """

    @staticmethod
    def contains_substring(string: str, substrings: List[str]):
        """
        return true if any of the items in substrings are in the string.
        An empty string returns false as it cannot contain anything
        An empty substrings list returns.  The substrings list cannot contain empty strings
        """

        if string == '':
            return False

        assert isinstance(substrings, list)
        if len(substrings) == 0:
            return True

        for substring in substrings:
            assert substring != "", "substring[] must not contain empty strings"

        for substring in substrings:
            if substring in string:
                return True
        return False

    def __init__(self, exif_parser):
        self.exif_parser = exif_parser

    def get_metadata(self, files: list, labels: list) -> dict:
        for label in labels:
            assert len(label.strip()) > 0, "labels cannot be empty"

        assert len(files) > 0, "must have one or more files to parse"

        results = {}
        for file in files:
            image = self.exif_parser(file)
            metadata = {}
            found_labels = [key for key in dir(image) if PicMeta.contains_substring(key, labels)]
            for label in found_labels:
                metadata[label] = image[label]
            results[file.name] = metadata
        return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Return metadata for photos.')
    parser.add_argument('-l', '--label', action="append", dest='labels',
                        help='only show meta data if the name contains a defined label')
    parser.add_argument('files', nargs='+', type=argparse.FileType('rb'), help='files to process')
    args = parser.parse_args()

    pm = PicMeta(exif.Image)

    print(pm.get_metadata(args.files, args.labels))
