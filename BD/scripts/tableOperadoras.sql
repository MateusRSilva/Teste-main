-- MySQL & PostgreSQL
CREATE TABLE operadoras (
    registro_ANS INT PRIMARY KEY,
    cnpj VARCHAR(255) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(255),
    logradouro VARCHAR(255),
    numero VARCHAR(50),
    complemento VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255),
    uf VARCHAR(255),
    cep VARCHAR(255),
    ddd VARCHAR(255),
    telefone VARCHAR(255),
    fax VARCHAR(255),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(255),
    regiao_de_comercializacao VARCHAR(255),
    data_registro_ans DATE
);
