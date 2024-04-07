from newsapi import NewsApiClient
from confluent_kafka import Producer, KafkaError
import time
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key='670c36ccfaac4136836b803f727940f3')

# Initialize Kafka Producer configuration
config = {
    'bootstrap.servers': 'part1-kafka-1:9092',
    'client.id': 'news-kafka-producer',
    'default.topic.config': {'acks': 'all'}
}

# Initialize Kafka Producer
producer = Producer(config)

iteration = 0  # Counter for iterations

def delivery_report(err, msg):
    """Delivery report callback."""
    global iteration
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}] - Headline: {msg.key().decode('utf-8')}, Iteration: {iteration}")

# Main function to fetch and publish news headlines to Kafka in a streaming manner
def fetch_and_publish_news():
    global iteration
    try:
        while True:  # Infinite loop
            iteration += 1  # Increment iteration counter
            logging.info(f"Iteration: {iteration}")
            
            # Fetch top headlines from NewsAPI
            top_headlines = newsapi.get_top_headlines(language='en', country='us')
            
            # Publish articles to Kafka topic
            for article in top_headlines['articles']:
                description = article.get('description')
                
                if description is not None:
                    producer.produce('named_er', key=article['title'], value=description.encode('utf-8'), callback=delivery_report)
                else:
                    logging.warning(f"Skipping article with title '{article['title']}' due to missing description.")
                
                # Wait for the message to be delivered or an error to occur
                producer.poll(0)
            
            # Flush the producer
            producer.flush()
            
            # Sleep for 60 seconds before fetching new headlines again
            time.sleep(15)
    except KeyboardInterrupt:
        logging.info("Script interrupted. Exiting...")
    finally:
        # Close the producer
        producer.flush()
        producer.close()

if __name__ == '__main__':
    fetch_and_publish_news()
