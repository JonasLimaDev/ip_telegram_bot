from cgitb import text
import telebot
from modulos import *
import threading
import datetime
from time import sleep
from multiprocessing.pool import ThreadPool

token = open("TOKEN",'r') 
CHAVE_API = token.read()

bot = telebot.TeleBot(CHAVE_API)
criar_arquivos() # cria os arquivos iniciais que precisa

def ping(telebot):
    """
    Faz o teste de ping constante de ip
    """
    while(True):
        lista_usuarios = get_dados_arquivo("users")
        for ip in get_dados_arquivo("monitorados"):
            teste = ip_is_alive(ip)
            if not teste:
                for usuario in lista_usuarios:
                    #telebot.send_message(usuario, f"❌ Algo de errado com o IP: {ip}")
                    telebot.send_message(usuario, f"✅ Tudo certo com o IP: {ip}") #envia a mensagem tudo certo
            #else:
                #for usuario in lista_usuarios:
                    #bot.send_message(usuario, f"❌ Algo de errado com o IP: {ip}") #envia a mensagem de erro
        sleep(60)


@bot.message_handler(commands=["cadastrar"])
def cadastrar_usuario(mensagem):
    """
    Adiciona o usuário para receber alertas
    """
    chatid = mensagem.chat.id
    salvo = salvar_usuario(chatid)
    if salvo:
        bot.reply_to(mensagem, f"Você foi Adicionado é receberá um alerta quando algo acontecer")
    else:
        bot.reply_to(mensagem, f"Opa!!!\nVocê já está cadastrado para receber alertas")


@bot.message_handler(commands=["remover"])
def remover_usuario(mensagem):
    """
    Remove o usuário para receber alertas
    """
    chatid = mensagem.chat.id
    deletado = deletar_usuario(chatid)
    if deletado:
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


@bot.message_handler(commands=["help","ajuda"])
def menu_ajuda(mensagem):
    #print(mensagem.text)
    texto = """
    <b>Ajuda</b>
    Comandos Disponíveis:
    /cadastrar :
    Adiciona o usuáro para receber alertas.\n
    /remover :
    Remove o usuáro para receber alertas\n
    <code>/testar_ip</code>:
    faz um teste separado para um IP específico
    Ex: <code>/testar_ip 192.168.37.13</code>\n
    """

    bot.send_message(mensagem.chat.id, texto, parse_mode="HTML")


def verificar(mensagem):
    return True


@bot.message_handler(func=verificar)
def responder(mensagem):
    # print(mensagem)
    if mensagem.text == "13":
        texto = "BIRL!!!💪"
    elif mensagem.text.lower() == 'sai de casa':
        texto = "Comi Pra caralho POHA!!!"
    elif mensagem.text.lower() == 'birl':
        texto="🏋"
    else:
        texto = f"Não sei o que fazer com: '{mensagem.text}' tente\n/ajuda."

    bot.send_message(mensagem.chat.id, texto)


def listener(messages):
    for m in messages:
        time_m = datetime.datetime.fromtimestamp(m.date)
        if m.content_type == 'text':
            print(f"{time_m.strftime('%d/%m/%Y-%H:%M:%S')} | {m.chat.first_name} [{m.chat.id}]: {m.text}")
        else:
            print(f"{time_m.strftime('%d/%m/%Y-%H:%M:%S')} | {m.chat.first_name} [{m.chat.id}]: {m.content_type}")


if __name__ == "__main__":
    try:
        x = threading.Thread(target=ping, args=(bot,))
        x.start()
        bot.set_update_listener(listener)
        bot.infinity_polling()
    except Exception as inst:
        print(type(inst))
        print("\nOcorreu algum erro tente novamente")
        print("Execução Interrompida")
        quit()
        