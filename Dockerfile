FROM python:3.8.3-buster

WORKDIR /app

ADD . /app

RUN apt-get -y update

# RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# RUN rm google-chrome-stable_current_amd64.deb

# Kalo error, ganti chromedriver versi 84
# RUN wget -N https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip -P ~/
# RUN unzip ~/chromedriver_linux64.zip -d ~/
# RUN rm ~/chromedriver_linux64.zip
# RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
# RUN chown root:root /usr/local/bin/chromedriver
# RUN chmod 0755 /usr/local/bin/chromedriver

RUN pip install -r requirement.txt

CMD ["python","main.py"]