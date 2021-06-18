from dataclasses import dataclass
from copy import deepcopy

"""
## Reimplement this with a proper Factory next time
## This is a non architected "top-down solution"
"""

@dataclass
class ModelTV:
    sb: list
    ns: list
    os: list
    px: list

    @staticmethod
    def __simplify(x):
        try:
            return [i['node'] for i in x]
        except:
            return x

    def simplify(self):
        self.sb = self.__simplify(self.sb)
        self.ns = self.__simplify(self.ns)
        self.os = self.__simplify(self.os)
        self.px = self.__simplify(self.px)
        self.simple = sorted(list(set(self.sb + self.ns + self.os + self.px)))



@dataclass
class ModelLOA:
    cm: ModelTV
    pgm: ModelTV

    def simplify(self):
        #print("Simple HEAD")
        self.simple = []
        try:
            self.cm.simplify()
            self.simple += self.cm.simple
        except:
            pass
        try:
            self.pgm.simplify()
            self.simple += self.pgm.simple
        except:
            pass
        self.simple = sorted(list(set(self.simple)))


def simpleFactory(X):
    simpleX = deepcopy(X)
    if type(simpleX) != list:
        simpleX.simplify()
    else:
        simpleX = sorted(list(set([i['node'] for i in simpleX])))
    return simpleX