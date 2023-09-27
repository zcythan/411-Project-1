from sklearn.tree import DecisionTreeClassifier

class FeatExt:
    def __init__(self, name):
        self.__fileName = name
        self.__featVectors = []
        self.__featLabels = []

    @staticmethod
    def __analyzeRL(vectorRL, boolz):
        # Abbreviation means it do not in fact be da end of da sentence
        abbrev = ["Dr", "Rep", "Mr", "St", "Pres", "Ald", "Prof", "Gen", "Sen", "Gov"]
        # [Left word, Right word, L < 3, L capital, R capital, L length, R length, is L on list of abbreviations?]
        vector = [vectorRL[0], vectorRL[1], 0, 0, 0, 0, 0, 0]

        if len(vector[0]) < 3:
            vector[2] = 1
        else:
            vector[2] = 0
        if vector[0] and vector[0][0].isupper():
            vector[3] = 1
        if vector[0] and vector[1][0].isupper():
            vector[4] = 1
        vector[5] = len(vector[0])
        vector[6] = len(vector[1])
        for abr in abbrev:
            if abr in vector[0]:
                vector[7] = 1

        #Gonna see if just using ASCII representation is good enough.
        intL = ""
        intR = ""

        for char in vector[0]:
            temp = ord(char)
            intL = intL + str(temp)
        if intL.isdigit():
            vector[0] = int(intL)
        else:
            vector[0] = 0

        for char in vector[1]:
            temp = ord(char)
            intR = intR + str(temp)
        if intR.isdigit():
            vector[1] = int(intR)
        else:
            vector[1] = 0

        if boolz:
            vectorStr = ""
            for i, var in enumerate(vector):
                if type(var) is int:
                    vectorStr += str(var) + "; "
                    continue
                vectorStr += str(var) + "; "

            return vectorStr
        return vector

    @staticmethod
    def __outcome(line):
        if "EOS" in line and "NEOS" not in line:
            return 1
        else:
            return 0

    @staticmethod
    def __extractRL(line, nextLine):
        vector = ["null", "null"]

        for i, char in enumerate(line):
            if char == '.' and (i + 1 < len(line)) and line[i+1] == " ":
                j = i - 1
                val = ""
                #Builds left side of period
                while j >= 0:
                    if line[j] == " ":
                        vector[0] = val
                        break
                    val = line[j] + val
                    j = j - 1
                j = 0
                val = ""
                prevCh = ''
                #substringing right of period
                for ch in nextLine:
                    if ch == " " and prevCh.isalpha():
                        vector[1] = val
                        break
                    prevCh = ch
                    if ch.isalpha():
                        val = val + nextLine[j]
                    j = j + 1

        return vector

    @property
    def getLabels(self):
        return self.__featLabels

    def readFile(self):
        with open(self.__fileName, 'r') as file:
            with open('SBD.answers', 'w') as out:
                prevLine = ""
                check = False
                #checking to see if TOK line may have word after period in it.
                for line in file:
                    skip = True
                    chkLine = line.replace("TOK", "")
                    for char in chkLine:
                        if char.isalpha():
                            skip = False
                            break
                    if skip:
                        continue
                    if check:
                        out.write(str(self.__outcome(prevLine)) + " " + self.__analyzeRL(self.__extractRL(prevLine, line), True) + '\n')
                        self.__featVectors.append(self.__analyzeRL(self.__extractRL(prevLine, line), False))
                        self.__featLabels.append(self.__outcome(prevLine))
                        check = False
                    if '.' in line and "TOK" not in line:
                        prevLine = line
                        check = True

        return self.__featVectors

class AccCalc:
    def __init__(self):
        self.x = 0

def main():
    print("Hello world")
    extractor = FeatExt("SBD.train")
    featureVectors = extractor.readFile()
    featureLabels = extractor.getLabels
    magicTree = DecisionTreeClassifier()
    magicTree.fit(featureVectors, featureLabels)

    #needs to take in one at a time and will return an integer
    #prediction = magicTree.predict(testdata)

    print(len(extractor.readFile()))


if __name__ == "__main__":
    main()


