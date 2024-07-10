import requests
import json
import os
from RESPOSTAS import respostas

class TelegramBot:
    def __init__(self):
        from TOKEN import TOKEN 
        self.iURL = f"https://api.telegram.org/bot{TOKEN}/"
        self.diretorio_atual = os.path.dirname(os.path.abspath(__file__))  
        
    def Iniciar(self):
        iUPDATE_ID = None
        while True:
            ATUALIZACAO = self.ler_novas_mensagens(iUPDATE_ID)
            IDADOS = ATUALIZACAO["result"]
            if IDADOS:
                for dado in IDADOS:
                    iUPDATE_ID = dado['update_id']
                    if "message" in dado: 
                        mensagem = str(dado["message"]["text"])
                        chat_id = dado["message"]["from"]["id"]
                        user = dado["message"]["from"]
                        resposta = self.gerar_respostas(mensagem)
                        self.responder(resposta, chat_id)
                        self.salvar_conversa(mensagem, resposta, user)
                    
    def ler_novas_mensagens(self, iUPDATE_ID):
        iLINK_REQ = f'{self.iURL}getUpdates?timeout=5'
        if iUPDATE_ID:
            iLINK_REQ = f'{iLINK_REQ}&offset={iUPDATE_ID + 1}'
        iRESULT = requests.get(iLINK_REQ)
        return json.loads(iRESULT.content)

    def gerar_respostas(self, mensagem):
        mensagem = mensagem.lower()
        for resposta in respostas:
            if any(palavra in mensagem for palavra in resposta["palavras_chave"]):
                return resposta["resposta"]
        return '''🔴Desculpe, não entendi sua mensagem.'''

    def responder(self, resposta, chat_id):
        iLINK_REQ = f'{self.iURL}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(iLINK_REQ)

    def salvar_conversa(self, mensagem, resposta, user):
        user_info = f"\n🗣USUÁRIO: @{user.get('username', 'N/A')}\n🆔ID: {user['id']}\n🉑NOME: {user.get('first_name', 'N/A')} {user.get('last_name', '')}"
        caminho_arquivo = os.path.join(self.diretorio_atual, "CONVERSAS.txt")
        with open(caminho_arquivo, "a", encoding="utf-8") as arquivo:
            arquivo.write("=" *50 + "\n")
            arquivo.write(f"{user_info}\n👄DISSE: {mensagem}\n🤖BOT: {resposta}\n")
            arquivo.write("=" *50 + "\n")
        print(f"Conversa salva em CONVERSAS.txt.")

bot = TelegramBot()
bot.Iniciar()
