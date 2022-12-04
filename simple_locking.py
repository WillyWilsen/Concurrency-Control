class SimpleLock:
    def __init__(self, jadwal : list):
        self.jadwal = jadwal
        self.dataItem = self.getAllItem()
        self.finalJadwal = self.getNewSchedule()

    #set status of item
    def getAllItem(self):
        dataItem = {}
        for item in self.jadwal:
            if item[0] != "C":
                dataItem[item[3]] = "Free" 
        return dataItem

    #generate locking schedule
    def getNewSchedule(self):
        jadwal = self.jadwal.copy()
        finalSchedule = []
        queue = []
        i = 0
        while i != len(jadwal):
            if jadwal[i][0] == "C":
                if self.checkQueue(jadwal[i][1], queue):
                    queue.append(jadwal[i])
                    jadwal.remove(jadwal[i])
                    i -= 1
                else:
                    finalSchedule.append(jadwal[i])
                    self.releaseLock(jadwal[i][1])
                    if len(queue) != 0:
                        newJadwal, newQueue = self.checkAvailable(jadwal, queue, i)
                        jadwal = newJadwal.copy()
                        queue = newQueue
            else:
                if self.checkQueue(jadwal[i][1], queue):
                    if self.checkUrutanJadwal(jadwal[i], queue):
                        finalSchedule.append("XL" + jadwal[i][1:])
                        finalSchedule.append(jadwal[i])
                        self.dataItem[jadwal[i][3]] = jadwal[i][1]
                    else:
                        queue.append(jadwal[i])
                        jadwal.remove(jadwal[i])
                        i -= 1
                elif self.dataItem.get(jadwal[i][3]) == "Free":
                    finalSchedule.append("XL" + jadwal[i][1:])
                    finalSchedule.append(jadwal[i])
                    self.dataItem[jadwal[i][3]] = jadwal[i][1]
                elif self.dataItem.get(jadwal[i][3]) == jadwal[i][1]:
                    finalSchedule.append(jadwal[i])
                else:
                    queue.append(jadwal[i])
                    jadwal.remove(jadwal[i])
                    i -= 1
            i += 1
        
        if len(queue) != 0:
            finalSchedule.append("deadlock")
        return finalSchedule

    # check if a transaction T is in queue
    def checkQueue(self, T, queue):
        for i in range(len(queue)):
            if queue[i][1] == T:
                return True
        return False

    #release all lock after commit
    def releaseLock(self, T):
        for item in self.dataItem.keys():
            if self.dataItem[item] == T:
                self.dataItem[item] = "Free"

    #check if item is available for operation in queue
    def checkAvailable(self, jadwal : list, queue : list, index):
        index += 1
        i = 0
        while i != len(queue):
            if queue[i][0] == "C":
                if not self.checkCommit(queue, queue[i][1]):
                    jadwal.insert(index, queue[i])
                    queue.remove(queue[i])
                    index += 1
                    i -= 1
                i += 1 
            else:
                if self.dataItem.get(queue[i][3]) == "Free" or self.dataItem.get(jadwal[i][3]) == queue[i][1]:
                    jadwal.insert(index, queue[i])
                    queue.remove(queue[i])
                    index += 1
                    i -= 1
                i += 1
        return jadwal, queue

    def checkCommit(self, queue : list, T):
        for item in queue:
            if item[0] != "C":
                if item[1] == T:
                    return True
        return False

    #periksa apakah ada operasi yang lebih dulu pada jadwal awal
    def checkUrutanJadwal(self, op, queue):
        for item in queue:
            if item[0] == "C":
                if item[1] == op[1]:
                    return self.checkDuluan(op, item)
            else:
                if item[1] == op[1]:
                    return self.checkDuluan(op, item)
        return False

    #cek apakah item1 lebih dulu dari item2
    def checkDuluan(self, item1, item2):
        return self.jadwal.index(item1) < self.jadwal.index(item2) 
                
    #cetak initial and final
    def printFinal(self):
        print("Initial Schedule = ", self.jadwal)
        print("Final Schedule = ", self.finalJadwal)

#test = SimpleLock(["R1(X)", "R2(X)", "C1", "R2(Y)", "C2"])
#test = SimpleLock(["R1(X)", "R2(Y)", "C1", "C2"])
#test = SimpleLock(["R1(A)", "W1(A)", "R2(A)", "W2(A)", "R1(B)", "W1(B)", "R2(B)", "W2(B)", "C1", "C2"])


#test = SimpleLock(["R1(X)", "R2(Y)", "R1(Y)", "W2(Y)", "W1(X)", "C1", "C2"])
#test.printFinal()
#test = SimpleLock(["R1(X)", "R2(Y)", "R1(Y)", "R2(X)", "C1", "C2"])
#test.printFinal()
#test = SimpleLock(["R1(X)", "W2(X)", "W2(Y)", "W3(Y)", "W1(X)", "C1", "C2", "C3"])
#test.printFinal()
#test = SimpleLock(["R1(X)", "R3(Y)", "R3(X)", "W3(Y)", "R2(Y)", "R1(Y)", "W3(X)", "R2(X)", "C1", "C2", "C3"])
#test.printFinal()
#test = SimpleLock(["R1(X)", "R2(Z)", "R3(X)", "R3(Y)", "W1(X)", "C1", "W3(Y)", "C3", "R2(Y)", "W2(Z)", "W2(Y)", "C2"])
#test.printFinal()
