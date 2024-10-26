import asyncio
import aiohttp
import json
import ssl
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente a partir de um arquivo .env
load_dotenv()

# Configurações iniciais como a chave da API e arquivos de endpoints/symbols
API_KEY = os.getenv("FREE_STOCK_MARKET_API_KEY")
ENDPOINTS_FILE = Path("txt/endpoints.txt")  # Caminho para o arquivo que contém os endpoints
SYMBOLS_FILE = Path("txt/symbols.txt")  # Caminho para o arquivo que contém os símbolos
PERIOD = "annual"  # Período a ser utilizado na requisição
REQUEST_TIMEOUT = 30.0  # Timeout para a requisição HTTP
MAX_RETRIES = 1  # Número máximo de tentativas para uma requisição falha
DELAY_BETWEEN_REQUESTS = 1.0  # Intervalo entre tentativas de requisição

# Função para ler um arquivo .txt e retornar uma lista de strings (endpoints ou symbols)
def read_txt_file(file_path: Path) -> List[str]:
    with file_path.open() as f:
        return [line.strip() for line in f if line.strip()]

# Função para verificar se a resposta da API é válida
def is_valid_response(data: Any) -> bool:
    # Verifica se a resposta é uma lista e contém um dicionário com o campo "symbol"
    if isinstance(data, list):
        return len(data) > 0 and isinstance(data[0], dict) and "symbol" in data[0]
    # Verifica se a resposta é um dicionário contendo o campo "symbol"
    elif isinstance(data, dict):
        return "symbol" in data
    return False

# Função para buscar dados de um determinado endpoint e símbolo de forma assíncrona
async def fetch_data(
    session: aiohttp.ClientSession,
    endpoint: str,
    symbol: str,
    retries: int = 0
) -> Dict[str, Any]:
    # Monta a URL para a API
    url = f"https://financialmodelingprep.com/api/v3/{endpoint}/{symbol}"
    try:
        # Faz a requisição assíncrona à API
        async with session.get(
            url, params={"period": PERIOD, "apikey": API_KEY}, timeout=REQUEST_TIMEOUT
        ) as response:
            # Aguarda e converte a resposta para JSON
            data = await response.json()
            # Verifica se a resposta é válida
            if is_valid_response(data):
                return {symbol: data}
            # Tenta novamente se a resposta for inválida e o número de tentativas não tiver sido excedido
            if retries < MAX_RETRIES:
                await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
                return await fetch_data(session, endpoint, symbol, retries + 1)
            print(f"Resposta inválida para {endpoint}:{symbol}")
            return {}
    # Trata exceções e tenta novamente se houver erros de conexão
    except Exception as e:
        if retries < MAX_RETRIES:
            await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
            return await fetch_data(session, endpoint, symbol, retries + 1)
        print(f"Ocorreu um erro para {endpoint}:{symbol}: {type(e).__name__} - {e}")
        return {}

# Função para processar os símbolos de um determinado endpoint
async def process_symbols(
    endpoint: str, symbols: List[str]
) -> Dict[str, Any]:
    # Configura um contexto SSL personalizado para evitar verificação de certificados (não recomendado para produção)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Cria uma sessão HTTP assíncrona
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        # Cria tarefas assíncronas para buscar dados de cada símbolo
        tasks = [fetch_data(session, endpoint, symbol) for symbol in symbols]
        # Aguarda a conclusão de todas as tarefas
        results = await asyncio.gather(*tasks)
        # Filtra e retorna os dados válidos
        return {symbol: data for result in results for symbol, data in result.items() if data}

# Função principal para processar os endpoints e símbolos
async def main():
    # Verifica se a chave da API foi carregada corretamente
    if not API_KEY:
        raise ValueError("API_KEY não encontrada nas variáveis de ambiente")

    # Lê os arquivos de endpoints e símbolos
    endpoints = read_txt_file(ENDPOINTS_FILE)
    symbols = read_txt_file(SYMBOLS_FILE)

    print(f"Processando {len(symbols)} símbolos em {len(endpoints)} endpoints.")

    # Itera sobre cada endpoint e processa seus respectivos símbolos
    for endpoint in endpoints:
        consolidated_data = await process_symbols(endpoint, symbols)

        # Salva os dados consolidados em arquivos JSON
        OUTPUT_FILE = Path(f"json/{endpoint}.json")
        with OUTPUT_FILE.open("w") as f:
            json.dump(consolidated_data, f, indent=4)

        print(f"Dados do endpoint {endpoint} salvos em {OUTPUT_FILE}")
        print(f"Dados consolidados salvos em {OUTPUT_FILE}")
        print(
            f"Processados com sucesso {len(consolidated_data)} de {len(symbols)} símbolos para o endpoint {endpoint}."
        )

# Executa a função principal assíncrona
if __name__ == "__main__":
    asyncio.run(main())