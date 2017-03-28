class CodeGenerator(object):
    def __init__(self):
        super(CodeGenerator, self).__init__()
    
    def genCode(self, filename):
        return ""

class CodeGeneratorOptions(object):
    def __init__(self, **kwargs):
        super(CodeGeneratorOptions, self).__init__()
        self.path = kwargs.get("path") or None
        self.className = kwargs.get("className", "SVGDrawablesKit")
        self.useTabs = kwargs.get("useTabs", False)
        self.spaces = kwargs.get("spaces", 4)

    @property
    def indentation(self):
        return "\t" if self.useTabs else " " * self.spaces