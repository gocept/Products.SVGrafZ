################################################################################
## 
## SVGrafZ: Base
## Version: $Id: base.py,v 1.1 2003/04/10 13:58:50 mac Exp $
##
################################################################################

from math import log10,floor,ceil
from types import *

class BaseGraph:
    """BaseClass for graphs providing base functionallity for all graphs."""

    __computed_results__ = None

    def hasLegend(self):
        "Has the graph a legend?"
        return (type(self.legend) == type([])) and self.legend


    def svgHeader(self):
        return """
        <svg xmlns="http://www.w3.org/2000/svg"
             xmlns:xlink="http://www.w3.org/1999/xlink"
             width="%i"
             height="%i">
             """ % (self.width, self.height)
        

    def svgFooter(self):
        return "</svg>"


    def minX(self):
        return self._computeMinMax('minX')

    def realMinX(self):
        return self._computeMinMax('realMinX')

    def minY(self):
        return self._computeMinMax('minY')

    def realMinY(self):
        return self._computeMinMax('realMinY')
        

    def maxX(self):
        return self._computeMinMax('maxX')

    def realMaxX(self):
        return self._computeMinMax('realMaxX')

    def maxY(self):
        return self._computeMinMax('maxY')

    def realMaxY(self):
        return self._computeMinMax('realMaxY')


    def countDistX(self):
        return self._computeMinMax('countDistX')

    def countDistY(self):
        return self._computeMinMax('countDistY')

    def numgraphs(self):
        return len(self.data)


    def _computeMinMax(self, key):
        if self.__computed_results__:
            return self.__computed_results__[key]

        self._testFormatOfData()
        self.__computed_results__ = {}
        cr = self.__computed_results__
        def compRoundedValMax(val):
            if val == 0:
                return 0
            valBase = 10 ** (int(log10(abs(val))))
            return valBase * ceil((float(val) / valBase)+1)

        def compRoundedValMin(val):
            if val == 0:
                return 0
            valBase = 10 ** (int(log10(abs(val))))
            return valBase * floor((float(val) / valBase)-1)

        def countDistinctValues(list):
            vals = 0
            while (len(list)):
                cval = list.pop()
                vals += 1
                try:
                    while 1:
                        list.pop(list.index(cval))
                except ValueError:
                    pass
            return vals

        allX = []
        allY = []
        for dataset in self.data:
            for value in dataset:
                allX.append(float(value[0]))
                allY.append(float(value[1]))

        cr['realMaxX'] = max(allX)
        cr['realMaxY'] = max(allY)
        cr['maxX']     = compRoundedValMax(cr['realMaxX'])
        cr['maxY']     = compRoundedValMax(cr['realMaxY'])

        cr['realMinX'] = min(allX)
        cr['realMinY'] = min(allY)
        cr['minX']     = compRoundedValMin(cr['realMinX'])
        cr['minY']     = compRoundedValMin(cr['realMinY'])

        cr['countDistX'] = countDistinctValues(allX)
        cr['countDistY'] = countDistinctValues(allY)
        
        return cr[key]


    def _testFormatOfData(self):
        if type(self.data) != ListType:
            raise RuntimeError, 'Data is not a list.'
        if len(self.data) == 0:
            raise RuntimeError, 'Data is empty.'
        i = 0
        for dataset in self.data:
            i = i + 1
            if type(dataset) != ListType:
                raise RuntimeError, 'Dataset %i is no List.' % i
            if len(dataset) == 0:
                raise RuntimeError, 'Dataset %i is empty.' % i

            j = 0
            for dataItem in dataset:
                j = j + 1
                if type(dataItem) != ListType:
                    raise RuntimeError, 'DataItem %i in Dataset %i is no List.'\
                          % (i,j)
                if len(dataItem) != 2:
                    raise RuntimeError,\
                          'DataItem %i in Dataset %i: More than 2 dimensions.'\
                          % (j,i)
                k = 0
                for dim in dataItem:
                    k = k + 1
                    if type(dim) not in [IntType,
                                         LongType,
                                         FloatType,
                                         StringType,
                                         UnicodeType,
                                         ]:
                        raise RuntimeError,\
                              'Dimension %i of DataItem %i in Dataset %i: \
                              Not allowed Type of %s.' \
                              % (k,j,i,type(dim))
        return 1        
