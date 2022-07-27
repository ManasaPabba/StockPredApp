FROM postgres:12

RUN apt-get update
RUN apt-get install -y postgresql-plpython3-12
RUN apt-get install -y python3 python3-pip
RUN cd /usr/lib/python3.9
RUN apt-get install -y git
RUN git clone https://github.com/AbdullahO/tspdb.git
RUN pip3 install tspdb/.
RUN cp tspdb/extension_py3/tspdb.control /usr/share/postgresql/12/extension/tspdb.control
RUN cp tspdb/extension_py3/tspdb--0.0.1.sql /usr/share/postgresql/12/extension/tspdb--0.0.1.sql

ENV POSTGRES_DB ''
ENV POSTGRES_USER ''
ENV POSTGRES_PASSWORD ''
COPY start.sh /docker-entrypoint-initdb.d/

USER postgres
# expose Postgres port
EXPOSE 5432
