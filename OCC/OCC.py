from Transaction import Transaction
import time

class OCC:
    def __init__(self, fileName):
        data = open(fileName, "r").read()
        if(data[-1] == "\n"):
            data = data[:-1]
        self.arr = data.split(",")
        print(self.arr)
        if(not self.validateData(self.arr)):
            print("Invalid data")
            return
        self.transactions = []
        self.__initTransactions__(self.arr)
        

    def validateData(self, data)-> bool:
        for i in data :
            if(not (i[0]=="C" or i[0]=="R" or i[0]=="W")):
                print("Invalid operation data format: ", i)
                return False
            
            if(i[0] == "C"):
                if(len(i) != 2):
                    print("Invalid commit data format: ", i)
                    return False
                if(not i[1].isnumeric()):
                    print("Invalid commit data thread format: ", i)
                    return False
            else:
                if(len(i) != 3):
                    print("Invalid read/write data format: ", i)
                    return False
                if(not i[1].isnumeric()):
                    print("Invalid read/write data object format: ", i)
                    return False

            
        return True

    def __initTransactions__(self,arr):
        listOfThreads = []
        for i in arr:
            t = i[1]
            if(t not in listOfThreads):
                listOfThreads.append(t)
        
        for i in (listOfThreads):
            self.transactions.append(Transaction(int(i),None,None,None))
            print("input")
            
            
    def validateTransaction(self, tx):
        '''
        only if
        finishTS(Ti) < startTS(Tj)
        startTS(Tj) < finishTS(Ti) < validationTS(Tj) 
        and the set of data items written 
        by Ti does not intersect 
        with the set of data items read by Tj
        validation succeeds

        otherwise: validation fails and Tj aborted
. 
        '''
        for i in self.transactions:
            if(i.getId() == tx.getId()):
                continue
            
            if(i.getTS() == None):
                continue

            if(i.getEndTime() < tx.getStartTime()):
                continue
            
            if(i.getEndTime()>tx.getStartTime() and i.getStartTime()<tx.getTS()):
                for vari in i.write:
                    iter=0
                    borted = False
                    while(iter<len(tx.read) and not borted):
                        if(vari == tx.read[iter]):
                            borted = True
                        iter+=1
                    if(borted):
                        for j in range(iter, len(tx.read)):
                            tx.addAborted(tx.read[j])
                        print("Aborted variables: ", vari)
                        return False
                            
            else:
                for vari in tx.read:
                    tx.addAborted(vari)
                return False

        return True


    def OCC(self):
        for i in self.arr:
            if(i[0]=='R' or i[0]=='W'):
                idThread= int(i[1])
                print(self.transactions[idThread].getStartTime())
                if(self.transactions[idThread].getStartTime() == None):
                    time.sleep(0.1)
                    a = time.time()
                    self.transactions[idThread].setStartTime(a)
                    print("Thread ", idThread, "is starting")

                if(i[0]=='R'):
                    print("Thread ", idThread, "is reading ", i[2])
                    self.transactions[idThread].read.append(i[2])
                
                if(i[0]=='W'):
                    print("Thread ", idThread, "is writing ", i[2])
                    self.transactions[idThread].write.append(i[2])
                
            if(i[0]=='C'):
                print("Commiting thread ", i[1])
                time.sleep(0.1)
                self.transactions[int(i[1])].setTS(time.time())

                res = self.validateTransaction(self.transactions[int(i[1])])
                if(res):
                    print("Validation succeeded for thread ", i[1])
                    self.transactions[int(i[1])].setEndTime(time.time())
                else:
                    print("Validation failed for thread ", i[1])
                    print("Aborted variables: ", self.transactions[int(i[1])].listAborted)
    def printTransactions(self):
        for i in self.transactions:
            print(i)

namaFile = input()
occ = OCC(namaFile)
occ.OCC()    
occ.printTransactions()

                    