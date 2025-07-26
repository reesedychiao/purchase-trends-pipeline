from kafka import KafkaProducer
import json
import time
import pandas as pd

df = pd.read_excel('data/online_retail.xlsx')
df['InvoiceDate'] = df['InvoiceDate'].astype(str)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092', 
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = "orders"
try:
    for _, row in df.iterrows():
        message = row.to_dict()
        producer.send(topic, value=message)
        time.sleep(5)
except Exception as e:
    print("Error:", e)

producer.flush()
producer.close()