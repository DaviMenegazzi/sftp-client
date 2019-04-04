#===========================
#By Davi M. Silva
# -> SFTP server exlporer.

# - LIBS ---------------------
import pysftp
from termcolor import *
import os
import time
#-----------------------------

print(colored("Hello World, SFTP server explorer by Davi M. Silva.", "blue", attrs=["bold"]))
host     = input("IP Address: ")
username = input("  Username: ")
passwd   = input("  Password: ")

print("Connecting...")
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
with pysftp.Connection(host=host, username=username, password=passwd, cnopts=cnopts) as sftp:

    print("Connected.")
    dir = "/home/"
    os.system("clear")

    print("\nType '?h' to show the help menu.            ")
    while 1:
        console = input(colored(sftp.pwd, "green") + ': ')

        if console == "?h":
            print(colored("Avaliable commands: ", attrs=["bold"]))

            #copy
            #clear
            #cd
            #ls

            print(colored(" -> copy  [folder, file] > Shortcut: cp - Copy the file/folder."                            , "cyan"))
            print(colored(" -> clear                > Shortcut: cl - Clear the screen."                                , "cyan"))
            print(colored(" -> cd    [folder]       - Change the current working directory to the folder specified."   , "cyan"))
            print(colored(" -> ls                   - List all the files and folders of the current working directory.", "cyan"))
            print(colored(" -> exit                 - Exit from SFTP explorer."                                        , "cyan"))

        if console == "clear" or console == "cl":
            os.system("clear")

        if "copy" in console.split() or "cp" in console.split(): #Copia arquivos
            #-1 é a flag para o último index em uma lista
            fileToCopy = console.split()[-1]
            try:
                if not fileToCopy in sftp.listdir(dir):
                    print("File not found.")
                else:

                    if sftp.isdir(fileToCopy):
                        string = str(sftp.cwd(dir))
                        for itens in sftp.listdir(dir + fileToCopy + "/"):
                            print("Copying " + colored(itens, "red") + "...")
                        sftp.get_r(fileToCopy, os.getcwd())
                    else:
                        sftp.get("./" + fileToCopy, callback=teste(0, 100))

            except Exception as err:
                print("Something went wrong: " + err)

            print(f"'" + colored(fileToCopy, "red") + "' downloaded successfully.")

        if "cd" in console.split(): #Se mover nos diretórios do FTP
            try:
                arq = console.split()

                #print("console.split: " + str(arq))
                #print(len(arq))


                if  ".." in arq:
                    dirr = sftp.pwd
                    arq_split = dirr.split("/")

                    if arq_split[-1] in dirr:
                        dir = dir.replace(arq_split[-1] + "/", "")
                        sftp.cwd(dir)
                else:
                    if not arq[-1] in sftp.listdir(dir):
                        print(f"Folder '{console.split()[-1]}' not found.")
                    else:
                        #NOTE: Ele tem que juntar os outros index do split, tirando o primeiro, pois, ele é o comando.
                        nomeArquivo = console.split()[1]
                        dir += nomeArquivo + "/"

                        sftp.cwd(dir)

            except FileNotFoundError:
                print(f"Folder '{console.split()[-1]}' not found.")

            except Exception as err:
                print("Something went wrong: " + (err))

        if console.lower() == "ls": #Listar os diretórios
            print("")
            cout = 0
            for dirs in sftp.listdir(dir):
                cout += 1
                if sftp.isdir(dir + dirs + "/"):
                    print("{} folder - {}".format(colored(cout, "magenta", attrs=["reverse"]), dirs))
                else:
                    print("{}   file - {}".format(colored(cout, "white", attrs=["reverse"]), dirs))
            print("")
            #print(sftp.listdir(dir))

        if console.lower() == "exit":
            print("Exiting...")
            exit()
