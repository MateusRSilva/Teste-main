from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS  # Importa o CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas e origens

# Caminho do arquivo CSV
file_path = r'C:\Users\mattr\OneDrive\Documentos\workspace\Teste-main\TESTE DE API\backend\CSV\Relatorio_cadop.csv'

# Função para carregar o CSV com tratamento de erros e codificação UTF-8
def load_csv():
    try:
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8', on_bad_lines='skip')
        df = df.applymap(lambda x: None if pd.isna(x) else x)
        return df
    except pd.errors.ParserError as e:
        print(f"Erro ao tentar ler o arquivo CSV: {e}")
        try:
            df = pd.read_csv(file_path, delimiter=';', header=None, encoding='utf-8', on_bad_lines='skip')
            df = df.applymap(lambda x: None if pd.isna(x) else x)
            return df
        except Exception as e:
            print(f"Erro ao tentar ler o arquivo sem cabeçalho: {e}")
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

# Função para converter o DataFrame para JSON e garantir que NaN seja convertido para null, além de adicionar IDs
def df_to_json(df):
    df['id'] = df.index
    return df.applymap(lambda x: None if pd.isna(x) else x).to_dict(orient='records')

# Rota para a raiz
@app.route('/')
def home():
    return jsonify({"message": "Bem-vindo à API de busca! Use a rota /search?q=termo_para_busca para pesquisar."})

# Rota para buscar cadastros de operadoras
@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('q', '').lower()
    
    if not search_term:
        return jsonify({"error": "Parâmetro de busca 'q' é obrigatório."}), 400
    
    # Filtra os dados com base no termo de busca
    if df is not None:
        filtered_data = df[df.apply(lambda row: row.astype(str).str.contains(search_term).any(), axis=1)]
        results = df_to_json(filtered_data)  # Converte para JSON com None no lugar de NaN
        return jsonify(results)
    else:
        return jsonify({"error": "Dados não carregados. Tente novamente mais tarde."}), 500

if __name__ == '__main__':
    app.run(debug=True)
