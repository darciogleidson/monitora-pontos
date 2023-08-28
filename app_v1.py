#Aplicação no python para enviar uma mensagem para um grupo do telegram
#A mensagem será enviada se a condição for verdadeira
#A condição é que tenho uma tabela no banco de dados (postgres) no schema spia que é atualizada a cada 5 minutos
#A tabela é tb_passagem, nela tem os seguintes campos:
#id (int), data_passagem (date), placa (varchar), equipamento_id (int)
#Tenho uma lista de equipamentos de entrada
#Tenho uma lista de equipamentos de saida
#Quero que todo registro que entre na tabela tb_passagem e que o equipamento_id esteja na lista de equipamentos de entrada
#verifique se a placa tenha algum registro na lista de equipamentos de saida nos ultimos 7 dias
#se tiver, enviar uma mensagem no telegram
#e que o programa fique rodando em loop infinito
#e pegando os registros que entram na tabela tb_passagem nos ultimos 5 minutos

import psycopg2
import telepot
import time
import datetime
import os

#função para enviar mensagem no telegram
def send_message(msg):
    bot.sendMessage(chat_id, msg)

#função para verificar se a placa tem registro na lista de equipamentos de saida nos ultimos 7 dias
def verifica_placa(placa):
    #abre a conexão com o banco de dados
    conn = psycopg2.connect(host="localhost",database="spia", user="postgres", password="postgres")
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

#função para verificar se o equipamento é de entrada
def verifica_equipamento_entrada(equipamento_id):
    #verifica se o equipamento está na lista de equipamentos de entrada
    if equipamento_id in equipamentos_entrada:
        #se estiver na lista de equipamentos de entrada, retorna verdadeiro
        return True
    else:
        #se não estiver na lista de equipamentos de entrada, retorna falso
        return False

#função para verificar se o equipamento é de saida
def verifica_equipamento_saida(equipamento_id):
    #verifica se o equipamento está na lista de equipamentos de saida
    if equipamento_id in equipamentos_saida:
        #se estiver na lista de equipamentos de saida, retorna verdadeiro
        return True
    else:
        #se não estiver na lista de equipamentos de saida, retorna falso
        return False

#função para verificar se a placa já foi processada
def verifica_placa_processada(placa):
    #abre a conexão com o banco de dados
    conn = psycopg2.connect(host="localhost",database="spia", user="postgres", password="postgres")
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

