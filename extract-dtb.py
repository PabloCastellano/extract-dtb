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

__version__ = "1.1"

DTB_HEADER = b"\xd0\x0d\xfe\xed"


def dump_file(filename, content):
    with open(filename, "wb") as fp:
        fp.write(content)


def split(args):
    pos_dtb = []
    content = None

    with open(args.filename, "rb") as fp:
        content = fp.read()

    dtb_next = content.find(DTB_HEADER)
    while dtb_next != -1:
        pos_dtb.append(dtb_next)
        dtb_next = content.find(DTB_HEADER, dtb_next + 1)

    if len(pos_dtb) == 0:
        print("No appended dtbs found")
        return

    if args.extract:
        os.makedirs(args.output_dir, exist_ok=True)
        last_pos = 0
        for n, pos in enumerate(pos_dtb, 0):
            dtb_filename = "dtbdump_{0:0>2}.dtb".format(n) if n != 0 else "kernel"
            dump_file(os.path.join(args.output_dir, dtb_filename), content[last_pos:pos])
            if n != 0:
                dtb_filename_new = "dtbdump_{0:0>2}_{1}.dtb".format(
                    n,
                    next(strings(os.path.join(args.output_dir, dtb_filename))).replace(" ", "_"))
                os.rename(os.path.join(args.output_dir, dtb_filename),
                          os.path.join(args.output_dir, dtb_filename_new))
                dtb_filename = dtb_filename_new
            print("Dumped {0}, start={1} end={2}".format(dtb_filename, last_pos, pos))
            last_pos = pos

        # Last chunk
        dtb_filename = "dtbdump_{0:0>2}.dtb".format(n + 1)
        dump_file(os.path.join(args.output_dir, dtb_filename), content[last_pos:])
        dtb_filename_new = "dtbdump_{0:0>2}_{1}.dtb".format(
            n + 1,
            next(strings(os.path.join(args.output_dir, dtb_filename))).replace(" ", "_"))
        os.rename(os.path.join(args.output_dir, dtb_filename),
                  os.path.join(args.output_dir, dtb_filename_new))
        print("Dumped {0}, start={1} end={2}".format(dtb_filename_new, last_pos, len(content)))
        print("Extracted {0} appended dtbs + kernel to {1}"
              .format(len(pos_dtb), args.output_dir))
    else:
        print("Found {0} appended dtbs".format(len(pos_dtb)))


def strings(filename, min=4):
    # with open(filename, "rb") as f:           # Python 2.x
    with open(filename, errors="ignore") as f:  # Python 3.x
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:  # catch result at EOF
            yield result


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
