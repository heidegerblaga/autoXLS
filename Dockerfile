FROM python:3.10.10

ADD main.py .
ADD exl.py .
COPY ./arkusze ./arkusze
ADD arkusze/nazwa.xlsx ./arkusze



RUN pip install pandas
RUN pip install openpyxl


CMD ["python","./main.py"]