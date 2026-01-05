import * as amqp from 'amqplib';
import { MESSAGE_COUNT, TOPIC_NAME } from './config';
import { saveResult } from './report';

async function run() {
    const conn = await amqp.connect('amqp://user:password@localhost:5672');
    const ch = await conn.createChannel();
    await ch.assertQueue(TOPIC_NAME);

    let count = 0;
    let startTime: number | null = null;

    console.log(`RabbitMQ Consumer (TS): Waiting for ${MESSAGE_COUNT} messages...`);

    await ch.consume(TOPIC_NAME, (msg) => {
        if (!msg) return;

        if (count === 0) {
            startTime = Date.now();
            console.log("RabbitMQ Consumer (TS): First message received.");
        }
        
        count++;
        
        if (count % 100000 === 0 && startTime) {
            const duration = (Date.now() - startTime) / 1000;
            console.log(`RabbitMQ Consumer (TS): Reached ${count} messages in ${duration.toFixed(4)}s`);
            saveResult("RabbitMQ (TS)", "Consumer", count, duration);
        }

        if (count >= MESSAGE_COUNT && startTime) {
            const duration = (Date.now() - startTime) / 1000;
            console.log(`\nRabbitMQ Consumer (TS): ${MESSAGE_COUNT} messages in ${duration.toFixed(4)} seconds`);
            saveResult("RabbitMQ (TS)", "Consumer", MESSAGE_COUNT, duration);
            
            // Close and exit
            ch.close().then(() => conn.close()).then(() => process.exit(0));
        }
    }, { noAck: true });
}

run().catch(console.error);
