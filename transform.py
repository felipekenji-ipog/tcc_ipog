import json
import numpy as np

from enums import IndicatorClass

# Nome da coluna do indicador analisado
company_measure_colname = IndicatorClass.growthGrossProfitRatio.colname

# Nomes para a montagem do gráfico
company_measure_plotname = IndicatorClass.growthGrossProfitRatio.plotname.strip("[]").lower()
economic_indicator_plotname = IndicatorClass.inflation.plotname.strip("[]").lower()

# Nomes dos arquivos JSON
company_data_filename = IndicatorClass.growthGrossProfitRatio.filename
economic_data_filename = IndicatorClass.inflation.filename

# Função para ler o arquivo JSON e extrair grossProfitRatio para todas as empresas
def extract_company_performance_measures(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    ratios = {}
    for company, records in data.items():
        ratios[company] = {}
        for record in records:
            year = record['calendarYear']
            gross_profit_ratio = record['growthGrossProfitRatio']
            ratios[company][year] = gross_profit_ratio  # Armazenar o ratio por ano
    return ratios

# Função para ler o arquivo JSON de inflação
def extract_economic_indicators(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    inflation = {}
    for entry in data['data']:
        year = entry['date'][:4]  # Obter o ano da data
        value = float(entry['value'])  # Converter o valor para float
        inflation[year] = value  # Armazenar a inflação por ano
    return inflation

# Chamar as funções para obter os dados
company_performance_measures = extract_company_performance_measures(company_data_filename)
economic_indicators = extract_economic_indicators(economic_data_filename)

# Filtrar anos que aparecem em ambos os conjuntos de dados
common_years = sorted(set().union(*(set(ratios.keys()) for ratios in company_performance_measures.values())).intersection(set(economic_indicators.keys())))

# Listas para armazenar empresas
directly_proportional_companies = []
inversely_proportional_companies = []

# Verificação das variações
for company, ratios in company_performance_measures.items():
    # Filtrar apenas os anos comuns
    company_performance_measures_values = [ratios[year] for year in common_years if year in ratios]
    inflation_values = [economic_indicators[year] for year in common_years if year in economic_indicators]

    # Verificar se a variação é semelhante ou inversa
    if len(company_performance_measures_values) > 1 and len(inflation_values) > 1:
        # Comparar a variação em relação ao ano anterior
        company_performance_measures_trend = np.sign(np.diff(company_performance_measures_values))  # 1 para aumento, -1 para diminuição
        inflation_trend = np.sign(np.diff(inflation_values))  # O mesmo para inflação

        # Verificar se a tendência é semelhante ou inversa
        if np.array_equal(company_performance_measures_trend, inflation_trend):
            directly_proportional_companies.append(company)
        elif np.array_equal(company_performance_measures_trend, -inflation_trend):
            inversely_proportional_companies.append(company)

# Imprimir os resultados
print(f"Empresas com variação de {company_measure_plotname}")
print(f"- Diretamente proporcional à {economic_indicator_plotname}:", directly_proportional_companies)
print(f"- Inversamente proporcional à {economic_indicator_plotname}:", inversely_proportional_companies)
