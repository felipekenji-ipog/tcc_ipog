import asyncio
import aiohttp
import json
import ssl
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ENDPOINTS_FILE = Path("txt/endpoints.txt")
REQUEST_TIMEOUT = 30.0
MAX_RETRIES = 1
DELAY_BETWEEN_REQUESTS = 1.0


def read_txt_file(file_path: Path) -> List[str]:
    with file_path.open() as f:
        return [line.strip() for line in f if line.strip()]


def is_valid_response(data: Any) -> bool:
    if isinstance(data, list):
        return len(data) > 0 and isinstance(data[0], dict)
    elif isinstance(data, dict):
        return True  # Assumindo que o dicionário é válido
    return False


async def fetch_data(
    session: aiohttp.ClientSession,
    endpoint: str,
    retries: int = 0
) -> Dict[str, Any]:
    url = f"https://www.alphavantage.co/query?"
    try:
        async with session.get(
            url, params={"function": endpoint, "apikey": API_KEY}, timeout=REQUEST_TIMEOUT
        ) as response:
            data = await response.json()
            if is_valid_response(data):
                return data  # Retorna os dados diretamente se for válido
            if retries < MAX_RETRIES:
                await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
                return await fetch_data(session, endpoint, retries + 1)
            print(f"Resposta inválida para {endpoint}")
            return {}
    except Exception as e:
        if retries < MAX_RETRIES:
            await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
            return await fetch_data(session, endpoint, retries + 1)
        print(f"Ocorreu um erro para {endpoint}: {type(e).__name__} - {e}")
        return {}


async def process_endpoint(endpoint: str) -> Dict[str, Any]:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        result = await fetch_data(session, endpoint)
        return result if result else {}


async def main():
    if not API_KEY:
        raise ValueError("API_KEY não encontrada nas variáveis de ambiente")

    endpoints = read_txt_file(ENDPOINTS_FILE)

    print(f"Processando {len(endpoints)} endpoints.")

    for endpoint in endpoints:
        consolidated_data = await process_endpoint(endpoint)

        OUTPUT_FILE = Path(f"json/{endpoint}.json")
        with OUTPUT_FILE.open("w") as f:
            json.dump(consolidated_data, f, indent=4)

        print(f"Dados do endpoint {endpoint} salvos em {OUTPUT_FILE}")
        print(f"Dados consolidados salvos em {OUTPUT_FILE}")
        print(f"Processados com sucesso os dados para o endpoint {endpoint}.")

if __name__ == "__main__":
    asyncio.run(main())