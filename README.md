# ip_telegram_bot

BOT para Telegram que faz verificação dos IP's que estão funcionando.

Usa o protocolo ICMP para isso.


## Dependências 


* [Python 3x](https://www.python.org/) 
* [pyTelegramBotAPI](https://pytba.readthedocs.io/en/latest/index.html)



## Arquivos
 * main.py
 * modulos.py



## Configurações Iniciais
1. ### Token
- O token de acesso ao seu bot deve ser inserido em um arquivo chamado *TOKEN*.
- Garanta que não tenha nenhum espaço extra além dos dados do token.


2. ### Pastas
- Uma pasta chamada *arquivos* será criada automaticamente na primeira execução script.
- Na pasta *arquivos* serão salvos as informações dos usuarios e ips monitorados


3. ### Arquivos
    - Serão criados na pasta *arquivos* automaticamente na primeira execução os arquivos *users.txt*, *ips_monitorados.txt* e *ips_alertas.txt*
        - **users.txt**: salva os ids de usuários que serão notifiocados
        - **ips_monitorados.txt**: ficarão os IP's monitorados cada IP deve ficar em uma linha
        - **ips_alertas.txt**: para uso futuro


## Sintaxe de Uso 
``` python3 main.py ```


## IMPORTANTE!!!

**ICMP** deve estar habilitado para que funcione, caso contrário sempre recebera um alerta de problema com o **IP**
