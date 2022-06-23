

from xml.dom import minidom

# parse an xml file by name
file = minidom.parse('G4Data1.heprep')

#use getElementsByTagName() to get tag
models = file.getElementsByTagName('heprep:attvalue')
models2 = file.getElementsByTagName('heprep:point')

# one specific item attribute
print('model #2 attribute:')
print(models[1].attributes['name'].value)

# all item attributes
#print('\nAll attributes:')
for elem in models:
    print(elem.attributes['name'].value)
    print(elem.attributes['value'].value)

for elem in models2:
    print(elem.attributes['x'].value)
    print(elem.attributes['y'].value)

models = file.getElementsByTagName('heprep:instance')
# one specific item's data
print('\nmodel #2 data:')
print(models[1].firstChild.data)
print(models[1].childNodes[0].data)

## all items data
#print('\nAll model data:')
#for elem in models:
#  print(elem.)  

# importing element tree
import xml.etree.ElementTree as ET 

# Pass the path of the xml document 
tree = ET.parse('G4Data1.heprep') 

# get the parent tag 
root = tree.getroot() 

# print the root (parent) tag along with its memory location 
print(root.tag) 

# print the attributes of the first tag  
print(root[1].attrib) 

# print the text contained within first subtag of the 5th tag from the parent 
print(root[0].text) 

for child in root:
     print(child.tag, child.attrib, child.get('x'))

Listk = [elem.attrib for elem in root.iter()]
print(Listk[1000:1040])

for Da in Listk:
    print(Da.values)

print(ET.tostring(root, encoding='utf8').decode('utf8'))

