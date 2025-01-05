FROM python:3.9
RUN mkdir /var/frontend
WORKDIR /var/frontend
COPY . .
RUN useradd -m -d /var/frontend -s /bin/bash appuser && \
    chown -R appuser:appuser /var/frontend
RUN apt-get update && pip install -r requirements.txt
EXPOSE 8080
USER appuser 
ENTRYPOINT ["python3"]
CMD ["app.py"]
