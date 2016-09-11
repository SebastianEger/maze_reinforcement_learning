class Test:
    _modul = 5

    def __init__(self):
        self.mod = 5

    def setModul(self, a):
        self._modul = a

    def getModul(self):
        return self._modul



test1 = Test()
test2 = Test()
test3 = Test()

test3.setModul(113)

print test1.getModul(), test2.getModul(), test3.getModul()
