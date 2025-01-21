-- Para importar para a tabela operadoras
LOAD DATA INFILE 'C:\\Users\\mattr\\OneDrive\\Documentos\\workspace\\testes\\BD\\csvs\\Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(registro_ANS, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_de_comercializacao, data_registro_ans);
