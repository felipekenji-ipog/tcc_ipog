import json
import matplotlib.pyplot as plt
from enums import IndicatorClass

# Nome da coluna do indicador analisado
company_measure_colname = IndicatorClass.growthGrossProfitRatio.colname

# Nomes para a montagem do gráfico
company_measure_plotname = IndicatorClass.growthGrossProfitRatio.plotname
economic_indicator_plotname = IndicatorClass.inflation.plotname

# Nomes dos arquivos JSON
company_data_filename = IndicatorClass.growthGrossProfitRatio.filename
economic_data_filename = IndicatorClass.inflation.filename

# Listar as empresas para análise
companies = ['SAP', 'ADBE', 'QCOM', 'SQ', 'UBER']


# Função para ler o arquivo JSON e extrair o indicador de performance para todas as empresas
def extract_company_performance_measures(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    ratios = {}
    for company, records in data.items():
        ratios[company] = {}
        for record in records:
            year = record['calendarYear']
            company_performance_measure_value = record[f'{company_measure_colname}']
            ratios[company][year] = company_performance_measure_value  # Armazenar o valor do indicador de performance por ano
    return ratios

# Função para ler o arquivo JSON de {economic_indicator_plotname}
def extract_economic_indicators(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    economic_indicator_value = {}
    for entry in data['data']:
        year = entry['date'][:4]  # Obter o ano da data
        value = float(entry['value'])  # Converter o valor para float
        economic_indicator_value[year] = value  # Armazenar a {economic_indicator_plotname} por ano
    return economic_indicator_value

# Chamar as funções para obter os dados
company_performance_measures = extract_company_performance_measures(company_data_filename)
economic_indicators = extract_economic_indicators(economic_data_filename)

# Criar gráficos para as empresas selecionadas
for company in companies:
    if company in company_performance_measures:
        ratios = company_performance_measures[company]

        # Filtrar anos comuns
        common_years = sorted(set(ratios.keys()).intersection(set(economic_indicators.keys())))
        company_values = [ratios[year] for year in common_years]
        inflation_values = [economic_indicators[year] for year in common_years]

        # Criar gráfico para a empresa
        if len(company_values) > 1 and len(inflation_values) > 1:
            fig, ax1 = plt.subplots(figsize=(12, 6))

            # Eixo Y para o {company_measure_plotname}
            ax1.set_xlabel('Ano')
            ax1.set_ylabel(f'{company_measure_plotname} ({company})', color='blue')
            ax1.plot(common_years, company_values, marker='o', label=f'{company_measure_plotname}', color='blue')
            ax1.tick_params(axis='y', labelcolor='blue')

            # Criar um segundo eixo Y para a {economic_indicator_plotname}
            ax2 = ax1.twinx()
            ax2.set_ylabel(f'{economic_indicator_plotname} (%)', color='red')
            ax2.plot(common_years, inflation_values, marker='o', label=f'{economic_indicator_plotname}', color='red')
            ax2.tick_params(axis='y', labelcolor='red')

            # Configurações do gráfico
            plt.title(f'{company}: {company_measure_plotname} x {economic_indicator_plotname}')
            plt.xticks(common_years)  # Definir os anos como ticks no eixo x
            ax1.grid()
            
            # Adicionar legendas
            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')

            # Salvar o gráfico em um arquivo ou exibi-lo
            cm_plotname_file=company_measure_plotname.strip("[]").replace(" ","").lower()
            ei_plotname_file=economic_indicator_plotname.strip("[]").replace(" ","").lower()
            plt.savefig(f'{company}__{cm_plotname_file}__{ei_plotname_file}.png')  # Salvar como PNG
            plt.show()  # Exibir o gráfico
        else:
            print(f"Dados insuficientes para a empresa {company}.")
    else:
        print(f"Empresa {company} não encontrada nos dados.")
