FROM python:3.9
RUN mkdir /var/db-app
WORKDIR /var/db-app
COPY . .
RUN useradd -m -d /var/db-app -s /bin/bash appuser && \
    chown -R appuser:appuser /var/db-app
RUN apt-get update && pip install -r requirements.txt
EXPOSE 5000
USER appuser 
ENTRYPOINT ["python3"]
CMD ["app.py"]
