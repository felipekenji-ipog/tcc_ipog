class IndClass:
    def __init__(self, filename, plotname, colname):
        self.filename = filename
        self.plotname = plotname
        self.colname = colname


class IndicatorClass:
    growthGrossProfitRatio = IndClass("json/income-statement-growth.json", "[Taxa de Crescimento do Lucro Bruto]", "growthGrossProfitRatio")
    inflation = IndClass("json/INFLATION.json", "[Inflação]", "")
    grossProfitGrowth = 