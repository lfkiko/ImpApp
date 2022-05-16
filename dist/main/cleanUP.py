import pandas as pd
from Scripts.toolBoox.toolBoox import rewriteText, readJson

if __name__ == "__main__":
    files = readJson('Scripts/Source/fileManger.json')
    for f in files:
        if f == 'settings':
            rewriteText(files[f], 'C:\\')
        elif files[f][-1] == 'm':
            pass
        
        elif files[f][-1] == 'v':
            df = pd.read_csv(files[f], header=None)
            df.head(1).to_csv(files[f], index=False, header=False)
       
