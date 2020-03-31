import sys
from xml.dom import minidom
from collections import OrderedDict
import operator

class CMDI():
    def __init__(self, url=None, content=None, debug=False):
        self.url = url
        self.stats = {}
        self.json = {}

    def dappend(self, dictionary, key, item):
        """Append item to dictionary at key.  Only create a list if there is more than one item for the given key.
        dictionary[key]=item if key doesn't exist.
        dictionary[key].append(item) if key exists."""
        if key in dictionary.keys():
            if not isinstance(dictionary[key], list):
                lst=[]
                lst.append(dictionary[key])
                lst.append(item)
                dictionary[key]=lst
            else:
                dictionary[key].append(item)
        else:
            dictionary.setdefault(key, item)

    def getstats(self, order=True):
        return sorted(self.stats.items(),key=operator.itemgetter(1),reverse=order)

    def node_attributes(self, node):
        """Return an attribute dictionary """
        if node.hasAttributes():
            return dict([(str(attr), str(node.attributes[attr].value)) for attr in node.attributes.keys()])
        else:
            return None

    def attr_str(self, node):
        return "%s-attrs" % str(node.nodeName)

    def hasAttributes(self, node):
        if node.nodeType == node.ELEMENT_NODE:
            if node.hasAttributes():
                return True
        return False

    def with_attributes(self, node, values):
        if node.nodeName in self.stats:
            self.stats[node.nodeName] = self.stats[node.nodeName] + 1
        else:
            self.stats[node.nodeName] = 1

        if self.hasAttributes(node):
            if isinstance(values, dict):
                self.dappend(values, '#attributes', self.node_attributes(node))
                return { str(node.nodeName): values }
            elif isinstance(values, str):
                return { str(node.nodeName): values,
                         attr_str(node): self.node_attributes(node)}
        else:
            return { str(node.nodeName): values }

    def xmldom2dict(self, node):
        """Given an xml dom node tree,
        return a python dictionary corresponding to the tree structure of the XML.
        This parser does not make lists unless they are needed.  For example:

        '12' becomes:
        { 'list' : { 'item' : ['1', '2'] } }
        BUT
        '1' would be:
        { 'list' : { 'item' : '1' } }

        This is a shortcut for a particular problem and probably not a good long-term design.
        """
        if not node.hasChildNodes():
            if node.nodeType == node.TEXT_NODE:
                if node.data.strip() != '':
                    return str(node.data.strip())
                else:
                    return None
            else:
                return self.with_attributes(node, None)
        else:
            #recursively create the list of child nodes
            childlist=[self.xmldom2dict(child) for child in node.childNodes if (self.xmldom2dict(child) != None and child.nodeType != child.COMMENT_NODE)]
            if len(childlist)==1:
                return self.with_attributes(node, childlist[0])
            else:
                #if False not in [isinstance(child, dict) for child in childlist]:
                new_dict={}
                for child in childlist:
                    if isinstance(child, dict):
                        for k in child:
                            self.dappend(new_dict, k, child[k])
                    elif isinstance(child, str):
                        self.dappend(new_dict, '#text', child)
                    else:
                        print "ERROR"
                return self.with_attributes(node, new_dict)

    def load(self, fname):
        self.json = self.xmldom2dict(minidom.parse(fname))
        #print(self.stats)
        #return x
        return self.xmldom2dict(minidom.parse(fname))

    def lispy_string(node, lst=None, level=0):
        if lst==None:
            lst=[]
        if not isinstance(node, dict) and not isinstance(node, list):
            lst.append(' "%s"' % node)
        elif isinstance(node, dict):
            for key in node.keys():
                lst.append("\n%s(%s" % (spaces(level), key))
                lispy_print(node[key], lst, level+2)
                lst.append(")")
        elif isinstance(node, list):
            lst.append(" [")
            for item in node:
                lispy_print(item, lst, level)
            lst.append("]")
        return lst

