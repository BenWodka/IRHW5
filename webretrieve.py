import resource
import sys
import time
import spacy
import json
from tokenizer import processQuery

MAP_RECORD_SIZE = 30
POST_RECORD_SIZE = 24
DICT_RECORD_SIZE = 59
nlp = spacy.blank("en")

def main(command, queryTerms, lineCountDict):
    if command == 'retrieve':
        lineCountDict = int(lineCountDict)
        queryTermsStr = ' '.join(queryTerms)
        filteredQueryTerms = processQuery(queryTermsStr, nlp)
        numDocs = 0
        accumulator = {}

        with open('outfiles/dict.txt', 'r') as dictfile:
            for filteredQueryTerm in filteredQueryTerms:
                index = computeIndex(filteredQueryTerm, lineCountDict)
                found = False
                originalIndex = index
                while True:
                    dictRecord = readDictRecord(dictfile, DICT_RECORD_SIZE, index)
                    dictTerm, numDocsInDict, startPosition = dictRecord
                    if dictTerm == filteredQueryTerm:
                        found = True
                        break
                    else:
                        index = (index + 1) % lineCountDict
                        if index == originalIndex:
                            break
                if not found:
                    print(f"Term '{filteredQueryTerm}' not found in dictionary.")
                    continue

                numDocs += numDocsInDict

                with open('outfiles/post.txt', 'r') as postfile:
                    for i in range(numDocsInDict):
                        postRecord = readPostRecord(postfile, POST_RECORD_SIZE, startPosition + i)
                        print(postRecord)
                        docId, weight = postRecord

                        # Update the accumulator
                        if docId in accumulator:
                            accumulator[docId] += weight
                        else:
                            accumulator[docId] = weight

        results = accumulator.items()
        print(results)
        sortedResults = sorted(results, key=lambda x: x[1], reverse=True)
        print(sortedResults)
        topResults = sortedResults[:10]

        with open('outfiles/map.txt', 'r') as mapfile:
            mapDict = {}
            for line in mapfile:
                docIdStr = line[:4].strip()
                filename = line[5:].strip()
                if docIdStr.isdigit():
                    docId = int(docIdStr)
                    mapDict[docId] = filename


        BASE_URL = "https://csce.uark.edu/~bmw032/HW5/smallfiles/"
        # Display the top 10 results
        outputResults = []
        #print("Top 10 results:")
        for result in topResults:
            print(f'result[0]:{result[0]}')
            doc_id = result[0]
            total_weight = result[1]
            filename = mapDict.get(doc_id)
            file_url = f"{BASE_URL}{filename}"
            #print(file_url)
            outputResults.append({
            "doc_id": doc_id,
            "url": file_url,
            "total_weight": total_weight
            })
            #print(f"DocID: {docId}, Filename: {filename}, Total Weight: {totalWeight}")

def readDictRecord(file, recordSize, recordNum):
    position = recordNum * recordSize
    file.seek(position)
    record = file.read(recordSize)
    term = record[:45].strip()
    numDocsStr = record[46:50].strip()
    startStr = record[51:].strip()
    numDocs = int(numDocsStr) if numDocsStr.isdigit() else 0
    start = int(startStr) if startStr.isdigit() else 0
    return (term, numDocs, start)

def readPostRecord(file, recordSize, recordNum):
    position = recordNum * recordSize
    file.seek(position)
    record = file.read(recordSize)
    docIdStr = record[:4].strip()
    weightStr = record[5:].strip()
    docId = int(docIdStr) if docIdStr.isdigit() else 0
    weight = float(weightStr) if weightStr.replace('.', '', 1).isdigit() else 0.0
    return (docId, weight)

def computeIndex(key, tableSize):
    sum = 0
    for char in key:
        sum = (sum * 19) + ord(char)
    index = sum % tableSize
    return index

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: ./retrieve.sh retrieve term1 term2 term3\n")
        print("i.e: ./retrieve.sh retrieve the dog jumped\n")
        sys.exit(1)

    command = sys.argv[1]
    queryTerms = sys.argv[2:-1]
    lineCountDict = sys.argv[-1]  # wc -l on file to get lines

    startRealTime = time.time()  # Real time
    startUserTime = resource.getrusage(resource.RUSAGE_SELF).ru_utime  # User time

    # Call main with given arguments
    main(command, queryTerms, lineCountDict)

    # End time measurement
    endRealTime = time.time()
    endUserTime = resource.getrusage(resource.RUSAGE_SELF).ru_utime

    elapsedRealTime = endRealTime - startRealTime
    elapsedUserTime = endUserTime - startUserTime

    # print(f"Real time: {elapsedRealTime:.2f} seconds")
    # print(f"User time (CPU): {elapsedUserTime:.2f} seconds")
