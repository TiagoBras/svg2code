from code_generator import CodeGenerator
from svg_parser import * 
from svg_colors import SVG_COLORS
from string import Template

def main():
    swiftGen = Swift3CodeGenerator()
    swiftGen.genCodeFromSVGFile("/Users/tiagobras/Documents/ChaosTokens/SVGs/rectangles.svg")

class CodeGeneratorOptions(object):
    def __init__(self):
        super(CodeGeneratorOptions, self).__init__()
        self.useTabs = False
        self.spaces = 4

    @property
    def indentation(self):
        return "\t" if self.useTabs else " " * self.spaces

class Swift3CodeGenerator(CodeGenerator, object):
    def __init__(self,  options=None):
        super(Swift3CodeGenerator, self).__init__()
        self.options = options or CodeGeneratorOptions()
   
    def genCodeFromSVGFile(self, filename):
        svg = SVG.fromFile(filename)

        self.genCode(svg)

    def genDrawCodeFromSVGString(self, string):
        svg = SVG.fromString(string)
        self.genCode(svg)

    def genCode(self, svg):
        s = self._genClassCode([svg])

        print(s)

    def _genClassCode(self, svgs, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)

        s = indent + "class %s {\n" % "StyleKit"
        for svg in svgs:
            s += self._genDrawMethod(svg, indentationLevel + 1)

        s += "\n" + self._genClassHelperMethods(indentationLevel + 1)
        return s + indent + "}"

    def _genDrawMethod(self, svg, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)
        indent1 = self._indentationForLevel(indentationLevel + 1)

        frame = self._genFrameRect(svg.x, svg.y, svg.width, svg.height)
        s = indent + "static func draw{}(inRect target: CGRect = {}) {{\n".format(
            self._titledName(svg.name), frame
        )

        s += indent1 + "let frame = %s\n\n" % frame
        s += indent1 + "let context = UIGraphicsGetCurrentContext()!\n"
        s += indent1 + "context.saveGState()\n"
        s += indent1 + "context.concatenate(StyleKit.transformToFit(rect: frame, inRect: target))\n\n"

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

    def _genClassHelperMethods(self, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)
        indent1 = self._indentationForLevel(indentationLevel + 1)
        indent2 = self._indentationForLevel(indentationLevel + 1)

        s = ""
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


        