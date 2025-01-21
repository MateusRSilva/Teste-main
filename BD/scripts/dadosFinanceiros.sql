CREATE TABLE dados_financeiros (
    data DATE NOT NULL,
    reg_ans INT NOT NULL,
    cd_conta_contabil VARCHAR(255) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    vl_saldo_inicial VARCHAR(255),
    vl_saldo_final VARCHAR(255),
    
    -- Definição da chave primária composta
    PRIMARY KEY (data, reg_ans, cd_conta_contabil)
);