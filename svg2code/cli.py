from __future__ import absolute_import, division, print_function

import os
import argparse
import glob
import sys
from stat import S_ISFIFO
from os import path
from code_generator import CodeGeneratorOptions
from code_generator_swift import Swift3CodeGenerator

def main():
    parser = argparse.ArgumentParser(description="SVG2Code - Code Generator")
    parser.add_argument('-o', '--output', help='Output file name', default="SVGDrawablesKit.swift")
    parser.add_argument('-c', '--class-name', help='Class name', default="SVGDrawablesKit")
    parser.add_argument('-s', '--spaces', type=int, help='Numbers of spacer per indentation', default=4)
    parser.add_argument('--tabs', help="Use tabs instead of spaces", action="store_true", default=False)
    parser.add_argument('-n', '--normalize', help="Normalize coordinates [0.0, 1.0]", action="store_true", default=False)
    parser.add_argument('--stdout', help="Instead of saving the output in a file it sends it to stdout", action="store_true", default=False)
    parser.add_argument('files', nargs='*', default='.')

    args = parser.parse_args()

    filesToParse = set()

    textToParse = None

    # Read from stdin if it's been piped to
    if S_ISFIFO(os.fstat(0).st_mode):
        textToParse = sys.stdin.read()
    else:
        for f in args.files:
            abspath = path.abspath(path.expanduser(f))

            if path.isdir(abspath):
                filesToParse.update(set(glob.glob(path.join(abspath, '*.svg'))))
            elif abspath.endswith('.svg'):
                filesToParse.add(abspath)

        if len(filesToParse) == 0:
            print("No SVG files found")
            exit(0)

    outputPath = path.abspath(args.output)

    if path.isdir(outputPath):
        path.join(outputPath, )

    extension = path.splitext(outputPath)[1]

    if extension not in ['.swift']:
        print("There is no code generator for '%s' files yet." % extension)
        exit(1)

    options = CodeGeneratorOptions(
        path=outputPath,
        className=args.class_name,
        useTabs=args.tabs,
        spaces=args.spaces,
        sendToSdout=args.stdout,
        normalizeCoords=args.normalize
    )
    swiftGen = Swift3CodeGenerator(options)

    if textToParse is not None:
        swiftGen.genDrawCodeFromSVGString(textToParse)
    else:
        swiftGen.genCodeFromSVGFiles(list(filesToParse))

if __name__ == '__main__':
    main()