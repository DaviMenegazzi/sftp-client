FROM python:3.6.7
ADD /main/main.py / dockerfile / requirements.txt / README.md /
RUN pip install -r requirements.txt
CMD ["python", "./main/main.py"]
