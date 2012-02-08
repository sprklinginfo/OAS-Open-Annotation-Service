
from meresco.core import Observable
from oas.utils import aboutNode
from oas.namespaces import namespaces


class AboutUriRewrite(Observable):

    def __init__(self, baseUrl):
        Observable.__init__(self)
        self._baseUrl = baseUrl

    def add(self, identifier, partname, lxmlNode):
        if identifier.startswith('urn:'):
            nodeWithAbout = aboutNode(lxmlNode)
            nodeWithAbout.attrib['{%(rdf)s}about' % namespaces] = self._baseUrl + identifier

        yield self.all.add(identifier=identifier, partname=partname, lxmlNode=lxmlNode)
