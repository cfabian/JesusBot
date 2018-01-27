import json

def readConf(fileName):
    print('Reading %s...' % (fileName))
    with open(fileName) as f:
        conf = json.load(f)
        
    return conf
    
def readLists():
    print('Reading lists.json...')
    with open('lists.json', 'r') as f:
        lists = json.load(f)
        
    return lists
    
def writeLists(lists):
    print('Updating lists.json...')
    with open('lists.json', 'w') as f:
        json.dump(lists, f)
    
# readLists()