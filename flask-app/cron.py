import plotly
from plotly.graph_objs import Scatter, Layout
import yaml
from bs4 import BeautifulSoup
from urllib import request as req

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, DateTime, Float, and_, Integer
from sqlalchemy.sql import column
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import sessionmaker, load_only


db_string = "postgresql://user:password@192.168.0.1/db_name"
db = create_engine(db_string)

meta = MetaData(db)
Base = declarative_base()

class Measurement(Base):
    __tablename__ = 'measurements'


    id = Column(Integer, primary_key=True)
    node = Column(String)
    sensor = Column(String)
    value = Column(Float)
    time = Column(DateTime, default=datetime.datetime.now)

Session = sessionmaker(bind=db)
session = Session()

def generate_plot(node_name, sensor_name, delta=datetime.timedelta(hours=24), suffix='24h', path='static/plots/'):
    x = []
    y = []

    for record in session.query(Measurement).filter(Measurement.node == node_name). \
            filter(Measurement.sensor == sensor_name). \
            filter(Measurement.time > datetime.date.today() - delta).all():
        print(record.value)
        x.append(record.time)
        y.append(record.value)

    plotly.offline.plot({
        "data": [Scatter(x=x, y=y)],
        "layout": Layout(title=str(node_name + ': ' + sensor_name + ' - ' + suffix)),
    }, filename=str(path + node_name + '_' + sensor_name + '_' + suffix + '.html'))


with open("etc/sw-mon.yml", 'r') as config:
    try:
        config = yaml.load(config)
    except yaml.YAMLError as exc:
        print(exc)

for node, data in config.get('nodes', {}).items():
    print(node)
    for sensor in data.get('sensors', []):
        generate_plot(node_name=node, sensor_name=sensor, delta=datetime.timedelta(minutes=90), suffix='90m')
        generate_plot(node_name=node, sensor_name=sensor, delta=datetime.timedelta(hours=24), suffix='24h')
        generate_plot(node_name=node, sensor_name=sensor, delta=datetime.timedelta(days=7), suffix='7d')
