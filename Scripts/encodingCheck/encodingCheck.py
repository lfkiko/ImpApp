import os
import sys

# from Scripts.toolBoox import checkEndCode


# from Scripts.toolBoox import *


def main(argv):
    path = argv[0]
    files = os.listdir(path)
    # for file in files:
    #     # outPut = 'file name: '+file
    #     # print(file)
    #     # with open(os.path.join(path, file)) as rawData:
    #     #     encoding = rawData
    #     #     # outPut = outPut + ",  encoding: "+encoding
    #     #     print(encoding)
    #     # print(outPut)
    #     # encoding = checkEndCode(os.path.join(path, file))
    #     with open(os.path.join(path, file), 'rb') as f:
    #         raw = f.read(4)  # will read less if the file is smaller
    #     # encoding = detect_lite(raw)
    #     # print(encoding["encoding"])
    #
    print(files)


if __name__ == "__main__":
    main(sys.argv[1:])

#   0 - path for files
