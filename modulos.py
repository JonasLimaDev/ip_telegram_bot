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
    if not os.path.exists("./arquivos"):
        os.system("mkdir ./arquivos")

    for arquivo in lista_arquivos.values():
        if not os.path.exists(arquivo):
            arquivo = open(arquivo,'w')
            arquivo.close()
        else:
            continue
    

def get_dados_arquivo(arquivo):
    """
    Retorna uma lista com os id's de chat de usuários cadastrados para receber alerta.
    """
    lista =[]
    with open(lista_arquivos[arquivo], "r") as file:
        for linha in file.readlines():
            lista.append(linha.replace("\n",""))
    return lista



def salvar_dados(arquivo,informacao):
    """
    Função genérica para salvar dados em arquivo.
    """
    dados_atuais = get_dados_arquivo(arquivo)
    if str(informacao) not in dados_atuais:
        with open(lista_arquivos[arquivo], "a") as f:
            f.write(f"{informacao}\n")
        return True
    else:
        return False


def deletar_informacao(arquivo,info):
    """
    Função genérica para remover dados em arquivo.
    """
    dados_atuais = get_dados_arquivo(arquivo)
    print(dados_atuais)

    if str(info) in dados_atuais:
        with open(lista_arquivos[arquivo], "w") as f:
            for dado in dados_atuais:
                if dado != str(info):
                    f.write(f"{dado}\n")
        return True
    else:
        return False



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