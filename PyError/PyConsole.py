def PrintHeader(header):
    pHeader = "||=====[" + header + "]=====||"
    print(pHeader)

def PrintSubHeader(subHead):
    pSubHead = "[---[" + subHead + "]---]"
    print(pSubHead)

def PrintNumberedList(mList):
    
    for index, item in enumerate(mList):
        print(index + 1, "-", item)

# Debug

PrintHeader("Test Header")
PrintSubHeader("Test SubHeader")
PrintNumberedList(["Test One", "Test Two", "Test Three"])