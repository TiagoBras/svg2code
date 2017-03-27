from code_generator import CodeGenerator
from svg_parser import * 
from svg_colors import SVG_COLORS
from string import Template

def main():
    swiftGen = Swift3CodeGenerator()
    swiftGen.genCodeFromSVGFile("/Users/tiagobras/Documents/ChaosTokens/SVGs/shapes2.svg")

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
    
        for node in svg.iterator:
            if node.isDrawable:
                name = node.id
                if len(name) == 0:
                    name = "path%d" % pathIndex
                    pathIndex += 1
                    
                s = self._genPathCode(node, name)
                
                print(s)

    def _genPathCode(self, path, name, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)

        s = indent + "let %s = UIBezierPath()\n" % name

        for c in path.commands:
            s += indent + ("%s." % name)

            if isinstance(c, MoveTo):
                p = P(c.x, c.y).applyTransform(path.transform)
                s += "move(to: CGPoint(x: %f, y: %f))\n" % (p.x, p.y)
            elif isinstance(c, ClosePath):
                s += "close()\n"
            elif isinstance(c, LineTo):
                p = P(c.x, c.y).applyTransform(path.transform)
                s += "addLine(to: CGPoint(x: %f, y: %f))\n" % (p.x, p.y)
            elif isinstance(c, CurveTo):
                p = P(c.x, c.y).applyTransform(path.transform)
                c1 = P(c.x1, c.y1).applyTransform(path.transform)
                c2 = P(c.x2, c.y2).applyTransform(path.transform)
                s += ("addCurve(to: CGPoint(x: %f, y: %f), "
                    "controlPoint1: CGPoint(x: %f, y: %f), "
                    "controlPoint2: CGPoint(x: %f, y: %f))\n") % (p.x, p.y, c1.x, c1.y, c2.x, c2.y)
            else:
                raise NotImplementedError("Path command '%s' is not implemented" % type(c))
        
        s += self._genNodeStyleCode(path, name, indentationLevel) 
        if self._hasStroke(path):
            s += indent + "%s.stroke()\n" % name
        # if self._hasFill(path):
        s += indent + "%s.fill()\n" % name

        return s


    def _genNodeStyleCode(self, node, name, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)

        s = ""

        if "stroke_width" in node.style:
            s += indent + "%s.lineWidth = %f\n" % (name, float(node.style["stroke_width"][:-2]))
        if self._hasStroke(node):
            s += indent + "{}.setStroke()\n".format(self._parseRGB(node.style["stroke"]))
        if self._hasFill(node):
            s += indent + "{}.setFill()\n".format(self._parseRGB(
                node.style["fill"], float(node.style.get("fill_opacity", 1.0))
                ))
        else:
            s += indent + "{}.setFill()\n".format(self._parseRGB(
                "black", float(node.style.get("fill_opacity", 1.0))
                ))
        return s

    def _hasStroke(self, node):
        return "stroke" in node.style

    def _hasFill(self, node):
        return "fill" in node.style

    def _genCGAffineTransform(self, t):
        return "CGAffineTransform(a: %f, b: %f, c: %f, d: %f, tx: %f, ty: %f)" % (t.a, t.b, t.c, t.d, t.e, t.f)

    def _getAppropriateCodeGeneratorForNode(self, node):
        nodeType = type(node)
        if nodeType not in self.GEN_MAP:
            raise NotImplementedError("Code generation for type '%s' not implemented" % nodeType)

        return self.GEN_MAP[nodeType]

    def _indentationForLevel(self, level):
        return self.options.indentation * level

    def _parseRGB(self, color, opacity=1.0):
        color = SVG_COLORS.get(color, color)

        if color == "none":
            return "UIColor.clear"

        if not color.startswith("rgb("):
            raise NotImplementedError("%s color format is not implemented" % color)

        components = [int(x) / 255.0 for x in color[4:-1].split(",")]
        components.append(opacity)
        
        return "UIColor(red: {}, green: {}, blue: {}, alpha: {})".format(*components)


if __name__ == '__main__':
    main()


        