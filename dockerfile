FROM python:3.6.7
<<<<<<< HEAD
ADD /main/main.py / dockerfile / requirements.txt / README.md /
=======
ADD main.py / dockerfile / requirements.txt /
>>>>>>> 30c5e741823954b7bcbabde431a6431cfc984fd0
RUN pip install -r requirements.txt
CMD ["python", "./main/main.py"]
