from code_generator import CodeGenerator
from svg_parser import * 
from svg_colors import SVG_COLORS
from string import Template

def main():
    swiftGen = Swift3CodeGenerator()
    swiftGen.genCodeFromSVGFile("/Users/tiagobras/Documents/ChaosTokens/SVGs/skull.svg")

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
        self.GEN_MAP = {
            SVGRect: self._genRectCode,
            SVGPath: self._genPathCode,
            SVGEllipse: self._genEllipseCode
        }
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
            # print(type(node))

            if node.isDrawable:
                name = node.id
                if len(name) == 0:
                    name = "path%d" % pathIndex
                    pathIndex += 1

                f = self._getAppropriateCodeGeneratorForNode(node)
                s = f(node, name)
                
                print(s)


    def _genRectCode(self, rect, name, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)

        # s = indent + ("let {name} = UIBezierPath("
        #     "rect: CGRect(x: {x}, y: {y}, width: {width}, height: {height})"
        #     ")").format(name=name, **rect.__dict__)

        p1 = P(rect.x, rect.y).applyTransform(rect.transform)
        p2 = P(rect.x + rect.width, rect.y).applyTransform(rect.transform)
        p3 = P(rect.x + rect.width, rect.y + rect.height).applyTransform(rect.transform)
        p4 = P(rect.x, rect.y + rect.height).applyTransform(rect.transform)

        s = indent + "let %s = UIBezierPath()\n" % name
        s += indent + "%s.move(to: CGPoint(x: %f, y: %f))\n" % (name, p1.x, p1.y)
        s += indent + "%s.addLine(to: CGPoint(x: %f, y: %f))\n" % (name, p2.x, p2.y)
        s += indent + "%s.addLine(to: CGPoint(x: %f, y: %f))\n" % (name, p3.x, p3.y)
        s += indent + "%s.addLine(to: CGPoint(x: %f, y: %f))\n" % (name, p4.x, p4.y)
        s += indent + "%s.close()\n" % name
        
        s += self._genNodeStyleCode(rect, name, indentationLevel) 

        if self._hasStroke(rect):
            s += indent + "%s.stroke()\n" % name
        # if self._hasFill(rect):
        s += indent + "%s.fill()\n" % name

        # if not rect.transform.isIdentity:
        #     s += indent + "%s.apply(%s)" % (name, _genCGAffineTransform(rect.transform))

        return s

    def _genEllipseCode(self, ellipse, name, indentationLevel=0):
        indent = self._indentationForLevel(indentationLevel)
        K = 0.5522847498307935
        cx, cy = ellipse.cx, ellipse.cy
        rx, ry = ellipse.rx, ellipse.ry
        cdX, cdY = rx * K, ry * K

        p = P(cx, cy - ry).applyTransform(ellipse.transform)
        p1 = P(cx + rx, cy).applyTransform(ellipse.transform)
        p1c1 = P(cx + cdX, cy - ry).applyTransform(ellipse.transform)
        p1c2 = P(cx + rx, cy - cdY).applyTransform(ellipse.transform)
        p2 = P(cx, cy + ry).applyTransform(ellipse.transform)
        p2c1 = P(cx + rx, cy + cdY).applyTransform(ellipse.transform)
        p2c2 = P(cx + cdX, cy + ry).applyTransform(ellipse.transform)
        p3 = P(cx - rx, cy).applyTransform(ellipse.transform)
        p3c1 = P(cx - cdX, cy + ry).applyTransform(ellipse.transform)
        p3c2 = P(cx - rx, cy + cdY).applyTransform(ellipse.transform)
        p4 = P(cx, cy - ry).applyTransform(ellipse.transform)
        p4c1 = P(cx - rx, cy - cdY).applyTransform(ellipse.transform)
        p4c2 = P(cx - cdX, cy - ry).applyTransform(ellipse.transform)

        s = indent + "let %s = UIBezierPath()\n" % name
        s += indent + "%s.move(to: CGPoint(x: %f, y: %f))\n" % (name, p.x, p.y)
        s += indent + "{}.addCurve(to: CGPoint(x: {}, y: {}), ".format(name, p1.x, p1.y) + \
            "controlPoint1: CGPoint(x: {}, y: {}), ".format(p1c1.x, p1c1.y) + \
            "controlPoint2: CGPoint(x: {}, y: {}))\n".format(p1c2.x, p1c2.y)

        s += indent + "{}.addCurve(to: CGPoint(x: {}, y: {}), ".format(name, p2.x, p2.y) + \
            "controlPoint1: CGPoint(x: {}, y: {}), ".format(p2c1.x, p2c1.y) + \
            "controlPoint2: CGPoint(x: {}, y: {}))\n".format(p2c2.x, p2c2.y)

        s += indent + "{}.addCurve(to: CGPoint(x: {}, y: {}), ".format(name, p3.x, p3.y) + \
            "controlPoint1: CGPoint(x: {}, y: {}), ".format(p3c1.x, p3c1.y) + \
            "controlPoint2: CGPoint(x: {}, y: {}))\n".format(p3c2.x, p3c2.y)

        s += indent + "{}.addCurve(to: CGPoint(x: {}, y: {}), ".format(name, p4.x, p4.y) + \
            "controlPoint1: CGPoint(x: {}, y: {}), ".format(p4c1.x, p4c1.y) + \
            "controlPoint2: CGPoint(x: {}, y: {}))\n".format(p4c2.x, p4c2.y)
        s += indent + "%s.close()\n" % name
        
        s += self._genNodeStyleCode(ellipse, name, indentationLevel) 
        if self._hasStroke(ellipse):
            s += indent + "%s.stroke()\n" % name
        # if self._hasFill(ellipse):
        s += indent + "%s.fill()\n" % name

        return s

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


        