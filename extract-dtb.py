#!/usr/bin/env python3
"""
Copyright 2017 Pablo Castellano

extract-dtb is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

extract-dtb is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with extract-dtb.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import os
import string

__version__ = "1.3"

DTB_HEADER = b"\xd0\x0d\xfe\xed"


def dump_file(filename, content):
    with open(filename, "wb") as fp:
        fp.write(content)


def safe_output_path(output_dir, dtb_filename_new):
    """ Safely combines the output folder with the relative path of the dtb
        (which may contain subfolders) and creates the necessary folder
        structure.

        :returns: the resulting file name
    """
    if "../" in dtb_filename_new + "/":
        raise RuntimeException("DTB file path points outside of extraction"
                               " directory: " + dtb_filename_new)
    ret = os.path.join(args.output_dir, dtb_filename_new)
    os.makedirs(os.path.dirname(ret), exist_ok=True)
    return ret


def split(args):
    """ Reads a file and looks for DTB_HEADER occurrences (beginning of each DTB)
        Then extract each one. If possible, use the device model as filename.
    """
    positions = []

    with open(args.filename, "rb") as fp:
        content = fp.read()

    dtb_next = content.find(DTB_HEADER)
    while dtb_next != -1:
        positions.append(dtb_next)
        dtb_next = content.find(DTB_HEADER, dtb_next + 1)

    if len(positions) == 0:
        print("No appended dtbs found")
        return

    if args.extract:
        os.makedirs(args.output_dir, exist_ok=True)
        begin_pos = 0
        for n, pos in enumerate(positions, 0):
            dtb_filename = get_dtb_filename(n)
            filepath = os.path.join(args.output_dir, dtb_filename)
            dump_file(filepath, content[begin_pos:pos])
            if n > 0:
                dtb_name = get_dtb_model(filepath)
                if dtb_name:
                    dtb_filename_new = get_dtb_filename(n, dtb_name)
                    dtb_filename_new_full = safe_output_path(args.output_dir,
                                                             dtb_filename_new)
                    os.rename(filepath, dtb_filename_new_full)
                    dtb_filename = dtb_filename_new
            print("Dumped {0}, start={1} end={2}"
                  .format(dtb_filename, begin_pos, pos))
            begin_pos = pos

        # Last chunk
        dtb_filename = get_dtb_filename(n + 1)
        filepath = os.path.join(args.output_dir, dtb_filename)
        dump_file(filepath, content[begin_pos:])
        dtb_name = get_dtb_model(filepath)
        if dtb_name:
            dtb_filename_new = get_dtb_filename(n + 1, dtb_name)
            os.rename(os.path.join(filepath),
                      os.path.join(args.output_dir, dtb_filename_new))
            dtb_filename = dtb_filename_new
        print("Dumped {0}, start={1} end={2}"
              .format(dtb_filename, begin_pos, len(content)))
        print("Extracted {0} appended dtbs + kernel to {1}"
              .format(len(positions), args.output_dir))
    else:
        print("Found {0} appended dtbs".format(len(positions)))


def get_dtb_filename(n, suffix=""):
    if n == 0:
        return "00_kernel"
    n = str(n).zfill(2)
    basename = "{0}_dtbdump".format(n)
    if suffix != "":
        basename += "_" + suffix.replace(" ", "_")
    return basename + ".dtb"


def get_dtb_model(filename, min_length=4):
    """ Finds the first printable string in a file with length greater
        than min_length. Replaces spaces with underscores.
    """
    with open(filename, errors="ignore") as f:
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min_length:
                return result.replace(" ", "_")
            result = ""
        if len(result) >= min_length:  # catch result at EOF
            return result.replace(" ", "_")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract dtbs from kernel images.")
    parser.add_argument("filename", help="Android kernel image")
    parser.add_argument("-o", dest="output_dir", default="dtb",
                        required=False, help="Output directory")
    parser.add_argument("-n", dest="extract", action="store_false", default=True,
                        required=False, help="Do not extract, just output information")
    parser.add_argument("-V", "--version", action="version", version=__version__)

    args = parser.parse_args()

    split(args)
