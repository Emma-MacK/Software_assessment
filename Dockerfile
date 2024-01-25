
FROM python:3.11.0

WORKDIR .

COPY . .

RUN pip install --upgrade pip
RUN pip install -r src/requirements.txt

# CMD ["python", "./Draft_scripts/emma_get_bed.py", "./Draft_scripts/tools_v2.py"]
