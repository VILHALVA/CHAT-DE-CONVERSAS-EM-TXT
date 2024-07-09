import requests
import json
import os

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
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    resposta = self.gerar_respostas(mensagem)
                    self.responder(resposta, chat_id)
                    self.salvar_conversa(mensagem, resposta)  
                    
    def ler_novas_mensagens(self, iUPDATE_ID):
        iLINK_REQ = f'{self.iURL}getUpdates?timeout=5'
        if iUPDATE_ID:
            iLINK_REQ = f'{iLINK_REQ}&offset={iUPDATE_ID + 1}'
        iRESULT = requests.get(iLINK_REQ)
        return json.loads(iRESULT.content)

    def gerar_respostas(self, mensagem):
        mensagem = mensagem.lower()
        if mensagem in ("/start", "oi", "ola"):
            return '''😃Olá! Seja bem-vindo ao chatBot. Posso falar sobre Tecnologia, Ciência, Filosofia, Teologia e mais.'''
        elif any(palavra in mensagem for palavra in ["gosta de ciência", "gosta de astronomia"]):
            return '''🌝Sim, eu gosto muito de falar sobre ciência e astronomia.'''
        elif any(palavra in mensagem for palavra in ["tecnologia", "programação", "android", "robô"]):
            return '''🌝Eu gosto muito de falar sobre tecnologia.'''
        elif any(palavra in mensagem for palavra in ["filosofia", "pensamento"]):
            return '''🌝Filosofia é uma área fascinante.'''
        elif any(palavra in mensagem for palavra in ["teologia", "religião"]):
            return '''🌝Teologia explora questões espirituais.'''
        elif any(palavra in mensagem for palavra in ["sim", "gostei"]):
            return '''😁Ótimo! Fico feliz que tenha gostado.'''
        elif any(palavra in mensagem for palavra in ["não", "não entendi", "desculpe"]):
            return '''🔴Desculpe, não entendi sua mensagem.'''
        else:
            return f'''🔴Desculpe, não entendi sua mensagem.'''

    def responder(self, resposta, chat_id):
        iLINK_REQ = f'{self.iURL}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(iLINK_REQ)

    def salvar_conversa(self, mensagem, resposta):
        caminho_arquivo = os.path.join(self.diretorio_atual, "CONVERSAS.txt")
        with open(caminho_arquivo, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"USUÁRIO: {mensagem}\nBOT: {resposta}\n\n")
        print(f"Conversa salva em CONVERSAS.txt.")

bot = TelegramBot()
bot.Iniciar()
