import requests
from bs4 import BeautifulSoup
import os
import zipfile
import logging
from pathlib import Path

# Configuração do logging para monitorar o progresso e erros
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Configuração de diretórios
BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "anexos"
ZIP_FILE_PATH = BASE_DIR / "anexos.zip"

# URL do site alvo
TARGET_URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

def create_directory(directory: Path):
    """Cria o diretório para downloads, se ainda não existir."""
    if not directory.exists():
        directory.mkdir(parents=True)
        logging.info(f"Diretório criado: {directory}")

def fetch_page_content(url: str) -> str:
    """Faz o download do conteúdo HTML da página."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("Página carregada com sucesso.")
        return response.text
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar a página: {e}")
        raise

def extract_pdf_links(html_content: str) -> dict:
    """Extrai os links dos PDFs de interesse."""
    soup = BeautifulSoup(html_content, "html.parser")
    pdf_links = {}
    for link in soup.find_all("a", href=True):
        href = link["href"]
        text = link.get_text().strip()
        if ("Anexo I" in text or "Anexo II" in text) and href.endswith(".pdf"):
            pdf_name = href.split("/")[-1]
            pdf_links[pdf_name] = href if href.startswith("http") else f"https://www.gov.br{href}"
    if not pdf_links:
        logging.warning("Nenhum PDF correspondente foi encontrado.")
    return pdf_links

def download_file(file_url: str, output_path: Path, new_name: str = None):
    """Baixa um arquivo PDF para o diretório especificado e renomeia, se necessário."""
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        temp_path = output_path
        if new_name:
            temp_path = output_path.with_name(new_name)
        
        with open(temp_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        logging.info(f"Arquivo baixado: {temp_path}")
        return temp_path
    except requests.RequestException as e:
        logging.error(f"Erro ao baixar o arquivo {file_url}: {e}")
        raise

def compress_files(files: list, zip_path: Path):
    """Compacta uma lista de arquivos em um arquivo ZIP."""
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file, arcname=file.name)
        logging.info(f"Arquivos compactados em: {zip_path}")
    except Exception as e:
        logging.error(f"Erro ao compactar os arquivos: {e}")
        raise

def main():
    logging.info("Iniciando o processo de web scraping e compactação.")

    # Preparação
    create_directory(DOWNLOAD_DIR)

    # Etapas do processo
    try:
        # 1. Obter o HTML da página
        html_content = fetch_page_content(TARGET_URL)

        # 2. Encontrar links para PDFs
        pdf_links = extract_pdf_links(html_content)
        if not pdf_links:
            logging.error("Nenhum link para PDF encontrado. Finalizando execução.")
            return

        # 3. Baixar os PDFs e renomeá-los
        downloaded_files = []
        for index, (pdf_name, pdf_url) in enumerate(pdf_links.items(), 1):
            new_name = f"Anexo_{index}.pdf"  # Definir o nome conforme o índice
            file_path = DOWNLOAD_DIR / pdf_name
            renamed_file = download_file(pdf_url, file_path, new_name)
            downloaded_files.append(renamed_file)

        # 4. Compactar os arquivos em um ZIP
        compress_files(downloaded_files, ZIP_FILE_PATH)

        logging.info("Processo concluído com sucesso.")
    except Exception as e:
        logging.error(f"Erro durante o processo: {e}")

if __name__ == "__main__":
    main()
