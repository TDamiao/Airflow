SET @proximo_lote :=sinasc_controle('dw', 'dw_dados_sexo');

INSERT INTO dw_dados_sexo (SEXO, bairro_id, VALOR, DATA, lote)
SELECT sexo, bairro_id, valor, data, @proximo_lote FROM st_dados_sexo