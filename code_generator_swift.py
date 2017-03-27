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

    def genCodeFromSVGString(self, string):
        svg = SVG.fromString(string)
        self.genCode(svg)

    def genCode(self, svg):
        indentLevel = 1
        pathIndex = 1
        
        lastPath = None
        for node in svg.iterator:
            if node.isDrawable and node.isVisible:
                name = node.id
                if len(name) == 0:
                    name = "path%d" % pathIndex
                    pathIndex += 1
    
                s = self._genPathCode(node, name, lastPath)
                
                lastPath = node

                print(s)

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

if __name__ == '__main__':
    main()


        