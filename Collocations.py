#mmm I love system libraries
import sys
import math

class Collocationator:
    def __init__(self, file):
        self._unigrams = self.__getUnigrams(file)
        self._bigrams = self.__getBigrams(file)
        self._unigramFreqs = self.__getUniFreqs()
        self._bigramFreqs = self.__getBiFreqs()

    def __getUniFreqs(self):
        uniDict = {}
        for word in self._unigrams:
            if word in uniDict:
                uniDict[word] += 1
            else:
                uniDict[word] = 1
        return uniDict

        # get number of occurrences of specific bigram

    def __getBiFreqs(self):
        biDict = {}
        for tup in self._bigrams:
            if tup in biDict:
                biDict[tup] += 1
            else:
                biDict[tup] = 1
        return biDict

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
                    unigrams.append(e.lower())

            return unigrams

    @staticmethod
    def __getBigrams(file):
        with open(file, 'r') as data:
            bigrams = []
            for line in data:
                elements = line.split()  # python moment
                for i in range(len(elements) - 1):
                    word = elements[i]
                    nextWord = elements[i + 1]
                    # filter out those pesky symbols
                    if (len(word) < 2 and not word.isalpha()) or (len(nextWord) < 2 and not nextWord.isalpha()):
                        continue

                    pair = (word.lower(), nextWord.lower())
                    bigrams.append(pair)
        return bigrams

class ChiSquare(Collocationator):
    def __init__(self, file):
        super().__init__(file)

    def print(self):
        output = self.__solve()
        for i, item in enumerate(output):
            if i >= 20:
                break
            print(str(item[0]) + " " + str(item[1]))

    def __solve(self):
        values = {}
        total_bigrams = sum(self._bigramFreqs.values())
        for gram, freq in self._bigramFreqs.items():
            expFreq = (self._unigramFreqs[gram[0]] * self._unigramFreqs[gram[1]])/len(self._bigrams)  # expected frequency
            obvFreq = freq
            #dividing bad 0 is bad
            if expFreq != 0:
                values[gram] = ((obvFreq - expFreq) ** 2)/expFreq
            else:
                values[gram] = 0

        return sorted(values.items(), key=lambda x: x[1], reverse=True)  # rewrite?


class PMI(Collocationator):
    def __init__(self, file):
        super().__init__(file)
        self.__pmiDict = {}
        self.__solve()

    def print(self):
        i = 0
        for k, v in self.__pmiDict.items():
            if i >= 20:
                break
            print(str(k) + " " + str(v))
            i += 1

    def __solve(self):
        for gram, freq in self._bigramFreqs.items():
            pGram = freq/len(self._bigrams)
            pW1 = self._unigramFreqs[gram[0]]/len(self._unigrams)
            pW2 = self._unigramFreqs[gram[1]]/len(self._unigrams)
            self.__pmiDict[gram] = math.log2((pGram/(pW1*pW2)))  # calculate the PMI
        self.__pmiDict = dict(sorted(self.__pmiDict.items(), key=lambda x: x[1], reverse=True))

def main():
    if len(sys.argv) < 2:
        print("Too few input arguments")
        return
    #What's better than functions? Classes!
    col = PMI(sys.argv[1])
    col.print()


if __name__ == "__main__":
    main()
