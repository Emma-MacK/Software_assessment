# Running Docker #

This document described how to build and run the app in a docker

This will allow the app to run without the need to create a conda environment or install necessary
dependencies.



## Using Make ##

If choosing to interact with the app through the command line you can build and run the docker using
`make`

N.B. Currently `make` can not be used to run the frotend in docker. If you wan't to interact with the
frontend please see documentation below on running the frotend in docker.

### Building and running the docker ###

The Makefile is set up to run `docker build` and `docker run` by default. Therefore there is no need
to execute separate command for these.
The first time you are running the docker simply use the following command to build your image and run
the container.

```
make STRING_ARG=Rcode
```

N.B.Make sure to replace `Rcode` with a valid test directory code.
e.g.

```
make STRING_ARG=R24
```

Of note, the first time this is run a permission error may occur. This can be resolved using `sudo chmod 666 /var/run/docker.sock`, which gives docker permission to interact with files

### Running the container from the existing image ###
Once you have run the container for the first time there is no need to keep rebuilding the image. To override the
default `make` command simply adjust the `make` command as follows:

```
make run STRING_ARG=Rcode
```

### Cleaning up images and containers ###
If you want to clean up your images or containers you can either use:

```
make clean
```
This will result in the container being removed.

```
make hard_clean
```
This will result in the container and the image being deleted.



## Using Docker to run the frontend while in root ##

Currently the ability to run the frontend from docker has not been integrated
into the makefile. However you can run the frotend in docker by following the
below commands.

First build the docker

```
docker build -t test_docker .
```

Then run the following command :

```
docker run -p 8000:8000 -v $(pwd):/code test_docker python frontend/manage.py runserver 0.0.0.0:8000
```

N.B. Feel free to replace test_docker with a name of your choosing

Finally access the frontend through the url:

http://127.0.0.1:8000/

## Retrieving files from docker ##

Files made using docker are held on the docker image and are not immediately accessible.
To retrieve files from the docker use the following command:

```
docker cp test_docker:[path to file in docker] [path to desired location]
```

example

```
docker cp test_docker:./panel_output.bed .
```
