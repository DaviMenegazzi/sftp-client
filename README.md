### SFTP SERVER ACCESS
With this script you can access SFTP servers from a terminal in linux (compatible only with linux).

### HOW WORKS?
This script has a very used and very reliable library for accessing SFTP servers called [pysftp](https://pysftp.readthedocs.io/en/release_0.2.9/).

### DOCKERFILE
You will need install docker to build the script:
```bash
 $ sudo apt-get install docker.io
```
and then, you can run the docker builder with this command:
```bash
$ docker build -t sftp-explorer .
```
and execute...
```bash
$ docker run -ti sftp-explorer
```
If necessary you will need to do in sudo.
