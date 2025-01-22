from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
from fuzzywuzzy import process
import unicodedata  # Para normalizar os textos

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas e origens

# Caminho do arquivo CSV
file_path = r'C:\Users\mattr\OneDrive\Documentos\workspace\Teste-main\TESTE DE API\backend\CSV\Relatorio_cadop.csv'

# Função para carregar o CSV com tratamento de erros e codificação UTF-8
def load_csv():
    try:
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8', on_bad_lines='skip')
        df = df.apply(lambda col: col.map(lambda x: None if pd.isna(x) else x))  # Corrige o erro de depreciação
        return df
    except pd.errors.ParserError as e:
        print(f"Erro ao tentar ler o arquivo CSV: {e}")
        return None
    except FileNotFoundError:
        print(f"O arquivo CSV não foi encontrado no caminho: {file_path}")
        return None

# Carrega os dados do CSV
df = load_csv()

if df is None:
    print("Não foi possível carregar os dados do CSV.")
else:
    print("CSV carregado com sucesso!")

# Função para normalizar o texto (remoção de acentos e conversão para minúsculas)
def normalize_text(text):
    text = str(text).lower()
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Função para realizar a busca com fuzzy matching
def fuzzy_search(df, search_term):
    search_term = normalize_text(search_term)  # Normaliza o termo de busca
    print(f"Buscando por: {search_term}")  # Debug: Exibe o termo de busca
    
    # Criar uma lista de todas as colunas combinadas em uma única lista para busca
    combined_columns = df.apply(lambda row: ' '.join(row.astype(str).fillna('')), axis=1).tolist()

    matches = []
    for i, text in enumerate(combined_columns):
        normalized_text = normalize_text(text)  # Normaliza o texto da linha
        best_match = process.extractOne(search_term, [normalized_text])
        
        #print(f"Comparando com: {normalized_text}")  # Debug: Exibe a comparação
        #print(f"Melhor match: {best_match}")  # Debug: Exibe o melhor match
        
        if best_match and best_match[1] >= 60:  # Define o limite de similaridade (pode ser ajustado)
            matches.append(df.iloc[i])

    return pd.DataFrame(matches)

# Função para converter o DataFrame para JSON e garantir que NaN seja convertido para null, além de adicionar IDs
def df_to_json(df):
    df['id'] = df.index
    return df.apply(lambda col: col.map(lambda x: None if pd.isna(x) else x)).to_dict(orient='records')

# Rota para a raiz
@app.route('/')
def home():
    return jsonify({"message": "Bem-vindo à API de busca! Use a rota /search/termo_para_busca para pesquisar."})

# Rota para buscar cadastros de operadoras
@app.route('/search/<search_term>', methods=['GET'])
def search(search_term):
    # Filtra os dados com base no termo de busca usando fuzzy search
    if df is not None:
        filtered_data = fuzzy_search(df, search_term)
        results = df_to_json(filtered_data)  # Converte para JSON com None no lugar de NaN
        return jsonify(results)
    else:
        return jsonify({"error": "Dados não carregados. Tente novamente mais tarde."}), 500

if __name__ == '__main__':
    app.run(debug=True)
