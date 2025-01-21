SELECT 
    o.registro_ANS, 
    o.cnpj, 
    o.razao_social, 
    o.nome_fantasia, 
    o.modalidade, 
    o.logradouro, 
    o.numero, 
    o.complemento, 
    o.bairro, 
    o.cidade, 
    o.uf, 
    o.cep, 
    o.ddd, 
    o.telefone, 
    o.fax, 
    o.endereco_eletronico, 
    o.representante, 
    o.cargo_representante, 
    o.regiao_de_comercializacao, 
    o.data_registro_ans,
    df.total_despesas
FROM 
    operadoras o
JOIN 
    (SELECT 
        reg_ans, 
        SUM(CAST(vl_saldo_final AS DECIMAL(15,2))) AS total_despesas
    FROM 
        dados_financeiros
    WHERE 
        descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
        AND data >= CURRENT_DATE - INTERVAL 1 YEAR
    GROUP BY 
        reg_ans) df
ON o.registro_ANS = df.reg_ans
ORDER BY 
    df.total_despesas DESC
LIMIT 10;
