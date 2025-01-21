import pdfplumber
import pandas as pd
import zipfile
from pathlib import Path
import logging

# Configuração do logger para monitorar e registrar erros ou mensagens
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Caminhos dos arquivos
BASE_DIR = Path.cwd()  # Diretório atual, altere se necessário
PDF_FILE_PATH = BASE_DIR / "WEB SCRAPING" / "anexos" / "Anexo_1.pdf"
CSV_DIR = BASE_DIR / "anexosCSV"  # Diretório para o CSV
CSV_FILE_PATH = CSV_DIR / "rol_procedimentos.csv"
ZIP_FILE_PATH = BASE_DIR / "Teste_MateusReis.zip"  # Caminho do arquivo ZIP

# Função para extrair dados do PDF
def extract_data_from_pdf(pdf_path):
    """Extrai os dados da tabela e os rodapés de um arquivo PDF sem repetir o cabeçalho."""
    data = []
    footnotes = {}
    header = None  # Variável para armazenar o cabeçalho
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                table = page.extract_table()
                
                if table:
                    # Verificar se é a primeira página e capturar o cabeçalho
                    if i == 0:
                        header = table[0]  # Primeira linha é o cabeçalho
                        data.append(header)  # Adiciona o cabeçalho ao início
                    else:
                        # Adiciona os dados, ignorando o cabeçalho nas páginas subsequentes
                        data.extend(table[1:])  # Pula o cabeçalho

                # Captura o texto da página para procurar o rodapé
                page_text = page.extract_text()
                if page_text:
                    footer_text = extract_legend_from_footer(page_text)
                    if footer_text:
                        footnotes = extract_footnote_mapping(footer_text)

    except Exception as e:
        logging.error(f"Erro ao extrair dados do PDF: {e}")
    
    return data, footnotes

# Função para extrair a legenda do rodapé
def extract_legend_from_footer(page_text):
    """Extrai a legenda do rodapé do texto da página."""
    if "Legenda:" in page_text:
        start_index = page_text.find("Legenda:")  # Encontrar a posição da palavra 'Legenda:'
        return page_text[start_index:]  # Pega o texto após 'Legenda:'
    return None

# Função para extrair abreviações e seus significados a partir da legenda
def extract_footnote_mapping(footer_text):
    """Extrai abreviações e seus significados do rodapé do PDF."""
    footnote_mapping = {}
    footer_parts = footer_text.split("Legenda:")[1].strip()
    footnote_parts = footer_parts.split("\n")

    for part in footnote_parts:
        if ":" in part:
            abbreviation, meaning = part.split(":", 1)
            abbreviation = abbreviation.strip()
            meaning = meaning.strip()

            # Considerando apenas as abreviações 'OD' e 'AMB'
            if abbreviation == "OD":
                footnote_mapping[abbreviation] = "Seg. Odontológica"
            elif abbreviation == "AMB":
                footnote_mapping[abbreviation] = "Seg. Ambulatorial"
    
    return footnote_mapping

# Função para processar e salvar os dados em CSV
def save_data_to_csv(data, footnotes, csv_path):
    """Salva os dados extraídos do PDF em um arquivo CSV, aplicando as substituições de rodapé."""
    try:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(data[1:], columns=data[0])

        for abbreviation, meaning in footnotes.items():
            if abbreviation in df.columns:
                df.rename(columns={abbreviation: meaning}, inplace=True)

            for col in df.columns:
                df[col] = df[col].replace(abbreviation, meaning)
        
        df.to_csv(csv_path, index=False)
        logging.info(f"Dados salvos com sucesso em: {csv_path}")
    except Exception as e:
        logging.error(f"Erro ao salvar os dados no CSV: {e}")

# Função para compactar o arquivo CSV em um ZIP
def compress_csv_to_zip(csv_path, zip_path):
    """Compacta o arquivo CSV gerado em um arquivo ZIP."""
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, csv_path.name)
        logging.info(f"Arquivo ZIP gerado com sucesso em: {zip_path}")
    except Exception as e:
        logging.error(f"Erro ao compactar o CSV em ZIP: {e}")

# Função principal para executar o processo
def main():
    """Função principal para coordenar a extração e processamento dos dados."""
    logging.info("Iniciando o processo de extração de dados do PDF...")
    
    # Extraindo os dados do PDF e as informações do rodapé
    data, footnotes = extract_data_from_pdf(PDF_FILE_PATH)
    
    if data:
        # Salvando os dados extraídos no CSV
        save_data_to_csv(data, footnotes, CSV_FILE_PATH)
        
        # Compactando o CSV em um arquivo ZIP
        compress_csv_to_zip(CSV_FILE_PATH, ZIP_FILE_PATH)
        
        logging.info(f"Processo concluído. Arquivo compactado: {ZIP_FILE_PATH}")
    else:
        logging.warning("Nenhum dado foi extraído do PDF.")

if __name__ == "__main__":
    main()
