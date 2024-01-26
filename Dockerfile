# Setting base image
FROM python:3.11.0

# Set working directory
WORKDIR .

# Copying the application into the container
COPY . .

# Setting environmental variables
ENV LOG_FILE_PATH=/var/local/panel_generator/logs/

	# -v /var/local/panel_generator/logs/:/var/local/panel_generator/logs/ \
    # -v /var/local/panel_generator/bedfiles/:/var/local/panel_generator/bedfiles/ \
    # -v /var/local/panel_generator/bedfile_jsons/:/var/local/panel_generator/bedfile_jsons/ \
    # -v /var/local/panel_generator/panel_jsons/:/var/local/panel_generator/panel_jsons/ \
    # -v /var/local/panel_generator/genes_jsons/:/var/local/panel_generator/genes_jsons/ \

# Installling dependencies
RUN pip install --upgrade pip
RUN pip install -r src/requirements.txt

# Creating directories and changing permissions
RUN mkdir -p /var/local/panel_generator/logs/
RUN chmod 777 /var/local/panel_generator/logs/



# CMD ["python", "./src/tools_v2.py", "./Draft_scripts/tools_v2.py"]
