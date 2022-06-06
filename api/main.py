from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from kafka import KafkaProducer
from datetime import datetime
import json
import logging

'''
API Gateway and Kafka Producer module

Objective 1: Collect customer transactions
Objective 2: Produce customer transactions to Kafka
'''

# For logging
logging.basicConfig(
    filename = "api-ingestion.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

KAFKA_PRODUCER = KafkaProducer(bootstrap_servers = 'kafka:9092')

def produce_to_kafka(producer, topic, json_event):
    """function that produces events to kafka topic

    Args:
        producer (KafkaProducer): producer object
        topic (str): name of the topic 
        json_event (json): json event recieved by the API gateway
    """

    def success(metadata):
        print(metadata.topic)
    
    def error(exception):
        print(exception)

    # kafka reads objects of the type "byte"
    bytes_event = bytes(json_event, 'utf-8')
    producer.send(topic, bytes_event).add_callback(success).add_errback(error)
    producer.flush()




class InvoiceItem(BaseModel):
    '''
    API messages JSON Schema
    '''
    InvoiceNo: str
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: int
    Country: str


app = FastAPI()


@app.get('/')
async def root():
    return {'Hello World'}


@app.post('/invoices')
async def post_invoice(item: InvoiceItem):
    try:
        # date format modification to meet ANSI standard
        old_date = datetime.strptime(item.InvoiceDate, "%d/%m/%Y %H:%M")
        item.InvoiceDate = datetime.strftime(old_date, "%Y-%m-%d %H:%M:%S")
        
        # json_item -> to be returned as a API response
        # str_item -> to be produced to Kafka
        json_item = jsonable_encoder(item)
        str_item = json.dumps(json_item)

        produce_to_kafka(KAFKA_PRODUCER, 'customer-event-api', str_item)

        logging.info(f"{str_item} event successfully produced")

        return JSONResponse(json_item, status_code=201)

    except Exception as err:
        logging.error(f"{err.__class__}\t{err}")




