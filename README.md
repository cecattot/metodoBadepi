1º extrair os dados 
[https://inpidrive.inpi.gov.br/index.php/s/pTASUok7glOjSeO](url)
(Talvez a forma mais fácil seja criando um BD com os dados dos arquivos, a estrutura do BD utilizado pode ser consulta em base.sql)

2º limitar os dados e exportá-los em csv, mantendo o número do processo na coluna "NO_PROCESS"
    Ex.: select * from badepiv10_mrc_deposito 
        inner join badepiv10_mrc_depositante ON badepiv10_mrc_depositante.NO_PROCESS = badepiv10_mrc_deposito.NO_PROCESS 
        inner join badepiv10_mrc_classe ON badepiv10_mrc_classe.NO_PROCESS = badepiv10_mrc_deposito.NO_PROCESS 
        inner join badepiv10_mrc_despacho ON badepiv10_mrc_despacho.NO_PROCESS = badepiv10_mrc_deposito.NO_PROCESS 
        where 
            badepiv10_mrc_deposito.DS_NATUREZ_MARCA like "Marca Coletiva";

3º executar main.py para que clone as páginas de cada pedido depositado

4º executar analise.py para que gere o csv com os nomes das marcas consolidados

5º para verificar se houve alguma falha, executar verificacao

6º o arquivo todas_as_marcas consiste na extração de todos os processos, sem repetição da base.

7º o arquivo todas_as_marcas_com_despacho consiste na extração de todos os processos, com cada despacho vinculado.
