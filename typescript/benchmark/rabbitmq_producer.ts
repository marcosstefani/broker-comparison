import * as amqp from 'amqplib';
import { MESSAGE_COUNT, TOPIC_NAME, PAYLOAD } from './config';
import { saveResult } from './report';

async function run() {
    const conn = await amqp.connect('amqp://user:password@localhost:5672');
    const ch = await conn.createChannel();
    await ch.assertQueue(TOPIC_NAME);

    console.log(`RabbitMQ Producer (TS): Starting to produce ${MESSAGE_COUNT} messages...`);
    const start = Date.now();
    const payload = Buffer.from(JSON.stringify(PAYLOAD));

    for (let i = 1; i <= MESSAGE_COUNT; i++) {
        const ok = ch.sendToQueue(TOPIC_NAME, payload);
        if (!ok) {
            await new Promise<void>(resolve => ch.once('drain', resolve));
        }
        
        if (i % 100000 === 0) {
            const duration = (Date.now() - start) / 1000;
            console.log(`RabbitMQ Producer (TS): Reached ${i} messages in ${duration.toFixed(4)}s`);
            saveResult("RabbitMQ (TS)", "Producer", i, duration);
        }
    }

    await ch.close();
    await conn.close();
    
    const duration = (Date.now() - start) / 1000;
    console.log(`\nRabbitMQ Producer (TS): ${MESSAGE_COUNT} messages in ${duration.toFixed(4)} seconds`);
    saveResult("RabbitMQ (TS)", "Producer", MESSAGE_COUNT, duration);
}

run().catch(console.error);
