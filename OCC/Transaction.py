class Transaction:
    ''''''
    def __init__(self, idx, ts_start, ts_val, ts_end):
        self.idx = idx
        self.ts_start = ts_start
        self.ts_val = ts_val
        self.ts_end = ts_end
        self.read = []
        self.write = []
        self.listAborted = []
    
    def getId(self):
        return self.idx

    def getTS(self):
        return self.ts_val
    
    def getStartTime(self):
        return self.ts_start
    
    def getEndTime(self):
        return self.ts_end

    def setTS(self, ts):
        self.ts_val = ts

    def setEndTime(self, ts):
        self.ts_end = ts
    
    def setStartTime(self, ts):
        self.ts_start = ts

    def __str__(self) -> str:
        ret = f"Transaction {self.idx}:\n"
        ret += f"Start: {self.ts_start}\n"
        ret += f"Validation: {self.ts_val}\n"
        ret += f"End: {self.ts_end}\n"
        ret += f"Read: {self.read}\n"
        ret += f"Write: {self.write}\n"
        return ret

    def addAborted(self, var):
        self.listAborted.append(var)