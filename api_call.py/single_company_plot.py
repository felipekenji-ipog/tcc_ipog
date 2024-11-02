import json
import matplotlib.pyplot as plt
from enums import FileClass, ColClass

# Nome da empresa analisada
company = 'HP'

# Nomes das métricas a serem analisadas
metrics = [
    ColClass.CAPITAL_DE_GIRO,
    ColClass.DIVIDA_PARA_PATRIMONIO,
    ColClass.FLUXO_DE_CAIXA_LIVRE_POR_ACAO,
    ColClass.RECEITA_POR_ACAO,
    ColClass.ROIC,
    ColClass.VALOR_DA_EMPRESA,
    ColClass.VALOR_DE_MERCADO
]

# Dicionário para mapear valores das métricas aos nomes das variáveis em ColClass
metric_names = {v: k for k, v in ColClass.__dict__.items() if not k.startswith('__')}

# Função para obter o título a partir do valor da métrica
def get_metric_title(metric_value):
    return metric_names.get(metric_value, metric_value)

# Nomes para montagem do gráfico
economic_indicator_plotname = FileClass.pib.plotname

# Ajustando nome do indicador macroeconômico para identificar pasta para salvar
ei_foldername = economic_indicator_plotname.replace("ç", "c").replace("ã","a").lower()

# Nomes dos arquivos JSON
company_data_filename = FileClass.metricas_chaves.filename
economic_data_filename = FileClass.pib.filename

# Função para ler o arquivo JSON e extrair múltiplas métricas para uma única empresa
def extract_company_performance_measures(filename, company, metrics):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    if company not in data:
        print(f"Empresa {company} não encontrada nos dados.")
        return {}

    # Armazenar dados das métricas por ano para a empresa especificada
    company_ratios = {}
    for record in data[company]:
        year = record['calendarYear']
        company_ratios[year] = {metric: record.get(metric, None) for metric in metrics}
    return company_ratios

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

# Obter dados
company_performance_measures = extract_company_performance_measures(company_data_filename, company, metrics)
economic_indicators = extract_economic_indicators(economic_data_filename)

# Criar gráficos para cada métrica selecionada
for metric in metrics:
    metric_name = get_metric_title(metric)  # Obter o nome da variável para o título do gráfico

    # Filtrar anos comuns entre as métricas e os indicadores econômicos
    common_years = sorted(set(company_performance_measures.keys()).intersection(set(economic_indicators.keys())))
    company_values = [company_performance_measures[year][metric] for year in common_years if company_performance_measures[year][metric] is not None]
    inflation_values = [economic_indicators[year] for year in common_years]

    if len(company_values) > 1 and len(inflation_values) > 1:
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Eixo Y para a métrica específica
        ax1.set_xlabel('Ano')
        ax1.set_ylabel(f'{metric_name} ({company})', color='blue')
        ax1.plot(common_years, company_values, marker='o', label=metric_name, color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Segundo eixo Y para o indicador econômico
        ax2 = ax1.twinx()
        ax2.set_ylabel(f'{economic_indicator_plotname}', color='red')
        ax2.plot(common_years, inflation_values, marker='o', label=economic_indicator_plotname, color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Configurações do gráfico
        plt.title(f'{company}: {metric_name} x {economic_indicator_plotname}')
        plt.xticks(common_years)
        ax1.grid()
        
        # Adicionar legendas
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Salvar o gráfico como arquivo ou exibi-lo
        metric_plotname_file = metric_name.replace(" ", "").lower()
        ei_plotname_file = economic_indicator_plotname.strip("[]").replace(" ", "").lower()
        plt.savefig(f'img_{ei_foldername}/{company}__{metric_plotname_file}__{ei_plotname_file}.png')  # Salvar como PNG
        plt.show()  # Exibir o gráfico
    else:
        print(f"Dados insuficientes para a métrica {metric_name} da empresa {company}.")
