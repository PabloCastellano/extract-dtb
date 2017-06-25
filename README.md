# extract-dtb

Tool to split a kernel image with appended dtbs into separated kernel and dtb files.

A Device Tree is a data structure for describing hardware. They are used in a lot of
ARM devices (e.g. Android), otherwise these would not be able to boot.

This tool is similar to [split-appended-dtb](https://github.com/dianlujitao/split-appended-dtb)
but it is written in Python and its code is simpler and almost 3x shorter.

If you want to learn more about DTB you can have a look at the
[Device Tree Reference](http://elinux.org/Device_Tree_Reference).

## Usage

```
$ ./extract-dtb.py --help
usage: extract-dtb.py [-h] [-n] filename

Extract dtbs from kernel images.

positional arguments:
  filename    Android kernel image

optional arguments:
  -h, --help     show this help message and exit
  -o OUTPUT_DIR  Output directory
  -n             Do not extract, just output information
```

Example:

```
$ ./extract-dtb.py -n vmlinuz-motorola-titan
Found 8 appended dtbs

$ ./extract-dtb.py vmlinuz-motorola-titan -o /tmp/dtb
Extracted 8 appended dtbs + kernel

$ ls -l /tmp/dtb
total 8808
-rw-rw-r-- 1 pablo pablo  194829 jun 25 17:14 dtbdump_1.dtb
-rw-rw-r-- 1 pablo pablo  194829 jun 25 17:14 dtbdump_2.dtb
-rw-rw-r-- 1 pablo pablo  194829 jun 25 17:14 dtbdump_3.dtb
-rw-rw-r-- 1 pablo pablo  194829 jun 25 17:14 dtbdump_4.dtb
-rw-rw-r-- 1 pablo pablo  194829 jun 25 17:14 dtbdump_5.dtb
-rw-rw-r-- 1 pablo pablo  192593 jun 25 17:14 dtbdump_6.dtb
-rw-rw-r-- 1 pablo pablo  193324 jun 25 17:14 dtbdump_7.dtb
-rw-rw-r-- 1 pablo pablo  193384 jun 25 17:14 dtbdump_8.dtb
-rw-rw-r-- 1 pablo pablo 7368984 jun 25 17:14 kernel
-rw-r--r-- 1 pablo pablo 9115814 jun 22 23:54 vmlinuz-motorola-titan
```
