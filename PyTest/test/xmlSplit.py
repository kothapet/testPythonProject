'''
Created on Dec 13, 2018

@author: anand
'''
from _overlapped import NULL

if __name__ == '__main__':
    pass

'''
d = dict()

for i in range(100):
    key = i % 10
    if key in d:
        d[key] += 1
    else:
        d[key] = 1
        
print(d)       
'''

import xml.etree.ElementTree as ET

fileDir = 'D:/EcliplseProjects/'
inFileName = 'test1.xml'

outFileName = inFileName.replace('.xml', '')
#print(outFileName)

tree = ET.parse(fileDir+inFileName)
root = tree.getroot()
print(root, root.tag, root.attrib )


#dummy_root= ET.Element(root.tag)
#print('dummy_root : ', dummy_root  )

split_xml = dict()

for child in root:
    print(child, child.tag, child.attrib )
    att1 = child.attrib['id'] 
    print(att1, type(att1))

    if not (att1 in split_xml):
        split_xml[att1] = ET.Element(root.tag, child.attrib)

    split_xml[att1].append(child) 
    
print(type(split_xml), split_xml )
         
for idx in split_xml:
    print(idx + ':')
    ET.ElementTree(split_xml[idx]).write(fileDir+outFileName+'_'+idx+'.xml')
    
