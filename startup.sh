
echo "Make sure, you're executing this program in sudo."

#Inicializa o docker builder // caso contrário, mostra mensagem de erro.
docker build -t sftp-explorer . || read -p "docker.io is not installed, you want to install it? [Y/N]: " ifstate

fileName="sftp.sh"

#-eq é igual a "=="
if [ $ifstate=="Y" ];
then
  apt-get install docker.io
  #Inicializa a imagem no docker através do outro sh

else
  echo "Program installer canceled."
fi

touch $fileName
echo "echo \"Make sure you're executing in sudo.\"" >> fileName
echo "docker run -ti sftp-explorer || echo \"Docker cannot run.\"" >> fileName
chmod 100 $fileName

echo "Now, you can execute 'start.sh' file to start the script."

#Remove esse arquivo
rm startup.sh
