FROM python:3.11.0

WORKDIR .

COPY . .

RUN pip install --upgrade pip
RUN pip install -r src/requirements.txt

EXPOSE 8000

CMD ["python", "./src/tools_v2.py", "./Draft_scripts/tools_v2.py"]
