'''
Created on Dec 13, 2018

@author: anand
'''
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    pass

fileDir = 'D:/EcliplseProjects/'
inFile = 'test1'
metaFile = 'meta'
outFile = 'test1'

fileList = ['AA', 'BB', 'CC']

for suffix in fileList:
    print(suffix)

    meta_tree = ET.parse(fileDir+metaFile+'_'+suffix+'.xml')
    meta_root = meta_tree.getroot()
    #print( meta_root.tag, meta_root.attrib['recType'] )
    
    f = open(fileDir+outFile+'_'+suffix+'.csv', 'w')
    heading = ['dummy']
    emptyRec = ['dummy']
    for fld in meta_root:
        heading.insert(int(fld.attrib['num'])  , '"' + fld.attrib['Name'] + chr(10) +  fld.attrib['Opic'] + chr(10) + fld.attrib['key'] + '"')
        emptyRec.insert(int(fld.attrib['num']) , None)
       
    headstr = ''    
    for fld in heading:
        if (fld != 'dummy'):
            headstr = headstr + fld + ','
    
    f.write(headstr + '\n')  
    
    #print(outFileName)
    in_tree = ET.parse(fileDir+inFile+'_'+suffix+'.xml')
    in_root = in_tree.getroot()
    #print( in_root.tag, in_root.attrib['id'] )
    
    for rec in in_root:
        #print('   ',  rec.tag, rec.attrib['id'] )
        record = emptyRec.copy()
        for fld in rec:
            record.insert(int(fld.attrib['id']), '"' + fld.text + '"'  )
        
        recstr = ''    
        for fld in record:
            if (fld == 'dummy'):
                recstr = recstr    
            elif fld is None:
                recstr = recstr +  ','    
            else:    
                recstr = recstr + fld + ','    
        
        f.write(recstr + '\n')
    
    f.close() 
