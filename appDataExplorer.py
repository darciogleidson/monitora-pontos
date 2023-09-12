#import psycopg2
import telepot
import time
import datetime
import os
from dotenv import load_dotenv
import pandas as pd
import pytz

#carrrega as variaveis de ambiente
load_dotenv()
#lista de equipamentos de entrada
equipamentos_entrada = [11550,11551,7780,9766,8964,8965,9194,9187,9706,9704,9771,9025,9031,48766,48767,48768,48772,48773,48774,48778,48779,48780]
#lista de equipamentos de saida
equipamentos_saida = [15701,15717,15626,15624,17888,15646,15640,15722,15668,972,15628,15694,5634,15711,18393]

# Calcula o limite de tempo para os últimos 20 minutos
limite_tempo = datetime.datetime.now(pytz.utc) - datetime.timedelta(minutes=20)
# Calcula o limite de dias para os últimos 7 dias
limite_dias = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)

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
    df = pd.read_csv('tabelaDataExplorer.csv')

    #passa a coluna para campo datetime
    df['dataRecebimento'] = pd.to_datetime(df['dataRecebimento'])

    # Filtra os registros com base no limite de tempo
    df_filtrado = df[df['dataRecebimento'] >= limite_tempo]

    # Groupby por placa e maior pas_dh_passagem e com o ponto da passagem com maior pas_dh_passagem
    placas_distintas = df_filtrado.groupby(['placa']).agg({'dataPassagem': 'max', 'equipamento_id': 'max'}).reset_index()

    #ler o arquivo csv tabelaPassagem.csv
    df_pontos_saida = pd.read_csv('tabelaDataExplorer.csv')
    df_pontos_saida = df_pontos_saida[df_pontos_saida['equipamento_id'].isin(equipamentos_saida)]

    #percorrer as placas_distintas e printar a placa, o equipamento e a data da passagem tirando a linha do cabeçalho
    for placa in placas_distintas.itertuples(index=False):

        df_pontos_saida['dataPassagem'] = pd.to_datetime(df_pontos_saida['dataPassagem'])
        df_passou = df_pontos_saida[(df_pontos_saida['placa'] == placa[0]) & (df_pontos_saida['dataPassagem'] >= limite_dias)]
        # Groupby por placa e maior pas_dh_passagem e com o ponto da passagem com maior pas_dh_passagem

        #se tiver registro, retorna verdadeiro
        if len(df_passou) > 0:
            df_passou['dataPassagem_formatada'] = df_passou['dataPassagem'].dt.strftime('%d-%m-%y %H:%M')
            data_passagem_1 = pd.to_datetime(placa.dataPassagem)
            send_message("Placa: " + placa.placa + " passou no Equipamento: " + str(placa.equipamento_id) + " na Data: " + (data_passagem_1.strftime('%d-%m-%y %H:%M')) +
                         " e também passou no Equipamento: " + str(df_passou['equipamento_id'].iloc[0]) + " na Data: " + str(df_passou['dataPassagem_formatada'].iloc[0]))

    #espera 1 minutos para fazer a verificação novamente
    time.sleep(30)
