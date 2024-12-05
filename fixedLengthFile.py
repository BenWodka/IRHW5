class fixedLengthFile:
    def __init__(self, filename, recordSize):
        self.filename = filename
        self.recordSize = recordSize
        self.numRecords = -1
        self.file = None

    def openForWrite(self):
        try:
            self.file = open(self.filename, 'w')
            self.numRecords = 0
            return True
        except IOError:
            return False

    def openForRead(self, numRecords):
        try:
            self.file = open(self.filename, 'r')
            self.numRecords = numRecords
            return True
        except IOError:
            return False

    def closeAfterWriting(self):
        if self.file:
            self.file.close()
        num = self.numRecords
        self.numRecords = -1
        return num

    def closeAfterReading(self):
        if self.file:
            self.file.close()
        self.numRecords = -1

    def writeRecord(self, *args):
        return

    def readRecord(self, recordNum):
        if self.file and 0 <= recordNum < self.numRecords:
            position = recordNum * self.recordSize
            print(f"SEEKING TO POSITION: {position}")
            self.file.seek(position)
            record = self.file.read(self.recordSize)
            print(f"READING FROM FILE AT {self.file.tell()}: {record}")
            return record, True
        return None, False


class mapFile(fixedLengthFile):
    RECORD_SIZE = 30

    def __init__(self, filename):
        super().__init__(filename, self.RECORD_SIZE)

    def writeRecord(self, docId, filename):
        if self.file:
            record = f"{str(docId).rjust(4)} {filename[:30].ljust(30)}".ljust(self.RECORD_SIZE - 1) + "\n"
            self.file.write(record)
            self.numRecords += 1
            return True
        return False

    def readRecord(self, recordNum):
        if self.file and 0 <= recordNum < self.numRecords:
            position = recordNum * self.recordSize
            print(f"SEEKING TO POSITION: {position}")
            self.file.seek(position)
            record = self.file.read(self.recordSize)
            docId = record[:4].strip()
            filename = record[5:29].strip()
            print(f"MAP RECORD {recordNum}: {docId} {filename}")
            return (docId, filename), True
        return None, False


class postFile(fixedLengthFile):
    RECORD_SIZE = 24
    def __init__(self, filename):
        super().__init__(filename, self.RECORD_SIZE)

    def writeRecord(self, docId, weight):
        if self.file:
            record = f"{str(docId).rjust(4)} {str(weight).rjust(6)}".ljust(self.RECORD_SIZE - 1) + "\n"
            self.file.write(record)
            self.numRecords += 1
            return True
        return False

    def readRecord(self, recordNum):
        if self.file and 0 <= recordNum < self.numRecords:
            position = recordNum * self.RECORD_SIZE
            print(f"SEEKING TO POSITION: {position}")
            self.file.seek(position)
            record = self.file.read(self.RECORD_SIZE)
            docId = record[:4].strip()
            weight = record[5:].strip()
            print(f"POST RECORD {recordNum}: {docId} {weight}")
            return (docId, weight), True
        return None, False


class dictFile(fixedLengthFile):
    RECORD_SIZE = 59

    def __init__(self, filename):
        super().__init__(filename, self.RECORD_SIZE)

    def writeRecord(self, term, numDocs, start):
        if self.file:
            record = f"{term[:45].ljust(45)} {str(numDocs).rjust(4)} {str(start).rjust(7)}".ljust(self.RECORD_SIZE - 1) + "\n"
            self.file.write(record)
            self.numRecords += 1
            return True
        return False

    def readRecord(self, recordNum):
        if self.file and 0 <= recordNum < self.numRecords:
            position = recordNum * self.recordSize
            self.file.seek(position)
            record = self.file.read(self.RECORD_SIZE)
            term = record[:45].strip()
            numDocs = record[46:50].strip()
            start = record[51:].strip()
            print(f"DICT RECORD {recordNum}: {term} {numDocs} {start}")
            return (term, numDocs, start), True
        return None, False
