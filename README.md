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
usage: extract-dtb.py [-h] [-o OUTPUT_DIR] [-n] [-V] filename

Extract dtbs from kernel images.

positional arguments:
  filename       Android kernel image

optional arguments:
  -h, --help     show this help message and exit
  -o OUTPUT_DIR  Output directory
  -n             Do not extract, just output information
  -V, --version  show program's version number and exit
```

Example:

```
$ ./extract-dtb.py -n /tmp/postmarketOS-export/vmlinuz-motorola-titan
Found 9 appended dtbs

$ ./extract-dtb.py /tmp/postmarketOS-export/vmlinuz-motorola-titan -o /tmp/dtb
Dumped kernel, start=0 end=7534024
Dumped dtbdump_1.dtb, start=7534024 end=7728853
Dumped dtbdump_2.dtb, start=7728853 end=7923682
Dumped dtbdump_3.dtb, start=7923682 end=8118511
Dumped dtbdump_4.dtb, start=8118511 end=8313340
Dumped dtbdump_5.dtb, start=8313340 end=8508169
Dumped dtbdump_6.dtb, start=8508169 end=8700762
Dumped dtbdump_7.dtb, start=8700762 end=8894086
Dumped dtbdump_8.dtb, start=8894086 end=9087470
Dumped dtbdump_9.dtb, start=9087470 end=9280854
Extracted 9 appended dtbs + kernel to /tmp/dtb

$ ls -l /tmp/dtb/
total 9088
-rw-rw-r-- 1 pablo pablo  194829 Aug 11 09:34 dtbdump_1.dtb
-rw-rw-r-- 1 pablo pablo  194829 Aug 11 09:34 dtbdump_2.dtb
-rw-rw-r-- 1 pablo pablo  194829 Aug 11 09:34 dtbdump_3.dtb
-rw-rw-r-- 1 pablo pablo  194829 Aug 11 09:34 dtbdump_4.dtb
-rw-rw-r-- 1 pablo pablo  194829 Aug 11 09:34 dtbdump_5.dtb
-rw-rw-r-- 1 pablo pablo  192593 Aug 11 09:34 dtbdump_6.dtb
-rw-rw-r-- 1 pablo pablo  193324 Aug 11 09:34 dtbdump_7.dtb
-rw-rw-r-- 1 pablo pablo  193384 Aug 11 09:34 dtbdump_8.dtb
-rw-rw-r-- 1 pablo pablo  193384 Aug 11 09:34 dtbdump_9.dtb
-rw-rw-r-- 1 pablo pablo 7534024 Aug 11 09:34 kernel
```

Also works with `boot.img`.
