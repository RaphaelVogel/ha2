# Can be used to remove the -dbg files from SAP UI5 if it should be deployed
import os
rootDir = './ui5lib'
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        if '-dbg' in fname:
            fullname = os.path.join(dirName, fname)
            print('Remove ', fullname)
            os.remove(fullname)