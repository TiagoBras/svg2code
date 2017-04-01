# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from jinja2 import Environment, PackageLoader
from svg2code.svg_parser import SVG, MoveTo, LineTo, CurveTo, ClosePath
from os import path
from svg2code.helpers import promptYesOrNo
from datetime import datetime
import re

env = Environment(
    loader=PackageLoader('svg2code', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True
)

# Custom tests definition
def isMoveTo(o):
    return isinstance(o, MoveTo)

def isLineTo(o):
    return isinstance(o, LineTo)

def isCurveTo(o):
    return isinstance(o, CurveTo)

def isClosePath(o):
    return isinstance(o, ClosePath)

env.tests['MoveTo'] = isMoveTo
env.tests['LineTo'] = isLineTo
env.tests['CurveTo'] = isCurveTo
env.tests['ClosePath'] = isClosePath

# Custom filters definition
def stripZeros(n):
    s = str(n)
    if '.' not in s:
        return s.lstrip()

    s = s.strip('0')

    startsWithDot = s.startswith('.')
    endsWithDot = s.endswith('.')

    if startsWithDot and endsWithDot:
        return '0'
    
    if startsWithDot:
        s = '0' + s

    if endsWithDot:
        s = s + '0'

    return s

def removeWhitespace(s):
    return re.sub(r'\s+', '', s)

def firstLower(s):
    return s if len(s) == 0 else s[0].lower() + s[1:]

def lpad(s, length, ch=' '):
    return s.rjust(length, ch)

env.filters["stripzeros"] = stripZeros
env.filters["firstlower"] = firstLower
env.filters["removewhitespace"] = removeWhitespace
env.filters["lpad"] = lpad

def main():
    options = CodeGeneratorOptions()
    gen = CodeGenerator(options)
    gen.genCodeFromSVGFiles(['/Users/tiagobras/Desktop/rect.svg'], '/Users/tiagobras/Desktop/Rect.swift')

def reindentFrom4SpacesTo(text, spaces, useTabs=False):
    regex = re.compile(r'^(?P<tab>(    )+|(\t+))', re.MULTILINE)
    s = spaces * " " if not useTabs else '\t'

    def cb(m):
        ws = m.group('tab')
        return s * len(ws) if ws[0] == "\t" else s * (len(ws) // 4)

    return regex.sub(cb, text)

class CodeGenerator(object):
    def __init__(self, options):
        super(CodeGenerator, self).__init__()
        self.options = options or CodeGeneratorOptions()
        
    def genCode(self, svgs, outputPath):
        fullpath = path.abspath(outputPath)
        filename, extension = path.splitext(path.basename(fullpath))
        extension = extension[1:]

        template = env.get_template(extension + '.tpl')

        if template is None:
            raise NotImplementedError("Code generator for '%s' is not yet implemented" % extension)

        generatedCode = template.render(
            project=self.options.project,
            author=self.options.author,
            class_name=self.options.className, 
            date=datetime.now(),
            svgs=svgs).encode('utf-8')

        generatedCode = reindentFrom4SpacesTo(generatedCode, self.options.spaces, self.options.useTabs)

        if outputPath is None or self.options.sendToSdout:
            print(generatedCode)
        else:
            if path.exists(fullpath):
                if not promptYesOrNo("'%s' already exists, would you like to overwrite it? (Y/N)" % (filename + '.' + extension)):
                    print("Code generation aborted")
                    return

            with open(fullpath, 'w') as f:
                f.write(generatedCode)

            print("'%s' created successfuly" % (filename + '.' + extension))

    def genCodeFromSVGFiles(self, paths, outputPath):
        if not isinstance(paths, (list, tuple)):
            paths = [paths]

        svgs = [SVG.fromFile(x) for x in paths]

        self.genCode(svgs, outputPath)

    def genDrawCodeFromSVGString(self, string):
        svg = SVG.fromString(string, "Path")
        self.genCode([svg], outputPath)

class CodeGeneratorOptions(object):
    def __init__(self, **kwargs):
        super(CodeGeneratorOptions, self).__init__()
        self.project = kwargs.get("project", "Project")
        self.author = kwargs.get("author", "Author")
        self.className = kwargs.get("className", "SVGDrawablesKit")
        self.useTabs = kwargs.get("useTabs", False)
        self.spaces = int(kwargs.get("spaces", 4))
        self.sendToSdout = kwargs.get("sendToSdout", False)
        self.normalizeCoords = kwargs.get("normalizeCoords", False)

    @property
    def indentation(self):
        return "\t" if self.useTabs else " " * self.spaces

if __name__ == '__main__':
    main()