#Inportações

import platform , os
import subprocess  

global lista_arquivos 

lista_arquivos={
        "users":"./arquivos/users.txt",
        "monitorados":"./arquivos/ips_monitorados.txt",
        "alertas":"./arquivos/ips_alertas.txt"}

#|=============================================================|#
#|                   FUNÇÕES DE ARQUIVOS                       |#
#|                                                             |#
#|=============================================================|#

def criar_arquivos():
    """
    Cria os arquivo que serão usado pelo programa.
    """
    for arquivo in lista_arquivos.values():
        if not os.path.exists(arquivo):
            arquivo = open(arquivo,'w')
            arquivo.close()
    

def get_dados_arquivo(tipo):
    """
    Retorna uma lista com os id's de chat de usuários cadastrados para receber alerta.
    """
    lista =[]
    with open(lista_arquivos[tipo], "r") as file:
        for linha in file.readlines():
            lista.append(linha.replace("\n",""))
    return lista


def salvar_usuario(user_chat_id):
    """
    salva um usuário para receber alertas
    """
    usuarios_atuais = get_dados_arquivo("users")
    if str(user_chat_id) not in usuarios_atuais:
        with open(lista_arquivos['users'], "a") as f:
            f.write(f"{user_chat_id}\n")
        return True
    else:
        return False


def deletar_usuario(user_chat_id):
    """
    Remove um id dos arquivo de usuários.
    Ao remover o usuário deixará de receber notificações. 
    """
    usuarios_atuais = get_dados_arquivo("users")
    if str(user_chat_id) in usuarios_atuais:
        with open(lista_arquivos['users'], "w") as f:
            for usuario in usuarios_atuais:
                if usuario != str(user_chat_id):
                    f.write(f"{usuario}\n")
        return True
    else:
        return False


def adicionar_ip_monitorado(ip_str):
    ips_monitorados = get_dados_arquivo("monitorados")
    if ip_str not in ips_monitorados:
        with open(lista_arquivos['users'], "a") as f:
            f.write(f"{ip_str}\n")
        return True
    else:
        return False


def salvar_ip_alerta(ip_lista_adicionar):
    """
    Recebe uma lista dos IP's offlines para alertar se voltaram
    """
    with open(lista_arquivos['alertas'], "a") as f:
        for ip in ip_lista_adicionar:
            f.write(f"{ip}\n")


def remover_ip_alerta(ip_lista_remover):
    """
    Recebe uma lista de IP's para remover da lista de alertas.
    """
    lista_ips_alertas = get_dados_arquivo("alertas") # IP's na lista atualmente
    with open(lista_arquivos['alertas'], "w") as f:
        for ip in lista_ips_alertas:
            if ip not in ip_lista_remover:
                #escreve o ip no arquivo se ele não estiver na lista de remoção
                f.write(f"{ip}\n")


#|=============================================================|#
#|                  FUNÇÕES DE TESTES DO IP'S                  |#
#|                                                             |#
#|=============================================================|#


def ip_is_alive(ip_str):
    """Testa se o IP está online.
    usa o protocolo ICMP, se ele não estiver habilitado sempre vai retornar False
    """
    parametro = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', parametro, '1', ip_str]
    teste_ip  = subprocess.call(command,stdout=subprocess.PIPE)
    if teste_ip == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    criar_arquivos()