
class FeatExt:
    def __init__(self, name):
        self.__fileName = name

    @staticmethod
    def __interpret(line):
        for i, char in enumerate(line):
            if char == '.' and (i + 1 < len(line)) and line[i+1] != " ":
                j = i
                val = ""
                #Builds left side of period
                while j >= 0:
                    if line[j] == " ":
                        break
                    val = line[j] + val
                    j -= 1
                #Builds right
                j = i+1
                while j < len(line):
                    if line[j] == " ":
                        return "Not Good: " + val
                    val = val + line[j]
                    j += 1
            elif char == '.' and (i + 1 < len(line)) and line[i+1] == " ":
                j = i
                val = ""
                while j >= 0:
                    if line[j] == " ":
                        return "Good: " + val
                    val = line[j] + val
                    j -= 1

        return "Rip: " + line

    def readFile(self):
        with open(self.__fileName, 'r') as file:
            with open('SBD.answers', 'w') as out:
                for line in file:
                    if '.' in line and "TOK" not in line:
                        out.write(self.__interpret(line) + '\n')

class AccCalc:
    def __init__(self):
        self.x = 0

def main():
    print("Hello world")
    extractor = FeatExt("SBD.train")
    extractor.readFile()


if __name__ == "__main__":
    main()


