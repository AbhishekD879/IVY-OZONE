FROM python:2.7.12-alpine


ADD bet_finder /bet_finder
WORKDIR /bet_finder
ADD requirements.txt /bet_finder/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["sh", "-c", "python bet_finder.py"]