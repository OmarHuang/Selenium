#!/usr/bin/env python3
"""This script for auto purchase."""
import argparse
import pchome

parser = argparse.ArgumentParser(description="Select a website.")
parser.add_argument("-p", "--pchome", action="store_true", help="Try to purchase on PChome")
args = parser.parse_args()


def main(args):
    """To run the script."""
    if args.pchome:
        pc = pchome.PChome()
        pc.login()
    else:
        print("Please select at least a website")


if __name__ == "__main__":
    main(args)
