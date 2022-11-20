class SimpleLock:
    def __init__(self, jadwal : list):
        self.jadwal = jadwal
        self.operationList = {'R' : 'Read', 'W' : 'Write', 'C' : 'Commit'}
        self.dataItem = self.getAllItem()
        self.finalJadwal = self.getNewSchedule()

    def getAllItem(self):
        dataItem = {}
        for item in self.jadwal:
            if item[0] != "C":
                dataItem[item[3]] = "Free" 
        return dataItem

    def getNewSchedule(self):
        jadwal = self.jadwal
        finalSchedule = []
        queue = []
        i = 0
        while i != len(jadwal):
            if jadwal[i][0] == "C":
                finalSchedule.append(jadwal[i])
                self.releaseLock(jadwal[i][1])
                if len(queue) != 0:
                    newJadwal, newQueue = self.checkAvailable(jadwal, queue, i)
                    jadwal = newJadwal
                    queue = newQueue
            else:
                if self.dataItem.get(jadwal[i][3]) == "Free":
                    finalSchedule.append("XL" + jadwal[i][1:])
                    finalSchedule.append(jadwal[i])
                    self.dataItem[self.jadwal[i][3]] = self.jadwal[i][1]
                elif self.dataItem.get(jadwal[i][3]) == jadwal[i][1]:
                    finalSchedule.append(jadwal[i])
                else:
                    queue.append(jadwal[i])
                    jadwal.remove(jadwal[i])
                    i -= 1
            i += 1
        print(finalSchedule)
        return finalSchedule

    def releaseLock(self, T):
        for item in self.dataItem.keys():
            if self.dataItem[item] == T:
                self.dataItem[item] = "Free"

    def checkAvailable(self, jadwal : list, queue : list, index):
        index += 1
        for item in queue:
            if self.dataItem.get(item[3]) == "Free":
                jadwal.insert(index, item)
                queue.remove(item)
                index += 1
        return jadwal, queue


test = SimpleLock(["R1(X)", "R2(X)", "R3(X)", "C1", "C2", "C3"])