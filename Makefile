# Makefile

# Defining variables
IMAGE_NAME = panel_generator
CONTAINER_NAME = run_container
VERSION = latest
STRING_ARG ?= Specify Rcode

# Declare phony targets
.PHONY: all build run clean

# Setting default targets
all: build run

# Build the docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the docker container and mount volumes
# TODO Change these as needed for personal use. host_path:containter_path
run:
	docker run \
	-v /var/local/panel_generator/logs/:/var/local/panel_generator/logs/ \
    -v /var/local/panel_generator/bedfiles/:/var/local/panel_generator/bedfiles/ \
    -v /var/local/panel_generator/bedfile_jsons/:/var/local/panel_generator/bedfile_jsons/ \
    -v /var/local/panel_generator/panel_jsons/:/var/local/panel_generator/panel_jsons/ \
    -v /var/local/panel_generator/genes_jsons/:/var/local/panel_generator/genes_jsons/ \
	-it --rm \
	--name $(CONTAINER_NAME) $(IMAGE_NAME):$(VERSION) \
	python src/tools_v2.py -ID $(STRING_ARG)

# Cleans away the docker image.
clean_image:
	docker rmi $(IMAGE_NAME) || true
