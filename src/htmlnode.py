class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        s = ""
        if self.props:
            for k, v in self.props.items():
                s += f" {k}=\"{v}\""
        return s
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return  self.props == other.props and \
        self.value == other.value and \
        self.children == other.children and \
        self.tag == other.tag
    
