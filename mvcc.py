class MVCC:
    def __init__(self, schedule: list):
        self.queue = list()
        self.eachTransaction = dict()
        self.eachTimestamp = dict()
        self.maxTimestamp = 0
        self.changedTimestamp = dict()
        self.generateQueue(schedule)
        self.printMVCC(schedule)

    def generateQueue(self, schedule: list):
        for i in range(len(schedule)):
            transaction_number = int(schedule[i][1])
            if (transaction_number in self.eachTransaction):
                self.eachTransaction[transaction_number].append([schedule[i], len(self.eachTransaction[transaction_number]) + 1])
            else:
                self.eachTransaction[transaction_number] = [[schedule[i], 1]]
                if (self.maxTimestamp < transaction_number):
                    self.maxTimestamp = transaction_number
            self.queue.append([schedule[i], len(self.eachTransaction[transaction_number])])
            if (schedule[i][0] != "C"):
                data = schedule[i][3]
                if (not(data in self.eachTimestamp)):
                    self.eachTimestamp[data] = [[0, 0, 0]]

    def read(self, data: str, read_time: int):
        idx = 0
        while (not(read_time in self.eachTransaction)):
            read_time = self.changedTimestamp[read_time]
        for i in range(len(self.eachTimestamp[data])):
            if (read_time > self.eachTimestamp[data][i][0] and read_time < self.eachTimestamp[data][i][1]):
                idx = i
        if (self.eachTimestamp[data][idx][0] < read_time):
            self.eachTimestamp[data][idx][0] = read_time
        print("TS(" + data + str(self.eachTimestamp[data][idx][2]) + ") = (" + str(self.eachTimestamp[data][idx][0]) + ", " + str(self.eachTimestamp[data][idx][1]) + ")")

    def write(self, data: str, write_time: int, transaction_id: int):
        is_abort = False
        first_write_time = write_time
        version = 0
        while (not(write_time in self.eachTransaction)):
            write_time = self.changedTimestamp[write_time]
        for i in range(len(self.eachTimestamp[data])):
            if (write_time < self.eachTimestamp[data][i][0]):
                is_abort = True
                version = self.eachTimestamp[data][i][2]
        if (not(is_abort)):
            self.eachTimestamp[data].append([write_time, write_time, first_write_time])
            print("TS(" + data + str(first_write_time) + ") = (" + str(write_time) + ", " + str(write_time) + ")")
        else:
            self.maxTimestamp += 1
            print("TS(T" + str(first_write_time) + ") < R-TS(" + data + str(version) + ") -> rollback")
            print("Ulang T" + str(first_write_time) + " dengan TS = " + str(self.maxTimestamp))
            self.changedTimestamp[write_time] = self.maxTimestamp
            self.eachTransaction[self.maxTimestamp] = self.eachTransaction[write_time]
            del self.eachTransaction[write_time]
            for j in range(len(self.eachTransaction[self.maxTimestamp])):
                if (self.eachTransaction[self.maxTimestamp][j][0][0] == "R"):
                    self.read(self.eachTransaction[self.maxTimestamp][j][0][3], int(self.eachTransaction[self.maxTimestamp][j][0][1]))
                elif (self.eachTransaction[self.maxTimestamp][j][0][0] == "W"):
                    self.write(self.eachTransaction[self.maxTimestamp][j][0][3], int(self.eachTransaction[self.maxTimestamp][j][0][1]), self.eachTransaction[self.maxTimestamp][j][1])
                if (transaction_id == self.eachTransaction[self.maxTimestamp][j][1]):
                    break

    def printMVCC(self, schedule: list):
        print("Schedule =", schedule)
        for i in range(len(self.queue)):
            if (self.queue[i][0][0] == "R"):
                print(self.queue[i][0], "->     ", end="")
                self.read(self.queue[i][0][3], int(self.queue[i][0][1]))
            elif (self.queue[i][0][0] == "W"):
                print(self.queue[i][0], "->     ", end="")
                self.write(self.queue[i][0][3], int(self.queue[i][0][1]), self.queue[i][1])

schedule = MVCC(["R1(A)", "R2(A)", "R3(B)", "R1(B)", "W3(C)", "W2(C)", "R1(C)", "C1", "R2(D)", "W3(B)", "C3", "W2(D)", "C2"])