# specify start image
FROM python

# all commands start from this directory
WORKDIR /

# copy all files from this folder to working directory (ignores files in .dockerignore)
COPY . /

RUN pip3 install -r requirements.txt

# set a default environment variable for the name
ENV BOT_NAME='sizif-bot'

# set the start command
CMD [ "python3", "bot.py"]