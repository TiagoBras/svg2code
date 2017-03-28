from __future__ import absolute_import, division, print_function

import re
import xml.etree.ElementTree as ElementTree
from svg_colors import SVG_COLORS

class RGBAColor(object):
    """rgba color format: [0.0, 1.0]"""
    def __init__(self, r=0.0, g=0.0, b=0.0, a=0.0):
        super(RGBAColor, self).__init__()
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)
        self.a = float(a)

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
        self.style = parent.style.copy() if parent is not None else {
            "fill": "black"
        }
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
            print("Cannot multiply the two matrices. Incorrect dimensions.")
            return

        C = [[0 for row in range(cols_B)] for col in range(rows_A)]

        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    C[i][j] += self[i][k] * other[k][j]
        return M(C)
