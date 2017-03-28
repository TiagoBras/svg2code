import re
import xml.etree.ElementTree as ElementTree

from svg_colors import SVG_COLORS

TEXT = "M374.52,15.976L375.212,15.981C376.744,16.012 378.138,16.637 379.56,17.128C380.346,17.39 382.445,20.178 383.281,20.318C386.354,20.83 389.262,24.261 391.92,26.21C393.785,27.578 395.385,28.877 397.015,30.507C399.398,32.891 401.65,35.887 403.881,38.437C406.105,40.979 406.09,42.523 408.223,45.082C409.336,46.418 410.459,48.471 411.545,49.556C413.402,51.413 413.491,50.349 415.178,55.891C415.798,57.929 420.349,62.354 422.288,66.233C423.43,68.516 424.374,70.39 425.101,72.814C425.711,74.846 426.444,77.373 427.165,79.295C428.702,83.395 429.775,87.345 430.506,91.731C431.243,96.153 431.393,101.745 432.632,106.084C433.21,108.107 434.105,111.421 435.069,113.349C437.852,118.915 437.498,125.851 440.961,130.937C443.796,135.101 444.875,140.626 448.492,144.891C450.22,146.929 450.595,152.95 451.958,156.13C453.942,160.761 457.357,163.211 460.429,166.897C461.584,168.283 462.51,170.699 463.042,172.296C463.618,174.024 465.085,175.153 466.177,176.824C468.683,180.661 468.777,183.938 469.753,187.841C470.652,191.435 468.795,199.332 466.051,202.381C454.029,215.745 437.611,217.402 428.732,214.443C424.398,212.998 420.511,212.239 416.294,211.034C413.75,210.308 410.895,209.073 408.356,208.347C405.737,207.599 401.054,204.149 399.822,205.387C395.37,209.856 380.287,225.199 374.936,230.55C373.476,232.01 370.536,235.334 370.278,235.142C369.615,234.65 366.434,231.25 365.05,230.236C360.724,227.068 358.371,222.836 354.133,219.305C353.194,218.522 351.164,216.167 350.254,215.257C347.447,212.45 343.784,208.002 340.077,206.149C339.515,205.868 328.429,210.836 327.427,211.265C325.476,212.101 323.943,212.626 321.972,213.05C315.619,214.414 315.507,213.233 305.555,214.639C304.027,214.855 301.796,214.97 299.386,214.952C295.995,214.928 289.82,212.768 286.945,210.703C283.262,208.058 280.925,205.892 277.708,202.556C273.107,197.784 270.206,191.229 271.114,183.967C272.383,173.816 277.704,167.154 283.969,159.323C284.943,158.105 286.124,155.891 286.899,154.342C288.093,151.953 289.389,148.989 290.624,146.521C292.355,143.057 294.614,140.106 296.371,136.593C299.562,130.21 301.107,123.082 303.337,116.391C304.511,112.868 306.869,109.8 308.039,106.29C309.751,101.154 311.044,96.264 312.859,91.113C314.675,85.957 313.343,84.166 315.319,80.214C316.843,77.168 318.614,73.884 320.3,69.9C321.42,67.255 323.754,63.934 324.933,61.182C325.953,58.802 326.394,56.118 327.894,53.867C329.298,51.762 331.273,49.843 332.77,47.598C336.317,42.277 340.221,37.684 344.119,34.14L348.328,30.02C350.497,27.521 352.048,26.044 354.663,24.615C358.474,22.533 364.667,17.091 368.125,16.597C370.019,16.353 371.915,16.045 373.828,15.982L374.52,15.976ZM367.374,112.842C366.588,112.932 366.894,112.835 366.428,113.022C364.286,114.307 364.91,121.627 360.102,124.661C357.536,126.279 353.408,125.054 350.491,126.027L344.033,128.113C337.708,128.21 332.014,129.625 331.337,135.823C331.171,137.344 336.353,146.506 336.837,149.023C337.658,153.293 341.752,159.528 343.71,163.807C344.793,166.176 350.128,170.038 351.098,171.678C354.009,176.597 359.471,183.222 366.839,184.146C370.563,184.612 380.345,184.315 382.293,180.419C382.736,179.534 382.255,178.496 382.56,177.58C382.965,176.366 383.629,175.424 383.825,174.247C384.086,172.683 381.753,172.729 382.48,171.276C382.749,170.737 386.122,169.795 386.656,169.429C388.443,168.204 390.111,167.022 391.073,165.627C393.342,162.341 395.181,153.62 397.353,149.275C399.062,145.856 405.669,141.006 403.843,136.44C400.749,128.705 388.7,128.95 382.074,126.465C380.48,125.868 377.708,124.35 376.18,122.251C373.235,118.208 373.36,116.483 372.751,113.535C372.644,113.018 369.968,113.029 369.388,112.977C368.718,112.894 368.048,112.864 367.374,112.842Z"

def main():
    svg = SVG.fromFile('/Users/tiagobras/Documents/ChaosTokens/SVGs/skull2.svg')

class RGBAColor(object):
    """rgba color format: [0.0, 1.0]"""
    def __init__(self, r=0.0, g=0.0, b=0.0, a=0.0):
        super(RGBAColor, self).__init__()
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @property
    def components(self):
        return [self.r, self.g, self.b, self.a]

    def __eq__(self, o):
        return self.r == o.r and self.g == o.g and self.b == o.b and self.a == o.a

    def __ne__(self, o):
        return not (self == o)

class SVGNode(object):
    def __init__(self, xml, parent=None, isDrawable=False):
        super(SVGNode, self).__init__()
        self.parent = parent
        self.depth = 0 if parent is None else parent.depth + 1
        self.id = self._genId(xml, parent)
        self.transform = self._parseTransform(xml)
        self.isDrawable = isDrawable
        # print(("-"*self.depth) + re.sub(r'\{[^\}]+\}', '', xml.tag) + " " + self.id or self.parent.id)
        self.style = parent.style.copy() if parent is not None else {}
        self.style.update(self._parseStyle(xml))
        
        if parent is not None:
            self.transform = parent.transform * self.transform

        self.children = self._parseChildren(xml, self)

    def _genId(self, xml, parent):
        newId = xml.attrib.get("id")

        if newId is not None:
            return newId

        if parent is None:
            return ""

        newId = parent.id

        m = re.search(r'(?P<n>\d+)$', newId)

        if m is not None:
            return re.sub(r'\d+$', str(int(m.group('n')) + 1), newId)
        else:
            return newId + '1' if parent.isDrawable else newId

    def _parseTransform(self, xml):
        if "transform" in xml.attrib:
            if not xml.attrib["transform"].startswith("matrix"):
                raise TypeError("%s does not start with matrix" % xml.attrib["transform"])

            f = [float(x) for x in xml.attrib["transform"][7:-1].split(",")]

            return M.withComponents(*f)
        else:
            return M()

    def _parseStyle(self, xml):
        if "style" in xml.attrib:
            styleArray = [x for x in xml.attrib["style"].split(';') if len(x) > 0]

            style = {}
            for el in styleArray:
                key, value = el.split(':')

                style[key.replace('-', '_')] = value

            return style
        else:
            return {}


    def _parseChildren(self, xml, parent):
        children = []
        for child in xml:
            tag = re.sub(r'\{[^\}]+\}', '', child.tag)

            if tag == "g":
                children.append(SVGGroup(child, parent))
            else:
                children.append(SVGPath(child, parent))

        return children

    def _getColorForKey(self, colorKey):
        color = self.style.get(colorKey)

        if color is None:
            return None

        color = SVG_COLORS.get(color) or color

        if color == 'inherit':
            return None
        elif color == "none":
            return RGBAColor(0.0, 0.0, 0.0, 0.0)
        elif color.startswith("rgb("):
            components = [int(x) / 255.0 for x in color[4:-1].split(",")]
            components.append(self.style.get(colorKey + "_opacity", 1.0))

            return RGBAColor(*components)

        raise NotImplementedError("%s color format is not implemented" % fillColor)

    @property
    def isVisible(self):
        fillColor = self.rgbaFillColor or RGBAColor(0.0, 0.0, 0.0, 0.0)
        strokeColor = self.rgbaStrokeColor or RGBAColor(0.0, 0.0, 0.0, 0.0)

        return fillColor.a > 0.0 or strokeColor.a > 0.0

    @property
    def rgbaFillColor(self):
        return self._getColorForKey("fill")

    @property
    def rgbaStrokeColor(self):
        return self._getColorForKey("stroke")

    @property
    def strokeWidth(self):
        width = self.style.get("stoke_width")

        if width is None or width == "inherit":
            return None

        if not width.endswith('px') or len(width) <= 2:
            raise NotImplementedError("%s stroke width format is not implemented" % width)

        return float(width[:-2])

    @property
    def strokeLineCap(self):
        cap = self.style.get("stroke_linecap")

        return None if cap is None or cap == "inherit" else cap

    @property
    def strokeMiterLimit(self):
        miter = self.style.get("stroke_miterlimit")

        return None if miter is None or miter == "inherit" else miter

    @property
    def usesEvenOddFillRule(self):
        return self.style.get("fill_rule", "nonzero") == "evenodd"

class SVG(SVGNode):
    def __init__(self, xml, parent=None):
        super(SVG, self).__init__(xml, parent)
        self.x, self.y, self.width, self.height = self._parseViewBox(xml)

    @classmethod
    def fromFile(cls, filename):
        tree = ElementTree.parse(filename)

        return cls(tree.getroot())

    @classmethod
    def fromString(cls, string):
        root = ElementTree.fromstring(string)

        return cls(root)

    @property
    def name(self):
        for node in self.iterator:
            if node.id:
                return node.id
        return None

    @property
    def iterator(self):
        """Depth-First iterator"""
        stack = [self]

        while stack:
            node = stack.pop()

            yield node

            for child in reversed(node.children):
                stack.append(child)

    def _parseViewBox(self, xml):
        if "viewBox" in xml.attrib:
            return [float(x) for x in xml.attrib["viewBox"].split(' ')]
        else:
            return [0, 0, 0, 0]

class SVGGroup(SVGNode):
    def __init__(self, xml, parent=None):
        super(SVGGroup, self).__init__(xml, parent)

TRAILING_ZEROS_RE = re.compile(r'\.?0+$')
def removeTrailingZeros(s):
    result = TRAILING_ZEROS_RE.sub('', s) if '.' in s else s
    # return result if '.' in result else result + '.0'
    return result
 
class SVGPath(SVGNode):
    def __init__(self, xml, parent=None):
        super(SVGPath, self).__init__(xml, parent, True)
        tag = re.sub(r'\{[^\}]+\}', '', xml.tag)

        d = xml.attrib.get("d")

        if tag == "rect":
            d = self._rectToPath(xml)
        elif tag == "ellipse":
            d = self._ellipseToPath(xml)
        elif tag == "circle":
            d = self._ellipseToPath(xml)

        if d is None:
            raise NotImplementedError("'%s' path converter is not yet implemented" % tag)

        self.commands = self._parseCommands(d)
        
    def _parseCommands(self, d):
        COMMANDS_RE = re.compile(r"([MmZzLlHhVvCcSsQqTtAa])")

        tokens = [x for x in COMMANDS_RE.split(d) if len(x) > 0]
        
        i = 0
        commands = []
        while i < len(tokens):
            command = tokens[i]
            coordinates = tokens[i+1] if i+1 < len(tokens) else None

            if command.islower():
                raise TypeError("%s is relative." % command)

            if command == 'M':
                i += 2
                commands.append(MoveTo(coordinates))
            elif command == 'L':
                i += 2
                commands.append(LineTo(coordinates))
            elif command == 'C':
                i += 2
                commands.append(CurveTo(coordinates))
            elif command == 'Z':
                i += 1
                commands.append(ClosePath())
            else:
                raise NotImplementedError("Command %s is not implemented" % command)

        return commands

    def _rectToPath(self, xml):
        x = float(xml.attrib.get("x", 0.0))
        y = float(xml.attrib.get("y", 0.0))
        width = float(xml.attrib.get("width", 0.0))
        height = float(xml.attrib.get("height", 0.0))
  
        points = [x, y, x + width, y, x + width, y + height, x, y + height]

        a, b, c, d, e, f, g, h = [removeTrailingZeros(str(n)) for n in points]

        return "M%s,%sL%s,%sL%s,%sL%s,%sZ" % (a, b, c, d, e, f, g, h)

    def _ellipseToPath(self, xml):
        cx = float(xml.attrib.get("cx", 0.0))
        cy = float(xml.attrib.get("cy", 0.0))
        rx = float(xml.attrib.get("rx", xml.attrib.get("r", 0.0)))
        ry = float(xml.attrib.get("ry", xml.attrib.get("r", 0.0)))
        K = 0.5522847498307935
        cdX, cdY = rx * K, ry * K

        points1 = [cx, cy - ry]
        points2 = [cx + rx, cy, cx + cdX, cy - ry, cx + rx, cy - cdY]
        points3 = [cx, cy + ry, cx + rx, cy + cdY, cx + cdX, cy + ry]
        points4 = [cx - rx, cy, cx - cdX, cy + ry, cx - rx, cy + cdY]
        points5 = [cx, cy - ry, cx - rx, cy - cdY, cx - cdX, cy - ry]

        px, py = [removeTrailingZeros(str(n)) for n in points1]
        p1x, p1y, p1x1, p1y1, p1x2, p1y2 = [removeTrailingZeros(str(n)) for n in points2]
        p2x, p2y, p2x1, p2y1, p2x2, p2y2 = [removeTrailingZeros(str(n)) for n in points3]
        p3x, p3y, p3x1, p3y1, p3x2, p3y2 = [removeTrailingZeros(str(n)) for n in points4]
        p4x, p4y, p4x1, p4y1, p4x2, p4y2 = [removeTrailingZeros(str(n)) for n in points5]

        return "M{},{}C{},{} {},{} {},{}".format(px, py, p1x1, p1y1, p1x2, p1y2, p1x, p1y) + \
            "C{},{} {},{} {},{}".format(p2x1, p2y1, p2x2, p2y2, p2x, p2y) + \
            "C{},{} {},{} {},{}".format(p3x1, p3y1, p3x2, p3y2, p3x, p3y) + \
            "C{},{} {},{} {},{}Z".format(p4x1, p4y1, p4x2, p4y2, p4x, p4y)

class MoveTo(object):
    def __init__(self, coordinates):
        super(MoveTo, self).__init__()
        xy = coordinates.split(',')
        self.x = float(xy[0])
        self.y = float(xy[1])

    def __repr__(self):
        return "(M %f,%f)" % (self.x, self.y)

class LineTo(object):
    def __init__(self, coordinates):
        super(LineTo, self).__init__()
        xy = coordinates.split(',')
        self.x = float(xy[0])
        self.y = float(xy[1])

    def __repr__(self):
        return "(L %f,%f)" % (self.x, self.y)

class CurveTo(object):
    def __init__(self, coordinates):
        super(CurveTo, self).__init__()
        x1y1x2y2xy = [x.split(',') for x in coordinates.split(' ')]
        self.x1 = float(x1y1x2y2xy[0][0])
        self.y1 = float(x1y1x2y2xy[0][1])
        self.x2 = float(x1y1x2y2xy[1][0])
        self.y2 = float(x1y1x2y2xy[1][1])
        self.x = float(x1y1x2y2xy[2][0])
        self.y = float(x1y1x2y2xy[2][1])

    def __repr__(self):
        return "(C %f,%f %f,%f %f,%f)" % (self.x1, self.y1, self.x2, self.y2, self.x, self.y)

class ClosePath(object):
    def __init__(self):
        super(ClosePath, self).__init__()
    
    def __repr__(self):
        return "(Z)"
            
class P(object):
    def __init__(self, x=0.0, y=0.0, z=1.0):
        self.x, self.y, self.z  = float(x), float(y), float(z)
  
    def __repr__(self): 
        return "(%f, %f, %f)" % (self.x, self.y, self.z)
  
    def applyTransform(self, m):
        x = m.a*self.x + m.c*self.y + m.e*self.z
        y = m.b*self.x + m.d*self.y + m.f*self.z
        z = m[2][0]*self.z + m[2][1]*self.y + m[2][2]*self.z

        return P(x, y, z)

class M(object):
    def __init__(self, array=None, **kwargs):
        super(M, self).__init__()
        self.array = array or [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0]]
        
        if array is None and len(kwargs) > 0:
            self.a = kwargs.get("a", 1.0)
            self.b = kwargs.get("b", 0.0)
            self.c = kwargs.get("c", 0.0)
            self.d = kwargs.get("d", 1.0)
            self.e = kwargs.get("e", 0.0)
            self.f = kwargs.get("f", 0.0)
            
        for r in range(0, 3):
            for c in range(0, 3):
                self.array[r][c] = float(self.array[r][c])
    
    @property
    def isIdentity(self):
        for r in range(0, 3):
            for c in range(0, 3):
                if r == c and self.array[r][c] != 1.0:
                    return False
                if r != c and self.array[r][c] != 0.0:
                    return False
        return True

    @classmethod
    def withComponents(cls, *args):
        if len(args) != 6:
            raise ValueError("Should these 6 components: a, b, c, d, e, f")
      
        m = cls(a=args[0], b=args[1], c=args[2], d=args[3], e=args[4], f=args[5])
      
        return m
      
    def __repr__(self): 
        maxLen = 0
        arrayStr = []
  
        for r in range(0, 3):
            arrayStr.append(["", "", ""])
        
            for c in range(0, 3):
                s = str(self[r][c])
                sLen = len(s)
          
                if sLen > maxLen:
                    maxLen = sLen
                arrayStr[r][c] = s
      
        f = '{:>' + str(maxLen) + 's} {:>' + str(maxLen) + 's} {:>' + str(maxLen) + 's}'

        return "\n".join([f.format(r[0], r[1], r[2]) for r in arrayStr])
      
    @property
    def a(self): return self.array[0][0]
    @a.setter
    def a(self, a): self.array[0][0] = float(a)
    @property
    def b(self): return self.array[1][0]
    @b.setter
    def b(self, b): self.array[1][0] = float(b)
    @property
    def c(self): return self.array[0][1]
    @c.setter
    def c(self, c): self.array[0][1] = float(c)
    @property
    def d(self): return self.array[1][1]
    @d.setter
    def d(self, d): self.array[1][1] = float(d)
    @property
    def e(self): return self.array[0][2]
    @e.setter
    def e(self, e): self.array[0][2] = float(e)
    @property
    def f(self): return self.array[1][2]
    @f.setter
    def f(self, f): self.array[1][2] = float(f)
    
    def __getitem__(self, index):
        return self.array[index]
      
    def __len__(self):
        return len(self.array)
    
    def __mul__(self, other):
        rows_A = len(self)
        cols_A = len(self[0])
        rows_B = len(other)
        cols_B = len(other[0])

        if cols_A != rows_B:
            print "Cannot multiply the two matrices. Incorrect dimensions."
            return

        C = [[0 for row in range(cols_B)] for col in range(rows_A)]

        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    C[i][j] += self[i][k] * other[k][j]
        return M(C)

if __name__ == '__main__':
    main()