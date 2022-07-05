from lxml import etree
import re

class XMLTool():
    """ XML Helper Class working with xml File """
    def __init__(self, filename):
        self.filename = filename
        self.open()
            
    def open(self):
        """ read the xml file """
        try:
            with open(self.filename) as fobj:
                xml = fobj.read()
                self.root = etree.fromstring(xml)
        except Exception as e:
            print(e)
            
    #https://www.python101.pythonlibrary.org/chapter31_lxml.html
            
            
            
            
    def find(self, key):
        """ find a key """        
        return etree.Element(key)
        
            
            
            
            
            
            
            
            
            
            
            
            
            
    def getRoot(self):
        """ return root Node """
        return self.root

    def print_xml_file(self):
        """ print out full formated xml file """
        ET.indent(self.root)
        print(ET.tostring(self.root, encoding='unicode'))
        
    def print_all_childs(self, elem):
        for child in elem:
            print(child.tag)
            
    def register_all_namespaces(self):
        namespaces = dict([node for _, node in ET.iterparse(self.filename, events=['start-ns'])])
        for ns in namespaces:
            print(ns)
            ET.register_namespace(ns, namespaces[ns])

    def getXMLS(self):
        """ get first xmlns String """
        self.xmlns = None
        self.register_all_namespaces()
        
        my_namespaces = dict([node for _, node in ET.iterparse(self.filename, events=['start-ns'])])
        print(my_namespaces)
        
        #for elem in self.tree.iter():
        #    print(elem)
        #    print(elem.get('xmlns'))
        """
        m = re.findall('{.*}', str(xml))
        print(m)
        
        if m:
            self.xmlns = m.group(0)
        """
 
            
    def find2(self, node, key):
        """ find a key from node, use xmlns if present """        
        elem = None
        if self.xmlns != None:
            elem = node.find("%s%s" % (self.xmlns, key))
        else:
            elem = node.find("%s" % key)
        return elem
    
    def find_chain(self, elements):
        """ 
        search the node in chain list elements
        e.g. [elem1, elem2, elem3]
        will return elem3 
        """
        elem = self.find(self.getRoot(), elements[0])
        for i in range(1, len(elements)):
            elem = self.find(elem, elements[i])
        return elem
    
    def getUrlfromXmlns(self):
        """ get the url from xmlNamespace """
        return self.xmlns[1:-1]
    
    
    def write(self):
        """ save the xml file to disk """
        try:
            # define Namespace, otherwise we will get nso, ns1 etc.
            print(self.xmlns)
            print(self.getUrlfromXmlns())
            ET.register_namespace("", self.getUrlfromXmlns())
            self.tree.write(self.filename)
        except Exception as e:
            print(e)
        
            
