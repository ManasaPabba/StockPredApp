FROM python:latest

RUN mkdir -p /home/app
COPY . /home/app
RUN pip install -r /home/app/requirements.txt


EXPOSE 8501

CMD streamlit run /home/app/app.py