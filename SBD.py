from sklearn.tree import DecisionTreeClassifier

class FeatExt:
    def __init__(self, name):
        self.__fileName = name
        self.__featVectors = []
        self.__featLabels = []

    @staticmethod
    def __analyzeRL(vectorRL):
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

        #The modulo is important, my first attempt was generating numbers that exceeded the 32 bit limit. lol.
        vector[0] = hash(vector[0]) % (2 ** 31)
        vector[1] = hash(vector[1]) % (2 ** 31)
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

    def readFile(self):
        with open(self.__fileName, 'r') as file:
            prevLine = ""
            check = False
            # checking to see if TOK line may have word after period in it.
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
                    self.__featVectors.append(self.__analyzeRL(self.__extractRL(prevLine, line)))
                    self.__featLabels.append(self.__outcome(prevLine))
                    check = False
                if '.' in line and "TOK" not in line:
                    prevLine = line
                    check = True

        return self.__featVectors, self.__featLabels

class AccCalc:
    def __init__(self, pred, ans):
        self.__predictions = pred
        self.__answers = ans

    def getAccuracy(self):
        correct = 0
        wrong = 0;

        for i, num in enumerate(self.__predictions):
            if str(num).isdigit() and num == self.__answers[i]:
                correct += 1
            else:
                wrong += 1

        return format((correct / (correct+wrong)) * 100 , '.2f')

def main():
    extractorTrain = FeatExt("SBD.train")
    extractorTest = FeatExt("SBD.test")
    #Extract vectors and labels from training data
    featureVectorsTrain, featureLabelsTrain = extractorTrain.readFile()
    #Extract vectors and labels from testing data
    featureVectorsTest, featureLabelsTest = extractorTest.readFile()
    magicTree = DecisionTreeClassifier()
    #Train the tree with feat. vectors from train and the known good labels.
    magicTree.fit(featureVectorsTrain, featureLabelsTrain)
    prediction = magicTree.predict(featureVectorsTest).tolist()
    #Compare our predicted labels with the actual labels from test.
    acc = AccCalc(prediction, featureLabelsTest)
    print(acc.getAccuracy() + "% correct")

    #Stuff that will be removed before submission
    with open('Predict.answers', 'w') as out:
        for i in prediction:
            out.write(str(i) + "\n")

    with open('Real.Answers', 'w') as out:
        for label in featureLabelsTest:
            out.write(str(label) + "\n")

    with open('SBD.answers', 'w') as out:
        vectorStr = ""
        for sets in featureVectorsTest:
            for var in sets:
                vectorStr += str(var) + "; "
            vectorStr = vectorStr + "\n"

        out.write(vectorStr)


if __name__ == "__main__":
    main()


