from lxml import etree

class XMLTool():
    """ XML Helper Class working with xml File """
    def __init__(self, filename):
        self.filename = filename
        self.open()
            
    def open(self):
        """ read the xml file """
        try:               
            # read Binary Stream
            data = open(self.filename, 'rb')
            xslt_content = data.read()
            self.root = etree.XML(xslt_content)
        except Exception as e:
            print(e)
            
    def find(self, node):
        """ find a node """        
        return self.root.find(node)    
            
            
    def getRoot(self):
        """ return root Node """
        return self.root
    
    def print_all_childs(self, node):
        """ iterate over all sub nodes """
        for element in node.iter():
            print("%s - %s" % (element.tag, element.text))

    def changeText(self, node, text):
        """ change the text attrib from node """
        node.text = text
        
    def find_chain(self, elements, ns=None):
        """ 
        search the node in chain list elements
        e.g. [elem1, elem2, elem3]
        will return elem3 
        """
        if ns != None:
            elem = self.root.find('{%s}%s' % (ns, elements[0]))
        else:
            elem = self.root.find(elements[0])
        for i in range(1, len(elements)):
            if ns != None:
                elem = elem.find('{%s}%s' % (ns, elements[i]))
            else:
                elem = elem.find(elements[i])
        return elem
       
    def write(self, filename=None):
        """ save the xml file to disk """
        try:
            tree = etree.ElementTree(self.root)
            if filename is None:
              tree.write(self.filename, pretty_print=True, xml_declaration=True, encoding=None)
            else:
              tree.write(filename, pretty_print=True, xml_declaration=True, encoding=None)
        except Exception as e:
            print(e)
            
        
            
