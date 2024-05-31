FROM python:3.9.4

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' ml-api-user

WORKDIR /opt/sentiment_webapp

ARG PIP_EXTRA_INDEX_URL

# Install requirements
ADD ./ /opt/sentiment_webapp
RUN pip install --upgrade pip
RUN pip install -r /opt/sentiment_webapp/requirements.txt
RUN pip uninstall typing extensions
RUN pip uninstall fastapi -y
RUN pip install --no-cache fastapi

RUN chmod +x /opt/sentiment_webapp/run.sh
RUN chown -R ml-api-user:ml-api-user ./

USER ml-api-user

EXPOSE 8001

CMD ["bash", "./run.sh"]