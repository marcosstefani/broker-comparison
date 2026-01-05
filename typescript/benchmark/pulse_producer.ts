import { Producer } from 'pulse-sdk';
import { MESSAGE_COUNT, TOPIC_NAME, PAYLOAD } from './config';
import { saveResult } from './report';

const producer = new Producer();

async function run() {
    console.log(`Pulse Producer (TS): Starting to produce ${MESSAGE_COUNT} messages...`);
    const start = Date.now();

    for (let i = 1; i <= MESSAGE_COUNT; i++) {
        await producer.send(TOPIC_NAME, PAYLOAD);
        
        if (i % 100000 === 0) {
            const duration = (Date.now() - start) / 1000;
            console.log(`Pulse Producer (TS): Reached ${i} messages in ${duration.toFixed(4)}s`);
            saveResult("Pulse (TS)", "Producer", i, duration);
        }
    }

    await producer.close();
    const duration = (Date.now() - start) / 1000;
    console.log(`\nPulse Producer (TS): ${MESSAGE_COUNT} messages in ${duration.toFixed(4)} seconds`);
    saveResult("Pulse (TS)", "Producer", MESSAGE_COUNT, duration);
}

run().catch(console.error);
