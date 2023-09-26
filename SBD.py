
class FeatExt:
    def __init__(self, name):
        self.__fileName = name

    def readFile(self):
        with open(self.__fileName, 'r') as file:
            for line in file:
                if '.' in line and "TOK" not in line:
                    print("Found a period in: ", line);

class AccCalc:
    def __init__(self):
        self.x = 0

def main():
    print("Hello world")
    extractor = FeatExt("SBD.train")
    extractor.readFile()


if __name__ == "__main__":
    main()


