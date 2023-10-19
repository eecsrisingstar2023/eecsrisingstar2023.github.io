from dataclasses import dataclass, field
from lxml import etree


PARENT_TAG = None


@dataclass
class Tag:
    tag: str
    attrib: dict = field(default_factory=dict)
    parent: object = None
    _text: str = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.element.text = value

    def __post_init__(self):
        self._make_element()
        self._append_to_parent()

    def write(self, filename):
        etree.ElementTree(self.element).write(filename)

    def _make_element(self):
        self.element = etree.Element(self.tag, attrib=self.attrib)

    def _append_to_parent(self):
        if self.parent is not None:
            self.parent.element.append(self.element)

    def __enter__(self):
        global PARENT_TAG
        if PARENT_TAG is not None:
            self.parent = PARENT_TAG
            self._append_to_parent()
        PARENT_TAG = self
        return self

    def __exit__(self, typ, value, traceback):
        global PARENT_TAG
        if PARENT_TAG is self:
            PARENT_TAG = self.parent