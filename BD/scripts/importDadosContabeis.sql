LOAD DATA INFILE 'C:\\Users\\mattr\\OneDrive\\Documentos\\workspace\\testes\\BD\\csvs\\1T2023.csv'
INTO TABLE dados_financeiros
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, reg_ans, cd_conta_contabil, descricao, @vl_saldo_inicial, @vl_saldo_final)

LOAD DATA INFILE 'C:\\Users\\mattr\\OneDrive\\Documentos\\workspace\\testes\\BD\\csvs\\2T2023.csv'
INTO TABLE dados_financeiros
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, reg_ans, cd_conta_contabil, descricao, @vl_saldo_inicial, @vl_saldo_final)

LOAD DATA INFILE 'C:\\Users\\mattr\\OneDrive\\Documentos\\workspace\\testes\\BD\\csvs\\3T2023.csv'
INTO TABLE dados_financeiros
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, reg_ans, cd_conta_contabil, descricao, @vl_saldo_inicial, @vl_saldo_final)

LOAD DATA INFILE 'C:\\Users\\mattr\\OneDrive\\Documentos\\workspace\\testes\\BD\\csvs\\4T2023.csv'
INTO TABLE dados_financeiros
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, reg_ans, cd_conta_contabil, descricao, @vl_saldo_inicial, @vl_saldo_final)
SET
    data = STR_TO_DATE(@data, '%d/%m/%Y'),
    vl_saldo_inicial = REPLACE(@vl_saldo_inicial, ',', '.'),
    vl_saldo_final = REPLACE(@vl_saldo_final, ',', '.');

LOAD DATA INFILE 'C:\\Users\\mattr\\OneDrive\\Documentos\\workspace\\testes\\BD\\csvs\\1T2024.csv'
INTO TABLE dados_financeiros
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, reg_ans, cd_conta_contabil, descricao, @vl_saldo_inicial, @vl_saldo_final)

LOAD DATA INFILE 'C:\\Users\\mattr\\OneDrive\\Documentos\\workspace\\testes\\BD\\csvs\\2T2024.csv'
INTO TABLE dados_financeiros
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, reg_ans, cd_conta_contabil, descricao, @vl_saldo_inicial, @vl_saldo_final)

LOAD DATA INFILE 'C:\\Users\\mattr\\OneDrive\\Documentos\\workspace\\testes\\BD\\csvs\\3T2024.csv'
INTO TABLE dados_financeiros
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, reg_ans, cd_conta_contabil, descricao, @vl_saldo_inicial, @vl_saldo_final)