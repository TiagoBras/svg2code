from code_generator import CodeGenerator, CodeGeneratorOptions
from svg_parser import * 
from svg_colors import SVG_COLORS
from helpers import promptYesOrNo
from string import Template
from os import path
import argparse
import glob
import sys

def main():
    pass

class Swift3CodeGenerator(CodeGenerator, object):
    def __init__(self, options=None):
        super(Swift3CodeGenerator, self).__init__()
        self.options = options or CodeGeneratorOptions()

    def genCode(self, svgs):
        generatedCode = self._genClassCode(svgs)

        if self.options.path is None:
            print(generatedCode)
        else:
            fullpath = path.abspath(self.options.path)
            filename = path.basename(fullpath)

            if path.exists(fullpath):
                if not promptYesOrNo("'%s' already exists, would you like to overwrite it? (Y/N)" % filename):
                    print("Code generation aborted")
                    return

            with open(fullpath, 'w') as f:
                f.write(generatedCode)

            print("'%s' created successfuly" % filename)

    def genCodeFromSVGFiles(self, filenames):
        if not isinstance(filenames, (list, tuple)):
            filenames = [filenames]

        svgs = [SVG.fromFile(x) for x in filenames]

        self.genCode(svgs)

    def genDrawCodeFromSVGString(self, string):
        svg = SVG.fromString(string)
        self.genCode([svg])

    def _genClassCode(self, svgs, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)

        s = indent + "import UIKit\n\n"
        s += indent + "class %s {\n" % self.options.className
        # Generate draw methods
        for svg in svgs:
            s += self._genImageMethod(svg, indentationLevel + 1)

        for svg in svgs:
            s += self._genDrawMethod(svg, indentationLevel + 1)

        s += "\n" + self._genClassHelperMethods(indentationLevel + 1)
        return s + indent + "}"

    def _genImageMethod(self, svg, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)
        indent1 = self._indentationForLevel(indentationLevel + 1)

        s = ""
        s += indent + "static func imageOf{}(withSize size: CGSize, opaque: Bool = false) -> UIImage {{\n".format(
            self._titledName(svg.name)
        )
        s += indent1 + "return image(withSize: size, opaque: opaque, drawingMethod: %s)\n" % self._genDrawMethodName(svg.name)
        s += indent + "}\n\n"

        return s

    def _genDrawMethod(self, svg, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)
        indent1 = self._indentationForLevel(indentationLevel + 1)

        frame = self._genFrameRect(svg.x, svg.y, svg.width, svg.height)
        s = indent + "static func {}(inRect target: CGRect = {}) {{\n".format(
            self._genDrawMethodName(svg.name), frame
        )

        s += indent1 + "let frame = %s\n\n" % frame
        s += indent1 + "let context = UIGraphicsGetCurrentContext()!\n"
        s += indent1 + "context.saveGState()\n"
        s += indent1 + "context.concatenate(%s.transformToFit(rect: frame, inRect: target))\n\n" % self.options.className

        didntDrawAnything = True
        pathIndex = 1
        lastPath = None
        for node in svg.iterator:
            if node.isDrawable and node.isVisible:
                name = node.id
                if len(name) == 0:
                    name = "path%d" % pathIndex
                    pathIndex += 1
    
                s += self._genPathCode(node, name, lastPath, indentationLevel + 1) + "\n"
                
                lastPath = node
                didntDrawAnything = False

        if didntDrawAnything:
            print("Warning: Didn't find anything to draw in '%s'" % svg.name)

            s += indent1 + "// There was nothing to draw here. ('%s')\n\n" % svg.name

        s += indent1 + "context.restoreGState()\n"
        s += indent + "}\n"

        return s

    def _genPathCode(self, currPath, name, lastPath=None, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)

        s = indent + "let %s = UIBezierPath()\n" % name

        for c in currPath.commands:
            s += indent + ("%s." % name)

            if isinstance(c, MoveTo):
                p = P(c.x, c.y).applyTransform(currPath.transform)
                s += "move(to: CGPoint(x: %f, y: %f))\n" % (p.x, p.y)
            elif isinstance(c, ClosePath):
                s += "close()\n"
            elif isinstance(c, LineTo):
                p = P(c.x, c.y).applyTransform(currPath.transform)
                s += "addLine(to: CGPoint(x: %f, y: %f))\n" % (p.x, p.y)
            elif isinstance(c, CurveTo):
                p = P(c.x, c.y).applyTransform(currPath.transform)
                c1 = P(c.x1, c.y1).applyTransform(currPath.transform)
                c2 = P(c.x2, c.y2).applyTransform(currPath.transform)
                s += ("addCurve(to: CGPoint(x: %f, y: %f), "
                    "controlPoint1: CGPoint(x: %f, y: %f), "
                    "controlPoint2: CGPoint(x: %f, y: %f))\n") % (p.x, p.y, c1.x, c1.y, c2.x, c2.y)
            else:
                raise NotImplementedError("Path command '%s' is not implemented" % type(c))

        if currPath.usesEvenOddFillRule:
            s += indent + "%s.usesEvenOddFillRule = true\n" % name

        strokeLineCap = currPath.strokeLineCap
        if strokeLineCap is not None and strokeLineCap != "butt":
            s += indent + "%s.lineCapStyle = .%s\n" % (name, strokeLineCap)

        strokeWidth = currPath.strokeWidth
        if strokeWidth is not None and strokeWidth != 1.0:
            s += indent + "%s.lineWidth = %f\n" % (name, strokeWidth) 

        fillColor = currPath.rgbaFillColor
        if fillColor is not None:
            if lastPath is None or (lastPath is not None and fillColor != lastPath.rgbaFillColor):
                s += indent + "%s.setFill()\n" % self._rgbaToUIColor(fillColor)
            s += indent + "%s.fill()\n" % name

        strokeColor = currPath.rgbaStrokeColor
        if strokeColor is not None:
            if lastPath is None or (lastPath is not None and strokeColor != lastPath.rgbaStrokeColor):
                s += indent + "%s.setStroke()\n" % self._rgbaToUIColor(strokeColor)
            s += indent + "%s.stroke()\n" % name

        return s

    def _genCGAffineTransform(self, t):
        return "CGAffineTransform(a: %f, b: %f, c: %f, d: %f, tx: %f, ty: %f)" % (t.a, t.b, t.c, t.d, t.e, t.f)

    def _getAppropriateCodeGeneratorForNode(self, node):
        nodeType = type(node)
        if nodeType not in self.GEN_MAP:
            raise NotImplementedError("Code generation for type '%s' not implemented" % nodeType)

        return self.GEN_MAP[nodeType]

    def _indentationForLevel(self, level):
        return self.options.indentation * level

    def _rgbaToUIColor(self, color):
        return "UIColor(red: {}, green: {}, blue: {}, alpha: {})".format(*color.components)

    def _titledName(self, name):
        return re.sub(r'[^\w]+$|[-_]+|^\d+', '', name.title())

    def _genFrameRect(self, x, y, width, height):
        components = [removeTrailingZeros(str(n)) for n in [x, y, width, height]]

        return "CGRect(x: {}, y: {}, width: {}, height: {})".format(*components)

    def _genDrawMethodName(self, name):
        return "draw" + self._titledName(name)

    def _genClassHelperMethods(self, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)
        indent1 = self._indentationForLevel(indentationLevel + 1)
        indent2 = self._indentationForLevel(indentationLevel + 1)

        s = ""
        s += indent + "static private func image(withSize size: CGSize, opaque: Bool, drawingMethod: (CGRect) -> Void) -> UIImage {\n"
        s += indent1 + "UIGraphicsBeginImageContextWithOptions(size, opaque, 0.0)\n\n"
        s += indent1 + "drawingMethod(CGRect(origin: .zero, size: size))\n\n"
        s += indent1 + "let image = UIGraphicsGetImageFromCurrentImageContext()!\n\n"
        s += indent1 + "UIGraphicsEndImageContext()\n\n"
        s += indent1 + "return image\n"
        s += indent + "}\n\n"
        s += indent + "static private func transformToFit(rect: CGRect, inRect target: CGRect) -> CGAffineTransform {\n"
        s += indent1 + "var scale = CGPoint(\n"
        s += indent2 + "x: abs(target.size.width / rect.size.width),\n"
        s += indent2 + "y: abs(target.size.height / rect.size.height)\n"
        s += indent1 + ")\n\n"
        s += indent1 + "let tallerThanWider = scale.y < scale.x\n\n"
        s += indent1 + "scale.x = min(scale.x, scale.y)\n"
        s += indent1 + "scale.y = scale.x\n\n"
        s += indent1 + "var translate = target.origin\n"
        s += indent1 + "if tallerThanWider {\n"
        s += indent2 + "translate.x += 0.5 * (target.size.width - (rect.size.width * scale.x))\n"
        s += indent1 + "} else {\n"
        s += indent2 + "translate.y += 0.5 * (target.size.height - (rect.size.height * scale.y))\n"
        s += indent1 + "}\n\n"
        s += indent1 + "let scaleT = CGAffineTransform(scaleX: scale.x, y: scale.y)\n"
        s += indent1 + "let translateT = CGAffineTransform(translationX: translate.x, y: translate.y)\n\n"
        s += indent1 + "return scaleT.concatenating(translateT)\n"
        s += indent + "}\n"

        return s

TRAILING_ZEROS_RE = re.compile(r'\.?0+$')
def removeTrailingZeros(s):
    result = TRAILING_ZEROS_RE.sub('', s) if '.' in s else s
    # return result if '.' in result else result + '.0'
    return result

if __name__ == '__main__':
    main()


        