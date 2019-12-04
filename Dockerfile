FROM python:3.7

RUN pip install dash==1.6.1 dash-daq==0.3.1 pandas gevent
RUN pip install dash_bootstrap_components Image cvxpy

ADD data /data
ADD assets /assets
ADD *.py /

CMD ["python", "flask_server.py"]