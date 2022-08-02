import telebot
from .modulos import *
import threading
import subprocess  
import platform , os    

from time import sleep
from multiprocessing.pool import ThreadPool


token = open("TOKEN",'r') 
CHAVE_API = token.read()

criar_arquivos()

bot = telebot.TeleBot(CHAVE_API)


def ip_is_alive(ip_str):
    #print(ip_str)
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', ip_str]
    teste_ip  = subprocess.call(command,stdout=subprocess.PIPE)
    if teste_ip == 0:
        return True
    else:
        return False


def ping(bot):
    """
    Faz o teste de ping constante de ip
    """
    while(True):

        lista_usuarios = usuarios_cadastrados()
        for ip in listar_ips():
            teste = ip_is_alive(ip)
            if not teste:
                for usuario in lista_usuarios:
                    bot.send_message(usuario, f"❌ Algo de errado com o IP: {ip}")
                    #bot.send_message(usuario, f"✅ Tudo certo com o IP: {ip}") #envia a mensagem tudo certo
            #else:
                #for usuario in lista_usuarios:
                    #bot.send_message(usuario, f"❌ Algo de errado com o IP: {ip}") #envia a mensagem de erro
        sleep(60)


@bot.message_handler(commands=["casa"])
def opcao3(mensagem):
    chatid = mensagem.chat.id
    bot.send_message(mensagem.chat.id, f"Sai de casa poha")


@bot.message_handler(commands=["cadastrar"])
def cadastrar_usuario(mensagem):
    """
    Adiciona o usuário para receber alertas
    """
    chatid = mensagem.chat.id
    #bot.send_message(mensagem.chat.id, f"Adicionar Usuário")
    usuarios_atuais = usuarios_cadastrados()
    arquivo = open("./users.txt",'a')
    if str(chatid) not in usuarios_atuais:
        # Verifica se o usuário não está na lista e o adiciona
        arquivo.write(f"{chatid}\n")
        arquivo.close()
        bot.reply_to(mensagem, f"Você foi Adicionado é receberá um alerta quando algo acontecer")
    else:
        bot.reply_to(mensagem, f"Opa!!!\n Você já está cadastrado para receber alertas")


@bot.message_handler(commands=["remover"])
def remover_usuario(mensagem):
    """
    Remove o usuário para receber alertas
    """
    chatid = mensagem.chat.id
    #bot.send_message(mensagem.chat.id, f"num vai dar não 🙁")
    usuarios_atuais = usuarios_cadastrados()
    if str(chatid) in usuarios_atuais:
        with open("./users.txt", "r") as f:
            lines = f.readlines()
        with open("./users.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != str(chatid):
                    f.write(line)
        bot.reply_to(mensagem, f"Você foi Removido e  não receberá mais alertas")
    else:
        bot.reply_to(mensagem, f"Opa!!!\n Você Não está na lista para receber alertas")


@bot.message_handler(commands=["testar_ip"])
def verificar_ip(mensagem):
    """
    Teste um IP específico passado pelo usuário
    """
    pool = ThreadPool(processes=1)
    ip = str(mensagem.text).replace("/testar_ip","")
    ip = ip.strip()
    #teste = ip_is_alive(ip)

    async_result = pool.apply_async(ip_is_alive, (ip,)) # tuple of args for foo
    teste = async_result.get()

    if teste:
        bot.reply_to(mensagem, f"✅ Tudo certo com o IP: {ip}")
    else:
        bot.reply_to(mensagem, f"❌ Algo de errado com o IP: {ip}")


def verificar(mensagem):
    return True


@bot.message_handler(func=verificar)
def responder(mensagem):
    #print(mensagem.text)
    if mensagem.text == '13':
        texto = "BIRL!!!💪"
    else:
        texto = """
    Escolha uma opção para continuar (Clique no item):
     /cadastrar Adiciona o usuáro para receber alertas.
     /remover Remove o usuáro para receber alertas
     /casa vai sair?
     Responder qualquer outra coisa não vai funcionar, clique em uma das opções
     """

    bot.reply_to(mensagem, texto)


@bot.message_handler(commands=["help","ajuda"])
def responder(mensagem):
    #print(mensagem.text)
    texto = """
    Escolha uma opção para continuar (Clique no item):\n
    /cadastrar :\n
    Adiciona o usuáro para receber alertas.\n
    /remover :\n
    Remove o usuáro para receber alertas\n
    /testar_ip\n
    faz um teste separado para um IP específico
    Ex: /testar_ip 192.168.37.13\n
    """

    bot.send_message(mensagem.chat.id, texto)



x = threading.Thread(target=ping, args=(bot))
x.start()
listar_ips()



bot.polling()
