class IndClass:
    def __init__(self, filename, plotname):
        self.filename = filename
        self.plotname = plotname


class FileClass:
    metricas_chaves = IndClass("json/key-metrics.json", "Taxas de Desempenho")
    inflacao = IndClass("json/INFLATION.json", "Inflação")
    pib = IndClass("json/REAL_GDP.json", "PIB")
    
class ColClass:
    RECEITA_POR_ACAO = 'revenuePerShare'
    FLUXO_DE_CAIXA_LIVRE_POR_ACAO = 'freeCashFlowPerShare'
    VALOR_DA_EMPRESA = 'enterpriseValue'
    VALOR_DE_MERCADO = 'marketCap'
    DIVIDA_PARA_PATRIMONIO = 'debtToEquity'
    ROIC = 'roic'
    CAPITAL_DE_GIRO = 'workingCapital'
    # LUCRO_LIQUIDO_POR_ACAO = 'netIncomePerShare'
    # FLUXO_DE_CAIXA_OPERACIONAL_POR_ACAO = 'operatingCashFlowPerShare'
    # CAIXA_POR_ACAO = 'cashPerShare'
    # VALOR_CONTABIL_POR_ACAO = 'bookValuePerShare'
    # VALOR_CONTABIL_TANGIVEL_POR_ACAO = 'tangibleBookValuePerShare'
    # PATRIMONIO_LIQUIDO_POR_ACAO = 'shareholdersEquityPerShare'
    # DIVIDA_DE_JUROS_POR_ACAO = 'interestDebtPerShare'
    # INDICE_PRECO_LUCRO = 'peRatio'
    # INDICE_PRECO_VENDAS = 'priceToSalesRatio'
    # INDICE_POCF = 'pocfratio'
    # INDICE_PFCF = 'pfcfRatio'
    # INDICE_PB = 'pbRatio'
    # INDICE_PT_B = 'ptbRatio'
    # EV_PARA_VENDAS = 'evToSales'
    # VALOR_DA_EMPRESA_SOBRE_EBITDA = 'enterpriseValueOverEBITDA'
    # EV_PARA_FLUXO_DE_CAIXA_OPERACIONAL = 'evToOperatingCashFlow'
    # EV_PARA_FLUXO_DE_CAIXA_LIVRE = 'evToFreeCashFlow'
    # RENDIMENTO_DE_LUCROS = 'earningsYield'
    # RENDIMENTO_DE_FLUXO_DE_CAIXA_LIVRE = 'freeCashFlowYield'
    # DIVIDA_PARA_ATIVOS = 'debtToAssets'
    # DIVIDA_LIQUIDA_PARA_EBITDA = 'netDebtToEBITDA'
    # INDICE_ATUAL = 'currentRatio'
    # COVERTURA_DE_JUROS = 'interestCoverage'
    # QUALIDADE_DA_RECEITA = 'incomeQuality'
    # RENDIMENTO_DE_DIVIDENDOS = 'dividendYield'
    # INDICE_DE_DISTRIBUICAO = 'payoutRatio'
    # VENDAS_GERAIS_E_ADMINISTRATIVAS_PARA_RECEITA = 'salesGeneralAndAdministrativeToRevenue'
    # PESQUISA_E_DESENVOLVIMENTO_PARA_RECEITA = 'researchAndDdevelopementToRevenue'
    # INTANGIVEIS_PARA_ATIVOS_TOTAL = 'intangiblesToTotalAssets'
    # CAPEX_PARA_FLUXO_DE_CAIXA_OPERACIONAL = 'capexToOperatingCashFlow'
    # CAPEX_PARA_RECEITA = 'capexToRevenue'
    # CAPEX_PARA_DEPRECIACAO = 'capexToDepreciation'
    # COMPENSACAO_BASEADA_EM_ACOES_PARA_RECEITA = 'stockBasedCompensationToRevenue'
    # NUMERO_DE_GRAHAM = 'grahamNumber'
    # RENDIMENTO_SOBRE_ATIVOS_TANGIVEIS = 'returnOnTangibleAssets'
    # GRAHAM_NET_NET = 'grahamNetNet'
    # VALOR_DE_ATIVOS_TANGIVEIS = 'tangibleAssetValue'
    # VALOR_LIQUIDO_DE_ATIVOS_ATUAIS = 'netCurrentAssetValue'
    # CAPITAL_INVESTIDO = 'investedCapital'
    # MEDIA_DE_CONTAS_A_RECEBER = 'averageReceivables'
    # MEDIA_DE_CONTAS_A_PAGAR = 'averagePayables'
    # MEDIA_DE_ESTOQUE = 'averageInventory'
    # DIAS_DE_VENDAS_A_RECUPERAR = 'daysSalesOutstanding'
    # DIAS_DE_CONTAS_A_PAGAR = 'daysPayablesOutstanding'
    # DIAS_DE_ESTOQUE_EM_MAOS = 'daysOfInventoryOnHand'
    # ROTATIVIDADE_DE_CONTAS_A_RECEBER = 'receivablesTurnover'
    # ROTATIVIDADE_DE_CONTAS_A_PAGAR = 'payablesTurnover'
    # ROTATIVIDADE_DE_ESTOQUE = 'inventoryTurnover'
    # ROE = 'roe'
    # CAPEX_POR_ACAO = 'capexPerShare'