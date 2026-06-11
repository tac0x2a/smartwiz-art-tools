#!/usr/bin/env python3
import sys
import subprocess
import shutil
from pathlib import Path
import sys
import os
import epd_util

def main():
    fit_mode = "letterbox"
    args = sys.argv[1:]
    
    if "--crop" in args:
        fit_mode = "crop"
        args.remove("--crop")

    if len(args) < 2:
        print("Usage: python3 convert_image.py [--crop] <input_image.jpg> <output_image.s6>")
        sys.exit(1)

    input_image = Path(args[0])
    output_image = Path(args[1])
    if not input_image.exists():
        print("File not found.")
        sys.exit(1)

    if not shutil.which("convert") and not shutil.which("magick"):
        print("ImageMagick (`magick` or `convert`) not found. Please install it.")
        sys.exit(1)

    try:
        epd_util.convert_image_to_s6(input_image, output_image, fit_mode=fit_mode)
    except Exception as e:
        print(f"convert image failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
