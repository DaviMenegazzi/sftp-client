#===========================
#By Davi M. Silva
# -> SFTP server exlporer.

# - LIBS ---------------------
import pysftp
from termcolor import *
import os
import time
import gnureadline # Converting the arrow keys to the commands
#-----------------------------
os.system("clear")

try:
    print(colored("SFTP Server Client | Davi M. Silva.", "blue", attrs=["bold"]))
    host     = input("-- IP Address: ")
    username = input("--   Username: ")
    passwd   = input("--   Password: ")
except KeyboardInterrupt:
    print("\nExiting...")
    exit()

h = []
def history(command):
    if command == "history" or command == "hist":
        print(f"History: ({len(h)} items)")
        for i in range(0, len(h)):
            print(f"{i + 1} -- " + h[i])
    else:
        print("-- Command not found.")

def att_size(remote_dir):
    dir_struct = sftp.listdir_attr(remote_dir)

    for attr in dir_struct:
        return attr.st_size

def instructions():
    print("")
    print(colored("ㅤ", "magenta", attrs=["reverse"]) + " | This color represents the folders.")
    print(colored("ㅤ", "white", attrs=["reverse"])   + " | This color represents the files.  ")
    print("")

print("Connecting...")
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
with pysftp.Connection(host=host, username=username, password=passwd, cnopts=cnopts) as sftp:

    print("Connected.")
    dir = "/home/"
    os.system("clear")

    print("\nType '?h' to show the help menu.            ")
    while 1:
        try:
            if os.geteuid() != 0: # Verifica se é root ou não.
                console = input(colored("(not root)", "white", attrs=["reverse"]) + " " + colored(sftp.pwd, "green") + ': ') #Console onde será executado os comandos
                h.append(console)
            else:
                console = input(colored("(root)", "white", attrs=["reverse"]) + " " + colored(sftp.pwd, "green") + ': ') #Console onde será executado os comandos
                h.append(console)

            if console == "?h":
                print(colored("Avaliable commands: ", attrs=["bold"]))

                #copy
                #clear
                #cd
                #ls
                #exit
                #hist
                #inst

                print(colored(" -> copy  [folder, file] > Shortcut: cp - Copy the file/folder."                                , "cyan"))
                print(colored(" -> clear                > Shortcut: cl - Clear the screen."                                    , "cyan"))
                print(colored(" -> cd    [folder]       - Change the current working directory to the folder specified."       , "cyan"))
                print(colored(" -> ls                   - List all the files and folders of the current working directory."    , "cyan"))
                print(colored(" -> history              > Shortcut: hist - List all the commands that have been executed."     , "cyan"))
                print(colored(" -> instructions         > Shortcut: inst - Show the instructions about the files and folders." , "cyan"))
                print(colored(" -> exit                 - Exit from SFTP Client."                                              , "cyan"))

            if console == "instructions" or console == "inst":
                instructions()

            if console == "clear" or console == "cl":
                os.system("clear")

            if console == "hist" or console == "history":
                history(console)

            if "copy" in console.split() or "cp" in console.split(): #Copia arquivos
                #-1 é a flag para o último index em uma lista
                fileToCopy = console.split()[-1]
                try:
                    if not fileToCopy in sftp.listdir(dir):
                        print("-- File not found.")
                    else:

                        if sftp.isdir(fileToCopy):
                            string = str(sftp.cwd(dir))
                            for itens in sftp.listdir(dir + fileToCopy + "/"):
                                print("Copying " + colored(itens, "red") + "...")
                            sftp.get_r(fileToCopy, os.getcwd())
                        else:
                            sftp.get("./" + fileToCopy)

                except Exception as err:
                    print("-- Something went wrong: " + err)

                print(f"'" + colored(fileToCopy, "red") + "' downloaded successfully.")


            if "cd" in console.split(): #Se mover nos diretórios do FTP
                try:
                    arq = console.split()
                    if  ".." in arq:
                        if dir == "/":
                            print("-- You are in the root folder.")
                            pass
                        else:
                            dirr = sftp.pwd
                            arq_split = dirr.split("/")

                            if arq_split[-1] in dirr:
                                dir = dir.replace(arq_split[-1] + "/", "")
                                sftp.cwd(dir)
                    else:
                        #NOTE: Ele tem que juntar os outros index do split, tirando o primeiro, pois, ele é o comando.
                        comando = console.split()[0]
                        pasta = console.replace(comando + " ", "")

                        if not pasta in sftp.listdir(dir):
                            print(f"-- Folder '{pasta}' not found.")
                            pass
                        else:
                            dir += pasta + "/"
                            #print("DIRETÓRIO: " + dir)

                            sftp.cwd(dir)

                except FileNotFoundError:
                    comando = console.split()[0]
                    pasta = console.replace(comando + " ", "")

                    print(f"-- Folder '{pasta}' not found.")

                except Exception as err:
                    print("-- Something went wrong: " + (err))

            if console.lower() == "ls": #Listar os diretórios
                print("")
                cout = 0
                for dirs in sftp.listdir(dir):
                    cout += 1
                    if sftp.isdir(dir + dirs + "/"):

                        colored_magenta = colored(cout, "magenta", attrs=["reverse"])
                        colored_branco  = colored(cout, "white", attrs=["reverse"])

                        print("{} folder - {}".format(colored_magenta, dirs))
                    else:
                        print("{}   file - {}".format(colored_branco, dirs))
                print("")


            if console.lower() == "exit":
                print("-- Exiting...")
                exit()

        except KeyboardInterrupt:
            print("\n-- Exiting...")
            exit()
