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

# Calcula o limite de tempo para os últimos 20 minutos
limite_tempo = datetime.datetime.now() - datetime.timedelta(minutes=20)
# Calcula o limite de dias para os últimos 7 dias
limite_dias = datetime.datetime.now() - datetime.timedelta(days=7)

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
    #send_message("mensagem de teste")

    #ler o arquivo csv tabelaPassagem.csv
    df = pd.read_csv('tabelaPassagem.csv')

    #passa a coluna para campo datetime
    df['pas_dh_passagem'] = pd.to_datetime(df['pas_dh_passagem'])

    # Filtra os registros com base no limite de tempo
    df_filtrado = df[df['pas_dh_passagem'] >= limite_tempo]

    # Groupby por placa e maior pas_dh_passagem e com o ponto da passagem com maior pas_dh_passagem
    placas_distintas = df_filtrado.groupby(['placa']).agg({'pas_dh_passagem': 'max', 'equ_id_equipamento': 'max'}).reset_index()

    # Aplica DISTINCT no campo 'placa'
    #placas_distintas = df_filtrado['placa'].unique()
    print("Placas distintas: " + str(placas_distintas))

    #ler o arquivo csv tabelaPassagem.csv
    df_pontos_saida = pd.read_csv('tabelaPassagem.csv')

    #percorrer as placas_distintas e printar a placa, o equipamento e a data da passagem tirando a linha do cabeçalho
    for placa in placas_distintas.itertuples(index=False):

        df_pontos_saida['pas_dh_passagem'] = pd.to_datetime(df_pontos_saida['pas_dh_passagem'])
        df_passou = (df_pontos_saida['placa'] == placa[0]) & (df_pontos_saida['pas_dh_passagem'] >= limite_dias) & (df_pontos_saida['equ_id_equipamento'].isin(equipamentos_saida)).any()
        # Groupby por placa e maior pas_dh_passagem e com o ponto da passagem com maior pas_dh_passagem

        #se tiver registro, retorna verdadeiro
        if len(df_passou) > 0:
            df_passou['pas_dh_passagem'] = pd.to_datetime(df_passou['pas_dh_passagem'])
            df_passou = df_passou.groupby(['placa']).agg({'pas_dh_passagem': 'max', 'equ_id_equipamento': 'max'}).reset_index()
            print('df_passou')
            print(df_passou)
            send_message("Placa: " + placa[0] + " passou no Equipamento: " + str(placa[2]) + " na Data: " + str(placa[1]))
            #send_message(" e " + df_passou[0] + " também passou no Equipamento: " + str(df_passou[2]) + " na Data: " + str(df_passou[1]))

    #espera 1 minutos para fazer a verificação novamente
    time.sleep(30)
