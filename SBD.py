
class FeatExt:
    def __init__(self, name):
        self.__fileName = name

    @staticmethod
    def __interpret(line, nextLine):
        vector = ["null", "null", 0, 0, 0]
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
                for ch in nextLine:
                    if ch == " " and prevCh.isalpha():
                        vector[1] = val
                        break
                    if not ch.isalpha():
                        continue
                    val = val + nextLine[j]
                    j = j + 1
                    prevCh = ch

            #elif char == '.' and (i + 1 < len(line)) and line[i+1] == " ":
        if len(vector[0]) < 3:
            vector[2] = 1
        else:
            vector[2] = 0
        if vector[0] and vector[0][0].isupper():
            vector[3] = 1
        if vector[0] and vector[1][0].isupper():
            vector[4] = 1

        vectorStr = ""
        for i, var in enumerate(vector):
            if type(var) is int:
                vectorStr += str(var) + "; "
                continue
            vectorStr += var + "; "

        return vectorStr

    def readFile(self):
        with open(self.__fileName, 'r') as file:
            with open('SBD.answers', 'w') as out:
                prevLine = ""
                check = False
                for line in file:
                    if check:
                        out.write(self.__interpret(prevLine, line) + '\n')
                        check = False
                    if '.' in line and "TOK" not in line:
                        prevLine = line
                        check = True

class AccCalc:
    def __init__(self):
        self.x = 0

def main():
    print("Hello world")
    extractor = FeatExt("SBD.train")
    extractor.readFile()


if __name__ == "__main__":
    main()


