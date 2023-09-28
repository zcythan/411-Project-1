"""

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

"""