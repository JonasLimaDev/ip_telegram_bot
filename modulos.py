import os
global lista_arquivos 

lista_arquivos={
        "users":"./arquivos/users.txt",
        "monitorados":"./arquivos/ips_monitorados.txt",
        "alertas":"./arquivos/ips_alertas.txt"}


def criar_arquivos():
    for arquivo in lista_arquivos.values():
        if not os.path.exists(arquivo):
            arquivo = open(arquivo,'w')
            arquivo.close()
    
def get_lista_usuarios():
    """
    Retorna uma lista com os id's de chat de usuários cadastrados para receber alerta.
    """
    lista =[]
    with open(lista_arquivos['users'], "r") as file:
            lines = file.readlines()
            for linha in file.readlines()():
                lista.append(linha.replace("\n",""))
    return lista


def inserir_usuario(user_chat_id):
    usuarios_atuais = get_lista_usuarios()
    if str(user_chat_id) not in usuarios_atuais:
        with open(lista_arquivos['users'], "a") as f:
            f.write(f"{user_chat_id}\n")
        return True
    else:
        return False

def remover_usuario(user_chat_id):
    usuarios_atuais = get_lista_usuarios()
    if str(user_chat_id) in usuarios_atuais:
        with open(lista_arquivos['users'], "w") as f:
            for usuario in usuarios_atuais:
                if usuario != str(user_chat_id):
                    f.write(f"{usuario}\n")
        return True
    else:
        return False