FROM python:3.6
ENV WD=/tr_cli
ADD ./ ${WD}
WORKDIR ${WD}

RUN pip install -e .

CMD ["python", "crlat_testrail_integration/testrail_coverage.py"]