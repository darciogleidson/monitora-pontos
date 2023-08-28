#aplicação em python para monitoramento de passagem de veículos em rodovias
#tenho uma lista de equipamentos de entrada
#tenho uma lista de equipamentos de saida
#pegar as passagens dos ultimos 20 minutos dos equipamentos de entrada
#verificar se a placa já passou nos equipamentos de saida nos ultimos 7 dias
#se passou, enviar mensagem para o telegram, avisando a data e hora da passagem e o equipamento de entrada
#e a data e hora da passagem e o equipamento de saida
#se não passou, não fazer nada

#import psycopg2
import telepot
import time
import datetime
import os
from dotenv import load_dotenv

#carrrega as variaveis de ambiente
load_dotenv()
#lista de equipamentos de entrada
equipamentos_entrada = "1,2,3,4,5,6,7,8,9,10"
#lista de equipamentos de saida
equipamentos_saida = "11,12,13,14,15,16,17,18,19,20"

#função para enviar mensagem no telegram
def send_message(msg):
    #token do bot do telegram
    token = os.getenv("BOT_TOKEN")
    #chat_id do telegram
    chat_id = os.getenv("CHAT_ID_DESENVOLVIMENTO")
    #cria o objeto bot
    bot = telepot.Bot(token)
    bot.sendMessage(chat_id, msg)
    # Substitua 'path/to/your/image.jpg' pelo caminho da imagem que você deseja enviar
    image_path = 'sonic.jpg'

    # Enviar a imagem
    bot.sendPhoto(chat_id, open(image_path, 'rb'))
    #printa a mensagem que foi enviada
    print("Mensagem enviada: " + msg)

#função para verificar se a placa tem registro na lista de equipamentos de saida nos ultimos 7 dias
def verifica_placa(placa):
    #abre a conexão com o banco de dados
    conn = psycopg2.connect(host="localhost",database="spia", user="sail", password="password")
    #abre o cursor para executar os comandos sql
    cur = conn.cursor()
    #monta o sql
    sql = "select * from tb_passagem where placa = '" + placa + "' and equipamento_id in (" + equipamentos_saida + ") and data_passagem >= current_date - 7"
    #executa o sql
    cur.execute(sql)
    #pega o resultado do sql
    rows = cur.fetchall()
    #fecha o cursor
    cur.close()
    #fecha a conexão
    conn.close()
    #verifica se tem registro
    if len(rows) > 0:
        #se tiver registro, retorna verdadeiro
        return True
    else:
        #se não tiver registro, retorna falso
        return False

#aplicação em loop infinito, fazendo a verificação a cada 5 minutos
while True:
    #printar mensagem que executou a verificação
    print("Executando verificação: " + str(datetime.datetime.now()))
    #mandar jpg para o telegram que esta no mesmo diretorio do script
    send_message("mensagem de teste")


    ##pegar as passagens dos ultimos 20 minutos dos equipamentos de entrada
    ##monta o sql
    #sql = "select * from tb_passagem where equipamento_id in (" + str(equipamentos_entrada) + ") and data_passagem >= current_timestamp - interval '60 minutes'"
    #print(sql)
    ##abre a conexão com o banco de dados
    #conn = psycopg2.connect(host="localhost",database="spia", user="sail", password="password")
    ##abre o cursor para executar os comandos sql
    #cur = conn.cursor()
    ##executa o sql
    #cur.execute(sql)
    ##pega o resultado do sql
    #rows = cur.fetchall()
    ##fecha o cursor
    #cur.close()
    ##fecha a conexão
    #conn.close()
#
    ##printar o resultado do sql
    #print(rows)
#
    ##percorre o resultado do sql para verificar se a placa já passou nos equipamentos de saida nos ultimos 7 dias
    #for row in rows:
    #    print(row[2])
    #    #verifica se a placa já passou nos equipamentos de saida nos ultimos 7 dias
    #    if verifica_placa(row[2]):
    #        #se passou, envia mensagem para o telegram
    #        send_message("Placa: " + row[2] + " - Data e Hora: " + str(row[3]) + " - Equipamento de Entrada: " + str(row[1]))

    #espera 1 minutos para fazer a verificação novamente
    time.sleep(60)
