#import psycopg2
import telepot
import time
import datetime
import os
from dotenv import load_dotenv
import pandas as pd

#carrrega as variaveis de ambiente
load_dotenv()
#lista de equipamentos de entrada
equipamentos_entrada = "1,2,3,4,5,6,7,8,9,10"
#lista de equipamentos de saida
equipamentos_saida = ["11,12,13,14,15,16,17,18,19,20"]

#função para enviar mensagem no telegram
def send_message(msg):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID_DESENVOLVIMENTO")

    bot = telepot.Bot(token)
    bot.sendMessage(chat_id, msg)

    # exemplo enviar imagem
    # image_path = 'sonic.jpg'
    # bot.sendPhoto(chat_id, open(image_path, 'rb'))

    # print("Mensagem enviada: " + msg)

#aplicação em loop infinito, fazendo a verificação a cada 5 minutos
while True:
    #printar mensagem que executou a verificação
    print("Executando verificação: " + str(datetime.datetime.now()))
    #mandar jpg para o telegram que esta no mesmo diretorio do script
    #send_message("mensagem de teste")


    #ler o arquivo csv tabelaPassagem.csv
    df = pd.read_csv('tabelaPassagem.csv')
    #pegar todos os registros dos ultimos 20 minutos, baseado no campo pas_dh_passagem
    df['pas_dh_passagem'] = pd.to_datetime(df['pas_dh_passagem'])

    # Calcula o limite de tempo para os últimos 20 minutos
    limite_tempo = datetime.datetime.now() - datetime.timedelta(minutes=20)

    # Filtra os registros com base no limite de tempo
    df_filtrado = df[df['pas_dh_passagem'] >= limite_tempo]

    # Aplica DISTINCT no campo 'placa'
    placas_distintas = df_filtrado['placa'].unique()
    print("Placas distintas: " + str(placas_distintas))

    #ler o arquivo csv tabelaPassagem.csv
    df_pontos_saida = pd.read_csv('tabelaPassagem.csv')

    for placa in placas_distintas:
        #verifica se a placa tem passage nos equipamentos de saida nos ultimos 7 dias
        #ERRO
        #df = df[(df['pas_ds_placa'] == placa) & (df['equ_id_equipamento'].isin(equipamentos_saida.split(","))) & (df['pas_dh_passagem'] >= datetime.datetime.now() - datetime.timedelta(days=7))]
        print(df_pontos_saida)
        print('-------------------')
        print(equipamentos_saida)
        print('-------------------')
        #placa_existente = (df['placa'] == placa_desejada) & (df['equipamento_id'].isin(equipamentos_saida)).any()
        df_passou =  (df_pontos_saida['placa'] == placa) & (df_pontos_saida['equ_id_equipamento'].isin(equipamentos_saida)).any()
        print(df_passou)
        #se tiver registro, retorna verdadeiro
        if len(df_passou) > 0:
            send_message("Placa " + placa + " passou nos pontos de saida nos ultimos 7 dias")

    #espera 1 minutos para fazer a verificação novamente
    time.sleep(60)