import { consumer, run, commit, Message } from 'pulse-sdk';
import { MESSAGE_COUNT, TOPIC_NAME } from './config';
import { saveResult } from './report';

let count = 0;
let startTime: number | null = null;

console.log(`Pulse Consumer (TS): Waiting for ${MESSAGE_COUNT} messages...`);

consumer(TOPIC_NAME, async (msg: Message) => {
    if (count === 0) {
        startTime = Date.now();
        console.log("Pulse Consumer (TS): First message received.");
    }
    
    count++;

    if (count % 1000 === 0) {
        await commit();
        if (count % 100000 === 0 && startTime) {
            const duration = (Date.now() - startTime) / 1000;
            console.log(`Pulse Consumer (TS): Reached ${count} messages in ${duration.toFixed(4)}s`);
            saveResult("Pulse (TS)", "Consumer", count, duration);
        }
    }

    if (count >= MESSAGE_COUNT && startTime) {
        await commit();
        const duration = (Date.now() - startTime) / 1000;
        console.log(`\nPulse Consumer (TS): ${MESSAGE_COUNT} messages in ${duration.toFixed(4)} seconds`);
        saveResult("Pulse (TS)", "Consumer", MESSAGE_COUNT, duration);
        process.exit(0);
    }
}, { autoCommit: false });

run();
