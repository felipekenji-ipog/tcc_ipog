import json
import numpy as np
import matplotlib.pyplot as plt
from enums import FileClass, ColClass

# Definindo o nome para o indicador econômico e ajustando para o nome da pasta
economic_indicator_plotname = FileClass.pib.plotname
ei_foldername = economic_indicator_plotname.replace("ç", "c").replace("ã", "a").lower()

# Nomes dos arquivos JSON
company_data_filename = FileClass.metricas_chaves.filename
economic_data_filename = FileClass.pib.filename

# Função para ler o arquivo JSON e extrair indicadores de desempenho para todas as empresas
def extract_company_performance_measures(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON de {filename}.")
        return {}

    ratios = {}
    # Iterando sobre cada empresa e seus registros
    for company, records in data.items():
        ratios[company] = {}
        for record in records:
            year = record['calendarYear']
            ratios[company][year] = {}

            # Itera sobre os atributos da ColClass, ignorando métodos especiais
            for indicator_name in dir(ColClass):
                if not indicator_name.startswith("__"):  # Ignora métodos especiais
                    column_name = getattr(ColClass, indicator_name)  # Obtém o nome da coluna

                    # Verifica se a coluna existe no registro
                    if column_name in record:
                        ratios[company][year][indicator_name] = record[column_name]

    return ratios

# Função para ler o arquivo JSON de inflação
def extract_economic_indicators(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON de {filename}.")
        return {}

    macro_kpi = {}
    # Extraindo dados de inflação
    for entry in data['data']:
        year = entry['date'][:4]
        value = float(entry['value'])
        macro_kpi[year] = value
    return macro_kpi

# Função para calcular o score de proporcionalidade
def calculate_proportionality_scores(company_performance_measures, economic_indicators, common_years):
    scores = {}
    # Iterando sobre cada empresa e seus indicadores
    for company, records in company_performance_measures.items():
        scores[company] = {}

        for indicator in records[next(iter(records))]:  # Pega a primeira empresa para obter os indicadores
            company_values = [records[year][indicator] for year in common_years if year in records]
            macro_kpi_values = [economic_indicators[year] for year in common_years if year in economic_indicators]

            # Verifica se há dados suficientes para calcular o score
            if len(company_values) > 1 and len(macro_kpi_values) > 1:
                company_trend = np.sign(np.diff(company_values))
                macro_kpi_trend = np.sign(np.diff(macro_kpi_values))

                # Atribui o score baseado na relação entre as tendências
                if np.array_equal(company_trend, macro_kpi_trend):
                    score = 1  # Diretamente proporcional
                elif np.array_equal(company_trend, -macro_kpi_trend):
                    score = -1  # Inversamente proporcional
                else:
                    score = 0  # Não proporcional

                scores[company][indicator] = score

    return scores

# Função para plotar os scores de proporcionalidade e salvar o gráfico final
def plot_proportionality_scores(scores):
    companies = list(scores.keys())
    indicators = list(scores[companies[0]].keys())

    # Dicionário para agregar os scores absolutos
    total_scores = {company: 0 for company in companies}
    indicator_names = ["Métricas Analisadas pelo Score:"]  # Lista para guardar todos os nomes de indicadores

    # Agregando scores absolutos e acumulando nomes dos indicadores
    for company in companies:
        for indicator in indicators:
            if indicator in scores[company]:
                total_scores[company] += abs(scores[company][indicator])
                if indicator not in indicator_names:
                    indicator_names.append(indicator)  # Adiciona o indicador único na lista de nomes

    # Filtra empresas com score total absoluto diferente de zero
    filtered_scores = {company: total_scores[company] for company in total_scores if total_scores[company] != 0}

    # Gráfico final de proporcionalidade total
    if filtered_scores:
        plt.figure(figsize=(10, 5))
        plt.bar(filtered_scores.keys(), filtered_scores.values(), color='lightgreen')
        plt.title('Proporcionalidade: Desempenho x PIB')
        plt.xlabel('Empresas')
        plt.ylabel('Score Total Absoluto')
        plt.axhline(0, color='red', linestyle='--')  # Linha de referência
        plt.xticks(rotation=45)
        max_score = max(filtered_scores.values())
        plt.yticks(np.arange(0, max_score + 1, 1))

        # Exibir os nomes dos indicadores como lista vertical no canto superior direito
        plt.gca().text(0.75, 0.95, "\n".join(indicator_names), fontsize=10, ha="left", va="top", 
                       bbox=dict(facecolor='white', edgecolor='black', alpha=0.7), transform=plt.gca().transAxes)

        # Salvando o gráfico final
        plt.savefig(f'img_{ei_foldername}/desempenho__{ei_foldername}.png')
        plt.close()
    else:
        print("Nenhuma empresa com score total absoluto diferente de zero.")

# Executando o fluxo principal
def main():
    # Obter os dados das empresas e indicadores econômicos
    company_performance_measures = extract_company_performance_measures(company_data_filename)
    economic_indicators = extract_economic_indicators(economic_data_filename)

    # Filtrar anos comuns
    common_years = sorted(set().union(*(set(ratios.keys()) for ratios in company_performance_measures.values())).intersection(set(economic_indicators.keys())))

    # Calcular scores de proporcionalidade
    proportionality_scores = calculate_proportionality_scores(company_performance_measures, economic_indicators, common_years)

    # Plotar os scores
    plot_proportionality_scores(proportionality_scores)

# Chama a função principal para iniciar o processo
if __name__ == "__main__":
    main()
