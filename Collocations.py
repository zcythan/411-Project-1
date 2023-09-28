#read the index and then the index off by one for bigrams
import sys

class Collocationator:
    def __init__(self, file):
        self._unigrams = self.__getUnigrams(file)
        self._bigrams = self.__getBigrams(file)
    @staticmethod
    def __getUnigrams(file):
        with open(file, 'r') as data:
            unigrams = []
            for line in data:
                elements = line.split()  # still a python moment
                size = len(unigrams)
                for e in elements:
                    if len(e) < 2 and not e.isalpha():  # no symbols allowed
                        continue
                    unigrams.append(e)

            return unigrams

    @staticmethod
    def __getBigrams(file):
        with open(file, 'r') as data:
            bigrams = []
            for line in data:
                elements = line.split()  # python moment
                for i in range(len(elements) - 1):  # Adjust loop range to avoid index out-of-range
                    word = elements[i]
                    nextWord = elements[i + 1]
                    # filter out those pesky symbols
                    if (len(word) < 2 and not word.isalpha()) or (len(nextWord) < 2 and not nextWord.isalpha()):
                        continue

                    pair = (word, nextWord)
                    bigrams.append(pair)
        return bigrams

class ChiSquare(Collocationator):
    def __init__(self, file):
        super().__init__(file)
        self.__unigramFreqs = self.__initUniFreqs()
        self.__bigramFreqs = self.__initBiFreqs()

    def print(self):
        output = self.__solve()
        for i, item in enumerate(output):
            if i >= 20:
                break
            print(str(item[1]) + " " + str(format(item[0], '.5f')))

    def __solve(self):
        values = []
        for tup in self._bigrams:
            expFreq = (self.__unigramFreqs[tup[0]] * self.__unigramFreqs[tup[1]])/len(self._bigrams)
            obvFreq = self.__bigramFreqs[tup]
            values.append(((obvFreq - expFreq) ** 2)/expFreq)
        labelBigram = []
        for i in range(0, len(values)):
            labelBigram.append((values[i], self._bigrams[i]))
        return sorted(labelBigram, key=lambda x: x[0], reverse=True)

    #get number of occurrences of specific unigram
    def __initUniFreqs(self):
        uniDict = {}
        for word in self._unigrams:
            if word in uniDict:
                uniDict[word] += 1
            else:
                uniDict[word] = 1
        return uniDict

    #get number of occurrences of specific bigram
    def __initBiFreqs(self):
        biDict = {}
        for tup in self._bigrams:
            if tup in biDict:
                biDict[tup] += 1
            else:
                biDict[tup] = 1
        return biDict

def main():
    if len(sys.argv) < 2:
        print("Too few input arguments")
        return
    col = ChiSquare(sys.argv[1])
    #print("Unigrams: " + str(col._unigrams))
    #print("Bigrams: " + str(col._bigrams))
    col.print()


if __name__ == "__main__":
    main()
